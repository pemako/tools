import os
import signal
import sys
import time
from multiprocessing import Condition, Manager, Process, Value

from config import log as logger


class Multi_pService():
    """Multi_p Service"""

    def __init__(self, cfg, execute_dir):
        self.execute_dir = execute_dir
        # worker
        self.worker_mum = cfg.service.workers
        # self.workers = []
        self.is_running = Value("b", False)
        self.stop_condition = Condition()
        # 初始化多进程间共享的容器
        manager = Manager()
        # 存放缓存的dict，约定key需要一个特定类型的prefix，即[type_value]
        # 例如媒体信息：'media_12306'，offer信息：'creative_10086'
        # 对这个dict的读写是进程安全的
        self.cache_dict = manager.dict()

    @property
    def workers(self):
        return []

    def init_signal_handler(self):
        """删除不需要处理的信号，以及增加需要处理的信号,并且设置不同的处理方法
        这里默认处理了SIGTERM和SIGINT，并且尝试停止service
        SIGINT = 2，可使用kill -2 pid 或 当CTRL+C终止程序时发出
        SIGTERM = 15，可使用kill -15 pid发出"""

        signals = (signal.SIGTERM, signal.SIGINT)
        self.signal_handlers = {}
        for sig in signals:
            self.signal_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self.handle_signal)

    def handle_signal(self, signal, frame):
        logger.info("Handle signal {}, stop service", signal)
        logger.info("Try to stop all workers.")
        self.stop()
        time.sleep(1)
        logger.info("Bye-bye.")
        sys.exit(0)

    def worker_process(self):
        while self.is_running.value:
            logger.info("Worker process {} is working", os.getpid())
            time.sleep(1)

        logger.info("Worker process {} quits", os.getpid())

    def run(self):
        logger.info("Multi_p service starts to run.")
        self.init_signal_handler()

        logger.info("Start multi_p service")
        self.is_running.value = True

        # fork the children
        for i in range(10):
            try:
                w = Process(target=self.worker_process)
                w.daemon = True
                w.start()
                self.workers.append(w)
            except Exception as x:
                logger.critical(x)

        for w in self.workers:
            w.join()

        # wait until the condition is set by stop()
        while True:
            self.stop_condition.acquire()
            try:
                self.stop_condition.wait()
                break
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception as x:
                logger.critical(x)

        self.is_running.value = False

    def stop(self):
        logger.info("Multi_p service will stop.")
        self.is_running.value = False
        self.stop_condition.acquire()
        self.stop_condition.notify()
        self.stop_condition.release()
