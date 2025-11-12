# Storage system (Docker)

Esta carpeta contiene `storage_system.py`, una pequeña app que inserta documentos en dos instancias MongoDB y genera `distribution_results.md`.

Cómo construir y ejecutar (PowerShell / Windows):

1) Levantar las instancias MongoDB definidas en la raíz con docker-compose:

```powershell
cd ..\
docker-compose up -d
```

2) Construir la imagen para la app (desde `part2-distributed-storage`):

```powershell
cd part2-distributed-storage
docker build -t storage-system:local .
```

3) Ejecutar el contenedor (se conectará a los Mongo locales mapeados por el compose):

```powershell
docker run --rm -v ${PWD}:/app --network host storage-system:local
```

Nota:
- `storage_system.py` por defecto intenta conectar a `mongodb://localhost:27017` y `mongodb://localhost:27018`.
- En Windows, `--network host` puede no funcionar igual que en Linux; si no funciona, ejecuta el contenedor en la misma red que `docker-compose` o pasa `--add-host` para apuntar a la máquina host.
