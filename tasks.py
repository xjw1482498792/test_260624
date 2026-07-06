from time import sleep

from celery import Celery


app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


@app.task
def slow_add(x, y):
    print(f"Worker: starting slow_add({x}, {y})")
    sleep(5)
    print("Worker: finished slow_add")
    return x + y


if __name__ == "__main__":
    result = slow_add.delay(12, 3)

    print("Task submitted.")
    print(f"Task id: {result.id}")
    print("Start a worker in another terminal:")
    print("celery -A tasks worker -P solo -l info")
