# Results Analysis - Parte 1

Tareas generadas: 20

## Resultados

-   Hilos: tiempo = 1.505s, tareas completadas = 20
-   Procesos: tiempo = 2.301s, tareas completadas = 20

## Observaciones

-   En este experimento los hilos fueron más rápidos. Esto puede darse cuando el trabajo es I/O bound (limitado por entrada y salida de datos) o simulado por time.sleep(), lo cual son operaciones sencillas que son cobiertas perfectamente por la concurrencia. Aunque en tareas que requerieran mayor potencia de computo deberían ser mejores los procesos.
    
-   Cuándo usar hilos (threads):
    
    -   Cuando las tareas son I/O-bound (esperas de red, lectura/escritura de disco, time.sleep, operaciones bloqueantes). En Python, los hilos permiten ocultar la latencia y mantener alta concurrencia.
    -   Cuando necesitas compartir memoria/estado entre tareas con bajo overhead (los hilos comparten el mismo espacio de memoria, facilitando acceso a estructuras comunes).
    -   Cuando la sobrecarga de crear/gestionar concurrencia debe ser baja (crear hilos suele ser más ligero que procesos).
-   Cuándo usar procesos (multiprocessing):
    
    -   Cuando las tareas son CPU-bound (cálculos intensivos, procesamiento numérico).
    -   Cuando quieres aislamiento entre tareas (fallos en un proceso no corrompen la memoria del resto).
    -   Cuando la escalabilidad en CPU es prioritaria y la memoria adicional/overhead por proceso es aceptable.