from lib.executor import Executor
from lib.logger import setup_logger

# logger settings
setup_logger()

# start
Executor.start()
