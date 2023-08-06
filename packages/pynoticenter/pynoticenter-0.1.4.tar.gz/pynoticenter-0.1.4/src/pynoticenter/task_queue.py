import asyncio
import logging
import threading
import time
from typing import Any

from pynoticenter import utils
from pynoticenter.task import PyNotiTask


class PyNotiTaskQueue(object):
    """PyNotiTaskQueue, each task queue has its own thread. All function thread safety"""

    __name: str = ""
    __lock: threading.RLock = None
    __is_terminated: bool = False
    __wait_until_task_done: bool = True
    __is_started: bool = False
    __task_id_count: int = 0
    __task_dict: dict[str, PyNotiTask] = None
    __first_tasks: list[str] = None
    __thread: threading.Thread = None
    __loop: asyncio.AbstractEventLoop = None
    __preprocessor: callable = None

    def __init__(self, name: str):
        self.__name = name if name is not None else f"{id(self)}"
        self.__lock = threading.RLock()
        self.__task_dict = dict()
        self.__first_tasks = list()
        self.__thread = threading.Thread(target=self.__worker_thread__)
        self.__preprocessor = None

    @property
    def is_terminated(self) -> bool:
        with self.__lock:
            return self.__is_terminated

    @property
    def task_count(self) -> int:
        with self.__lock:
            return len(self.__task_dict)

    def __terminate_thread_callback__(self, wait: bool):
        # run in thread.
        wait_interval = 0.5
        with self.__lock:
            if self.__is_terminated:
                return

        with self.__lock:
            self.__is_terminated = True
            self.__wait_until_task_done = wait
            if not wait and self.__loop is not None:
                self.__loop.call_soon_threadsafe(self.__cancel_scheduled_task__)
        self.__wait_until_tasks_cleanup__(wait_interval)

        # stop run loop and wait for thread exit.
        with self.__lock:
            if self.__loop is not None:
                self.__loop.call_soon_threadsafe(self.__cleannup_thread__)
        self.__wait_until_thread_exit__(wait_interval)

    def terminate(self, wait: bool = True):
        # terminate thread and stop event loop
        logging.info(f"{self.__log_prefix__()}: Task queue terminate. wait: {wait}")
        event = utils.RunInThread(self.__terminate_thread_callback__, wait)
        if wait:
            utils.Wait(event)

    def set_preprocessor(self, preprocessor: callable):
        with self.__lock:
            self.__preprocessor = preprocessor

    def post_task(self, fn: callable, *args: Any, **kwargs: Any) -> str:
        return self.post_task_with_delay(0, fn, *args, **kwargs)

    def post_task_with_delay(self, delay: float, fn: callable, *args: Any, **kwargs: Any) -> str:
        task_id = ""
        with self.__lock:
            if self.is_terminated:
                logging.info(f"{self.__log_prefix__():}: task queue is terminated. ignore new task.")
                return

            # add task
            task_id = str(self.__task_id_count + 1)
            self.__task_id_count += 1
            self.__task_dict[task_id] = PyNotiTask(task_id, delay, fn, self.__preprocessor, *args, **kwargs)

            # start thread
            if not self.__is_started:
                self.__is_started = True
                self.__thread.start()

            # dispatch task, if thread not create, record it and it will be reschedule later.
            if self.__loop is not None:
                # cross thread function call, must use threadsafe.
                self.__loop.call_soon_threadsafe(self.__schedule_task__, task_id)
            else:
                self.__first_tasks.append(task_id)

        return task_id

    def cancel_task(self, task_id: str):
        logging.info(f"{self.__log_prefix__()}: cancel task {task_id}")
        task: PyNotiTask = None
        with self.__lock:
            task = self.__pop_task__(task_id)
        if task is not None:
            task.cancel()

    def __pop_task__(self, task_id: str) -> PyNotiTask:
        with self.__lock:
            if task_id in self.__task_dict:
                return self.__task_dict.pop(task_id)

    def __log_prefix__(self):
        return f"TaskQueue[{self.__name}]"

    def __wait_until_tasks_cleanup__(self, wait_interval: float):
        # wait for all task finish
        task_count = self.task_count
        logging.info(f"{self.__log_prefix__()}: waiting for tasks cleanup. tasks: {task_count}")
        wait_time = 0.0
        while True:
            task_count = self.task_count
            if task_count == 0:
                break
            time.sleep(wait_interval)
            wait_time += wait_interval
            logging.debug(f"{self.__log_prefix__()}: waiting for tasks finish. time: {wait_time} tasks: {task_count}")
        logging.info(f"{self.__log_prefix__()}: All tasks cleanup. wait time: {wait_time}")

    def __wait_until_thread_exit__(self, wait_interval: float):
        logging.info(f"{self.__log_prefix__()}: waiting for thread exit.")
        wait_time = 0.0
        while True:
            with self.__lock:
                if self.__thread is None or not self.__is_started:
                    break
            wait_time += wait_interval
            time.sleep(wait_interval)
            logging.debug(f"{self.__log_prefix__()}: waiting for thread exit. time: {wait_time}")
        logging.info(f"{self.__log_prefix__()}: thread exit. wait time: {wait_time}")

    def __cancel_scheduled_task__(self):
        logging.info(f"{self.__log_prefix__()}: cancel scheduled task.")
        with self.__lock:
            task_ids = list()
            task_ids.extend(self.__task_dict.keys())
            for task_id in task_ids:
                self.cancel_task(task_id)

    def __cleannup_thread__(self):
        logging.info(f"{self.__log_prefix__()}: stop event run loop.")
        with self.__lock:
            self.__loop.stop()

    def __schedule_task__(self, task_id: str):
        # call from worker thread, asyncio event loop.
        log_prefix = f"{self.__log_prefix__()} Task[{task_id}]:"
        logging.debug(f"{log_prefix} schedule task.")
        need_execute = False
        delay = 0
        task: PyNotiTask = None
        with self.__lock:
            if task_id in self.__task_dict:
                task = self.__task_dict[task_id]

            if task is None:
                logging.debug(f"{log_prefix} task has been cancelled or not exist.")
                self.__pop_task__(task_id)
                return

            if self.is_terminated and not self.__wait_until_task_done:
                logging.debug(f"{log_prefix} task queue terminated, cancel schedule task.")
                task.cancel()
                self.__pop_task__(task_id)
                return

            if task.delay == 0:
                need_execute = True
            else:
                delay = task.delay
                logging.debug(f"{log_prefix} task delay execute in {delay}.")
                handler = self.__loop.call_later(delay, self.__schedule_task__, task_id)
                task.set_delay(0)
                task.set_timer_handle(handler)

        if need_execute:
            task.execute()
            self.__pop_task__(task_id)

    def __worker_thread__(self):
        logging.info(f"{self.__log_prefix__()}: worker thread begin.")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        with self.__lock:
            self.__loop = loop

            if self.__is_terminated and not self.__wait_until_task_done:
                # terminate before the thread start.
                for task_id in self.__first_tasks:
                    self.cancel_task(task_id)
                self.__first_tasks.clear()
                # recancel the schedule task again
                self.__loop.call_soon(self.__cancel_scheduled_task__)

            for task_id in self.__first_tasks:
                self.__loop.call_soon(self.__schedule_task__, task_id)
            self.__first_tasks.clear()

        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            logging.info(f"{self.__log_prefix__()}: worker thread end.")
            with self.__lock:
                self.__thread = None
