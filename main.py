from lib.executor import Executor
from lib.logger import setup_logger

# log format
setup_logger()

# start
Executor.start()
