import os
import logging
import shutil
from typing import NoReturn

from .errors import ClientError
LOG_BASE = "/log"

SERVER_LOG_PATH = os.path.join(LOG_BASE, "judge_server.log")

logger = logging.getLogger(__name__)
handler = logging.FileHandler(SERVER_LOG_PATH)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

DEBUG = os.getenv("judger_debug") == "1"

class InitSubmissionEnv(object):
    """
    create environment for submission and delete when done
    """
    def __init__(self, workspace: str, hw_id: str):
        self.work_dir = os.path.join(workspace, hw_id)

    def __enter__(self) -> str:
        try:
            os.mkdir(self.work_dir)
        except OSError as exception:
            logger.exception(exception)
            ClientError("failed to create runtime dir")
        return self.work_dir

    def __exit__(self, exc_type, exc_val, exc_tb)  -> NoReturn:
        if not DEBUG:
            try:
                shutil.rmtree(self.work_dir)
            except OSError as exception:
                logger.exception(exception)
                ClientError("failed to clean runtime dir")