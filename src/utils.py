import hashlib
import json
import logging
import os
from typing import List

from const import DB_CRACK_PATH
from src.config import WECHAT_DB_ROOT
from pysqlcipher3 import dbapi2 as sqlite
from pysqlcipher3.dbapi2 import Connection


logging.basicConfig(
                    format='%(asctime)s - %(module)15s - %(levelname)5s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


db_keys_dict = {}


def md5(s: str) -> str:
    # ref: - [(25条消息) Python之MD5加密_毕来生-CSDN博客](https://blog.csdn.net/qq_878799579/article/details/74324869)
    hl = hashlib.md5()
    hl.update(s.encode(encoding="utf-8"))
    return hl.hexdigest()


def get_db_path(db_file: str):
    """

    :param db_file:
        sample: "Message/msg_0.db"
    :return:
    """
    return os.path.join(WECHAT_DB_ROOT, db_file)


def get_db_key(db_file: str) -> str:
    if not db_keys_dict:
        raise Exception("init db_keys_dict first!")
    return db_keys_dict[db_file]


def auth_db(db_file: str) -> Connection:
    logger.info(f"authenticating {db_file}")

    db_key = get_db_key(db_file)
    logger.info({"db_key": db_key})

    db_path = get_db_path(db_file)
    logger.info({"dp_path": db_path})

    logger.info(f"connecting {db_file}")
    conn = sqlite.connect(db_path)
    logger.info(f"connected {db_file}")

    conn.execute(f'PRAGMA key = "{db_key}";')
    conn.execute(f"PRAGMA cipher_compatibility = 3;")
    conn.commit()

    logger.info(f"authenticated {db_file}")

    return conn


def get_tables_of_conn(conn: Connection) -> List[str]:
    return list(i[0] for i in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'"))


def get_table_cols(conn: Connection, table_name: str) -> List[str]:
    return sorted(list(i[1] for i in conn.execute(f"PRAGMA table_info({table_name})")))


def init_db_keys_dict():
    global db_keys_dict
    db_keys_dict = json.load(open(DB_CRACK_PATH))
    logger.debug({"db_keys_dict": db_keys_dict})

