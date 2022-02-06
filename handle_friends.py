from typing import List, Optional

import pandas as pd

from utils import md5, get_tables_of_conn, get_table_cols, auth_db, logging
from const import FIELD_MD5_NAME

logger = logging.getLogger("CONTACTS")

DB_FILE = "Contact/wccontact_new2.db"

# {'columns': [
# '_packed_WCContactData',
# -> 'm_nsAliasName',
# 'm_nsBrandIconUrl', 'm_nsChatRoomAdminList', 'm_nsChatRoomDesc', 'm_nsChatRoomMemList',
# 'm_nsDraft', 'm_nsEncodeUserName', 'm_nsFullPY', 'm_nsGoogleContactName',
# 'm_nsHeadHDImgUrl'(big image), 'm_nsHeadHDMd5'(null), 'm_nsHeadImgUrl'(small image), 'm_nsImgStatus',
# -> 'm_nsRemark', 'm_nsRemarkPYFull', 'm_nsRemarkPYShort',
# 'm_nsShortPY',
# -> 'm_nsUsrName'(wxid),
# 'm_patSuffix',
# 'm_uiCertificationFlag',
# 'm_uiChatRoomMaxCount', 'm_uiChatRoomStatus', 'm_uiChatRoomVersion',
# 'm_uiConType', 'm_uiImgKey',
# 'm_uiSex'(0: female, 1: male, 2: unknown),
# 'm_uiType'(cannot understand what does it mean, according to the data),
# -> 'nickname',
# 'openIMInfo'
# ]}
CONTACT_COLUMNS_SELECTED = ["m_nsUsrName", "nickname", "m_nsRemark", "m_nsAliasName", "m_uiSex",
                            "m_nsHeadHDImgUrl"]
CONTACT_COLUMNS_DUMPED = [FIELD_MD5_NAME] + CONTACT_COLUMNS_SELECTED

conn = auth_db(DB_FILE)
tables = get_tables_of_conn(conn)
assert len(tables) == 1, "should have only one contact table"

table_name = tables[0]
logger.info({"columns": get_table_cols(conn, table_name)})

rows = list([md5(row[0])] + list(row) for row in
            conn.execute(f"SELECT {', '.join(CONTACT_COLUMNS_SELECTED)} from {table_name}"))
df = pd.DataFrame(columns=CONTACT_COLUMNS_DUMPED, data=rows)
logger.info({"shape": df.shape})


def find_friend_md5(name: str) -> Optional[dict]:
    logger.info(f"finding contact of {name}")
    items = df.query(f" m_nsRemark.str.contains('{name}') or nickname.str.contains('{name}')")  # type: pd.DataFrame
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
    return item[FIELD_MD5_NAME]


def dump_friends():
    df.to_csv("friends-all.csv", encoding="utf-8")


if __name__ == '__main__':
    dump_friends()
