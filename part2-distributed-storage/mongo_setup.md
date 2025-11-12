# MongoDB setup (Docker)

Instrucciones rápidas para levantar dos nodos MongoDB usando `docker-compose`:

1. Ir a la carpeta `exam-sistemas-distribuidos` (donde está el `docker-compose.yml`).
2. Ejecutar:

```bash
docker-compose up -d
```

3. Verificar contenedores:

```bash
docker ps
```

4. Para detenerlos:

```bash
docker-compose down
```

Nota: en este entorno de desarrollo no se ha levantado Docker; el archivo `storage_system.py` incluye un modo `use_mock=True` para permitir pruebas sin MongoDB.
