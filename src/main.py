import json
import os
from typing import Optional
from argparse import ArgumentParser

from const import DB_FILES, DATA_DIR
from src.config import ME
from utils import auth_db, logger, get_tables_of_conn, get_table_cols, init_db_keys_dict
from handle_friends import find_friend, get_friend_md5, get_friend_name
from handle_groups import find_group, get_group_md5, get_group_name

import pandas as pd


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
            logger.info(f"found in {table}")
            return parse_chats(table)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--task", '-t', help="目标任务", choices=["dump-chat"], default="dump-chat")
    parser.add_argument('--friend', '-f', help="例如：'朱思奕'")
    parser.add_argument('--group', '-g', help="例如：'樱花三结义'")

    args = parser.parse_args()

    logger.info({"args": args})

    chat_name = None
    chat_md5 = False
    init_db_keys_dict()

    if args.friend:
        logger.info(f"searching friend for {args.friend}")
        friend = find_friend(args.friend)
        if friend:
            chat_md5 = get_friend_md5(friend)
            chat_name = get_friend_name(friend)
            logger.info(f"found friend: {chat_name}, md5: {chat_md5}")

    if args.group and not chat_md5:
        logger.info(f"searching group for {args.group}")
        group = find_group(args.group)
        if group:
            chat_md5 = get_group_md5(group)
            chat_name = get_group_name(group)
            logger.info(f"found group: {chat_name}, md5: {chat_md5}")

    if not chat_md5:
        raise Exception(f"not found target chat")

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
            sender = chat_name if v["mesSvrID"] == 1 else ME
            send_time = v["IntRes2"]
            chats.append({"sender": sender, "content": content, "send_time": send_time})

    json.dump(chats, open(os.path.join(DATA_DIR, f"chats-{chat_name}.json"), "w"), ensure_ascii=False, indent=2)
