from queue import Queue
from threading import Thread
from time import sleep, strftime


# 模拟 Celery 里的 broker，比如 Redis / RabbitMQ。
# 主程序把任务放进这个队列，worker 从这个队列取任务。
task_queue = Queue()


def log(message):
    print(f"{strftime('%H:%M:%S')} | {message}")


def slow_add(x, y):
    # 模拟一个耗时任务，比如发邮件、生成报表、处理文件。
    log(f"worker: start slow_add({x}, {y})")
    sleep(5)
    result = x + y
    log(f"worker: finished, result = {result}")


def worker():
    # 模拟 Celery worker：一直运行，等待队列里出现新任务。
    while True:
        # 如果队列为空，get() 会停在这里等待，不会继续往下执行。
        task_name, args = task_queue.get()

        if task_name == "slow_add":
            slow_add(*args)

        # 告诉队列：刚才取出的任务已经处理完了。
        task_queue.task_done()


def submit_task(task_name, *args):
    # 模拟 Celery 的 xxx.delay(...)：只提交任务，不在这里执行任务。
    task_queue.put((task_name, args))
    log(f"main: submitted {task_name}{args}")


if __name__ == "__main__":
    # 启动一个后台 worker。
    # daemon=True 表示主程序结束时，这个后台线程也会跟着结束。
    Thread(target=worker, daemon=True).start()

    log("main: user sends a request")
    submit_task("slow_add", 2, 3)
    log("main: response returned immediately")

    log("main: program can do other things now")
    task_queue.join()
    log("main: all background tasks done")
