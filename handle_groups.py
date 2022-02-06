from typing import Optional

from const import FIELD_MD5_NAME
from utils import auth_db, get_tables_of_conn, md5, logging

conn = auth_db("Group/group_new.db")

tables = get_tables_of_conn(conn)

print(tables)

group_contacts = list(conn.execute("select * from GroupContact"))


logger = logging.getLogger("GROUPS")


def find_group_md5(group_name: str) -> Optional[str]:
    """

    :param group_name:
    :return: wxid_md5 of group
    """

    _group = [i for i in group_contacts if group_name in i[2]]

    if not _group:
        logger.warning(f"not found group of {group_name}")
        return

    if len(_group) > 1:
        logger.warning(f"can't decide group since there are {len(_group)}")
        logger.warning(_group)
        return

    group = _group[0]

    group_md5 = md5(group[0])

    print(group_md5, group)

    return group_md5
