from typing import Optional

import pandas as pd

from utils import md5, get_tables_of_conn, get_table_cols, auth_db, logger
from const import FIELD_MD5_NAME


'''
# columns of a user:

'_packed_WCContactData',
-> 'm_nsAliasName',
'm_nsBrandIconUrl', 'm_nsChatRoomAdminList', 'm_nsChatRoomDesc', 'm_nsChatRoomMemList',
'm_nsDraft', 'm_nsEncodeUserName', 'm_nsFullPY', 'm_nsGoogleContactName',
'm_nsHeadHDImgUrl'(big image), 'm_nsHeadHDMd5'(null), 'm_nsHeadImgUrl'(small image), 'm_nsImgStatus',
-> 'm_nsRemark', 'm_nsRemarkPYFull', 'm_nsRemarkPYShort',
'm_nsShortPY',
-> 'm_nsUsrName'(wxid),
'm_patSuffix',
'm_uiCertificationFlag',
'm_uiChatRoomMaxCount', 'm_uiChatRoomStatus', 'm_uiChatRoomVersion',
'm_uiConType', 'm_uiImgKey',
'm_uiSex'(0: female, 1: male, 2: unknown),
'm_uiType'(cannot understand what does it mean, according to the data),
-> 'nickname',
'openIMInfo'
'''

DB_FILE = "Contact/wccontact_new2.db"

CONTACT_COLUMNS_SELECTED = ["m_nsUsrName", "nickname", "m_nsRemark", "m_nsAliasName", "m_uiSex",
                            "m_nsHeadHDImgUrl"]
CONTACT_COLUMNS_DUMPED = [FIELD_MD5_NAME] + CONTACT_COLUMNS_SELECTED

df = None


def get_df():
    global df
    if df is None:
        conn = auth_db(DB_FILE)
        tables = get_tables_of_conn(conn)
        assert len(tables) == 1, "should have only one contact table"

        table_name = tables[0]
        logger.info({"columns": get_table_cols(conn, table_name)})

        rows = list([md5(row[0])] + list(row) for row in
                    conn.execute(f"SELECT {', '.join(CONTACT_COLUMNS_SELECTED)} from {table_name}"))
        df = pd.DataFrame(columns=CONTACT_COLUMNS_DUMPED, data=rows)
        logger.info({"shape": df.shape})
    return df


def get_friend_md5(friend: dict) -> str:
    return friend[FIELD_MD5_NAME]


def get_friend_name(friend: dict) -> str:
    return friend.get("m_nsRemark", friend["nickname"])


def find_friend(name: str) -> Optional[dict]:
    logger.info(f"finding contact of {name}")
    items = get_df().query(
        f" m_nsRemark.str.contains('{name}') or nickname.str.contains('{name}')")  # type: pd.DataFrame
    if len(items) == 0:
        logger.warning(f"not found name of {name}")
        return None
    if len(items) > 1:
        logger.warning(f"cannot decide since it matched {len(items)} choices: ")
        logger.warning(items.values)
        return None
    item = items.iloc[0].to_dict()
    logger.info("found")
    logger.info(item)
    return item


def dump_friends():
    get_df().to_csv("friends-all.csv", encoding="utf-8")


if __name__ == '__main__':
    dump_friends()
