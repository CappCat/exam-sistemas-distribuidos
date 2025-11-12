import multiprocessing
import threading
import time
import random

def _process_worker(task_id, difficulty, counter):
    """Worker para procesos: simula trabajo y actualiza contador compartido."""
    processing_time = difficulty * 0.3
    time.sleep(processing_time)
    # Actualizar contador compartido de manera segura
    with counter.get_lock():
        counter.value += 1


class TaskProcessor:
    def __init__(self):
        # Lock para hilos
        self.thread_lock = threading.Lock()
        self.tasks_completed_threads = 0

        # Contador compartido para procesos
        self.tasks_completed_processes = multiprocessing.Value('i', 0)

    def process_task(self, task_id, difficulty):
        #Simula procesamiento con diferente dificultad. 
        # difficulty: 1 (fácil) - 5 (difícil)

        processing_time = difficulty * 0.3
        time.sleep(processing_time)
        result = task_id * difficulty
        return result

    def _worker_thread(self, task):
        task_id, difficulty = task
        _ = self.process_task(task_id, difficulty)
        with self.thread_lock:
            self.tasks_completed_threads += 1

    def run_with_threads(self, tasks):
        """Ejecuta las tareas usando hilos. Devuelve (elapsed_seconds, tasks_completed)."""
        self.tasks_completed_threads = 0
        threads = []
        start = time.time()
        for task in tasks:
            t = threading.Thread(target=self._worker_thread, args=(task,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        elapsed = time.time() - start
        return elapsed, self.tasks_completed_threads

    def run_with_processes(self, tasks):
        """Ejecuta las tareas usando procesos. Devuelve (elapsed_seconds, tasks_completed)."""
        # Reiniciar contador
        with self.tasks_completed_processes.get_lock():
            self.tasks_completed_processes.value = 0

        processes = []
        start = time.time()
        for task_id, difficulty in tasks:
            p = multiprocessing.Process(target=_process_worker, args=(task_id, difficulty, self.tasks_completed_processes))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        elapsed = time.time() - start
        return elapsed, self.tasks_completed_processes.value


def generate_tasks(n=20):

    return [(i, random.randint(1, 5)) for i in range(1, n + 1)]


if __name__ == '__main__':
    
    tasks = generate_tasks(20)
    tp = TaskProcessor()

    print("Ejecutando con hilos...")
    t_threads, completed_threads = tp.run_with_threads(tasks)
    print(f"Hilos - Tiempo: {t_threads:.3f}s, Tareas completadas: {completed_threads}")

    print("Ejecutando con procesos...")
    t_procs, completed_procs = tp.run_with_processes(tasks)
    print(f"Procesos - Tiempo: {t_procs:.3f}s, Tareas completadas: {completed_procs}")

