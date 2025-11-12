import hashlib
from datetime import datetime
from pathlib import Path
import random
import sys

from pymongo import MongoClient


class DistributedStorage:
    """Almacenamiento distribuido conectado a dos instancias MongoDB.

    Conecta a los URIs especificados (por defecto localhost:27017 y :27018).
    """

    def __init__(self, mongo_uris=None):
        # mongo_uris expected as tuple: (uri1, uri2)
        uri1 = 'mongodb://localhost:27017'
        uri2 = 'mongodb://localhost:27018'
        if mongo_uris:
            uri1, uri2 = mongo_uris

        # Intentar conectar a ambos nodos con timeout corto
        self.client1 = MongoClient(uri1, serverSelectionTimeoutMS=3000)
        self.client2 = MongoClient(uri2, serverSelectionTimeoutMS=3000)

        # Forzar comprobación de conexión (puede lanzar excepción si falla)
        self.client1.admin.command('ping')
        self.client2.admin.command('ping')

        self.db1 = self.client1['distributed_db']
        self.db2 = self.client2['distributed_db']

    def _select_node_for_document(self, document_data):
        document_id = str(document_data.get('id', len(document_data)))
        hash_value = hashlib.md5(document_id.encode()).hexdigest()
        node_index = int(hash_value, 16) % 2
        if node_index == 0:
            return 'db1', 'node1'
        else:
            return 'db2', 'node2'

    def insert_document(self, data):
        node_key, node_name = self._select_node_for_document(data)
        doc = {
            '_id': data.get('id'),
            'data': data,
            'node': node_name,
            'created_at': datetime.now().isoformat(),
        }
        coll = self.db1['documents'] if node_key == 'db1' else self.db2['documents']
        # Usar upsert para evitar duplicados si se reinserta
        coll.replace_one({'_id': doc['_id']}, doc, upsert=True)
        return True, node_name

    def find_document(self, document_id):
        results = []
        doc1 = self.db1['documents'].find_one({'_id': document_id})
        if doc1:
            doc1['source_node'] = 'node1'
            results.append(doc1)
        doc2 = self.db2['documents'].find_one({'_id': document_id})
        if doc2:
            doc2['source_node'] = 'node2'
            results.append(doc2)
        return results

    def get_stats(self):
        c1 = int(self.db1['documents'].count_documents({}))
        c2 = int(self.db2['documents'].count_documents({}))

        total = c1 + c2
        percent1 = (c1 / total * 100) if total else 0
        percent2 = (c2 / total * 100) if total else 0
        return {
            'node1_count': c1,
            'node2_count': c2,
            'total': total,
            'node1_percent': percent1,
            'node2_percent': percent2,
        }


def generate_sample_data(num_documents=100):
    sample_data = []
    for i in range(num_documents):
        sample_data.append({
            'id': i,
            'name': f'Documento_{i}',
            'value': i * 10,
            'category': f'categoria_{i % 5}',
            'timestamp': datetime.now().isoformat(),
        })
    return sample_data


def main(argv=None):
    argv = argv or sys.argv[1:]
    # Allow optional custom URIs via args: --uri1 <uri> --uri2 <uri>
    uri1 = 'mongodb://localhost:27017'
    uri2 = 'mongodb://localhost:27018'
    if '--uri1' in argv:
        i = argv.index('--uri1')
        if i + 1 < len(argv):
            uri1 = argv[i + 1]
    if '--uri2' in argv:
        i = argv.index('--uri2')
        if i + 1 < len(argv):
            uri2 = argv[i + 1]

    print(f'Modo: MongoDB real. Intentando conectar a {uri1} y {uri2} ...')
    try:
        ds = DistributedStorage(mongo_uris=(uri1, uri2))
    except Exception as e:
        print('ERROR: No se pudo conectar a MongoDB. Asegúrate de que Docker esté levantado o que MongoDB esté accesible en los puertos especificados.')
        print('Detalle:', e)
        print('\nPuedes levantar los contenedores con:')
        print('  cd exam-sistemas-distribuidos; docker-compose up -d')
        sys.exit(1)

    docs = generate_sample_data(100)
    for d in docs:
        ds.insert_document(d)

    stats = ds.get_stats()
    # Guardar en archivo
    out = Path(__file__).parent / 'distribution_results.md'
    with out.open('w', encoding='utf-8') as f:
        f.write('# Distribución de documentos (MongoDB real)\n\n')
        f.write(f"Total: {stats['total']}\n\n")
        f.write(f"- Nodo 1: {stats['node1_count']} ({stats['node1_percent']:.2f}%)\n")
        f.write(f"- Nodo 2: {stats['node2_count']} ({stats['node2_percent']:.2f}%)\n")

    # Print final con estadísticas (solicitado)
    print('\n=== Estadísticas de distribución (MongoDB real) ===')
    print(f"Total documentos: {stats['total']}")
    print(f"Nodo 1: {stats['node1_count']} ({stats['node1_percent']:.2f}%)")
    print(f"Nodo 2: {stats['node2_count']} ({stats['node2_percent']:.2f}%)")
    print('Archivo de resultados guardado en:', out)


if __name__ == '__main__':
    main()
