# Examen - Sistemas Distribuidos

Este repositorio contiene una solución de ejemplo para el examen práctico de Sistemas Distribuidos.

Estructura incluida:

- `part1-processes-threads/` : Código y análisis de la Parte 1 (procesos vs hilos)
- `part2-distributed-storage/` : Código y documentación de la Parte 2 (almacenamiento distribuido)
- `docker-compose.yml` : Composición Docker para levantar 2 nodos MongoDB y el script de la parte 2

Requisitos locales para probar Parte 1:
- Python 3.8+ (no se requieren paquetes externos aparte de la stdlib para ejecutar la Parte 1)

Cómo ejecutar la Parte 1 (desde la raíz `exam-sistemas-distribuidos`):
```powershell
python .\part1-processes-threads\task_processor.py
```

El script generará 20 tareas con dificultad aleatoria, ejecutará la versión con hilos y con procesos, medirá tiempos y guardará un análisis en `part1-processes-threads/results_analysis.md`.

Parte 2:
- Se incluye `docker-compose.yml` para levantar dos instancias de MongoDB.
- `part2-distributed-storage/storage_system.py` incluye un script que se ejecuta mediante las instrucciones en el archivo que está dentro de la carpeta, el dockerFile crea un contenedor con las dependencias del script.

