# MongoDB setup (Docker)

Instrucciones rápidas para levantar dos nodos y el script de python MongoDB usando `docker-compose`:

1. Ir a la carpeta `exam-sistemas-distribuidos` (donde está el `docker-compose.yml`).
2. Ejecutar:

```bash
docker-compose up -d
```

3. Verificar contenedores:

```bash
docker ps
```

4. Para ver los logs del sistema:

```bash
docker-compose logs -f storage
```

5. Para detenerlos:

```bash
docker-compose down
```

