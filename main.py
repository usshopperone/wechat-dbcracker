import json
from typing import Optional

from const import DB_FILES, ME
from utils import auth_db, logging, get_tables_of_conn, sqlite, Connection, get_table_cols
from handle_friends import find_friend_md5
from handle_groups import find_group_md5

import pandas as pd

logger = logging.getLogger("main")


def find_chat_in_msg_db(db_file: str) -> Optional[pd.DataFrame]:
    conn = auth_db(db_file)

    def parse_chats(table: str) -> pd.DataFrame:
        data = list(conn.execute(f"SELECT * from {table}"))
        columns = get_table_cols(conn, table)
        df = pd.DataFrame(columns=columns, data=data)
        logger.info({"shape": df.shape})
        return df

    for table in get_tables_of_conn(conn):
        logger.debug(f"handling {table}")
        if chat_md5 in table:
            logger.info(f"found {TARGET_NAME} in {table}")
            return parse_chats(table)


if __name__ == '__main__':

    TARGET_NAME = "樱花三结义"
    IS_FIND_FRIEND = False
    IS_FIND_GROUP = True

    chat_md5 = False

    if IS_FIND_FRIEND:
        logger.info(f"searching friend for {TARGET_NAME}")
        chat_md5 = find_friend_md5(TARGET_NAME)
        if chat_md5:
            logger.info(f"found md5 of friend: {chat_md5}")

    if IS_FIND_GROUP and not chat_md5:
        logger.info(f"searching group for {TARGET_NAME}")
        chat_md5 = find_group_md5(TARGET_NAME)
        if chat_md5:
            logger.info(f"found md5 of group: {chat_md5}")

    if not chat_md5:
        raise Exception(f"not found target chat of {TARGET_NAME}")

    df = None
    for db_file in DB_FILES:
        if "msg" in db_file:
            df = find_chat_in_msg_db(db_file)
            if df is not None:
                break

    chats = []
    if df is not None:
        for (k, v) in df.iterrows():
            content = v["StrRes1"]
            sender = TARGET_NAME if v["mesSvrID"] == 1 else ME
            send_time = v["IntRes2"]
            chats.append({"sender": sender, "content": content, "send_time": send_time})

    json.dump(chats, open(f"chats-{TARGET_NAME}.json", "w"), ensure_ascii=False, indent=2)