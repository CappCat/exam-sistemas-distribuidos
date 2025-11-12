# Results Analysis - Parte 1

Tareas generadas: 20

## Resultados

- Hilos: tiempo = 1.505s, tareas completadas = 20
- Procesos: tiempo = 2.301s, tareas completadas = 20

## Observaciones

- En este experimento los hilos fueron más rápidos. Esto puede darse cuando el trabajo es I/O bound o simulado por time.sleep(), lo cual son operaciones sencillas que son cobiertas perfectamente por la concurrencia. Aunque en tareas que requerieran mayor potencia de computo deberían ser mejores los procesos.
