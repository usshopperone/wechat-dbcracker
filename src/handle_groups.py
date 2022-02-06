from typing import Optional

from utils import auth_db, get_tables_of_conn, md5, logger

'''
a group sample:
(
'23331802985@chatroom', 
0, 
'樱花三结义 - 拿下AI', 
'yinghuasanjieyi - naxiaAI', 
None, 
'', 
'', 
'', 
0, 
0, 
2050, 
'IMG_HAS', 
0, 
'http://wx.qlogo.cn/mmcrhead/znjWj2aXw2hV3soCK2oOjbIOpe6sd1viciblvcePJo8jMbpHibVQHA3JYFYkjtibEIsS7UPpia7Rq0q19N0LXeibGLp4d9icW/0', 
'', 
'', 
'wxid_ck85xup8b1bj21;wxid_k2gcdm9ecl3122;wxid_bza7ffi93oc222', 
None, 
1, 
None, 
None, 
'', 
None, 
'', 
'v3_020b3826fd03010000000000a33336f783ea16000000501ea9a3dba12f95f6b60a0536a1adb6be22eda2096c077b53e5c79a1c567959c597040839824daf5667b210b0262cd0458db8ad0a30aa82c4ad31b8d0e0a45dba55ac01fc7db5830000f35e56@stranger', 
700000019, 
500, 
None, 
b'\xb0\x01\x00\xb8\x01\x00\xc0\x01\x00\xd0\x01\x00\xea\x01\x00\xf2\x01\x00\xfa\x01\x00\x82\x02\x00\x8a\x02\x06IMG_NO\x92\x02\x00\x98\x02\x00\xa2\x02\x00\xaa\x02\x00\xb0\x02\x00\xc2\x02\x13wxid_ck85xup8b1bj21\xc8\x02\x00\xd2\x02\x010\xd8\x02\x00\xe2\x02\x00\xea\x02\x00\xf2\x02\x00\xf8\x02\x00\x8a\x03\xb7\x02<RoomData><Member UserName="wxid_k2gcdm9ecl3122"><Flag>0</Flag></Member><Member UserName="wxid_bza7ffi93oc222"><Flag>1</Flag><DisplayName>\xe6\x9c\xac\xe7\xbe\xa4\xe5\x94\xaf\xe4\xb8\x80\xe6\x8c\x87\xe5\xae\x9a\xe8\x8f\x9c\xe9\xb8\xa1</DisplayName></Member><Member UserName="wxid_ck85xup8b1bj21"><Flag>16</Flag></Member><MaxCount>500</MaxCount><Version>700000019</Version></RoomData>\x98\x03\x00\xa0\x03\x00\xa8\x03\xf5\x90\xfb\x8f\x06\xb2\x03\x00\xba\x03\x00\xc2\x03\x00\xca\x03\x00\xf8\x03\x80\x80 ', 
None
)
'''


groups = None


def get_groups():
    global groups
    if groups is None:
        conn = auth_db("Group/group_new.db")

        tables = get_tables_of_conn(conn)

        print(tables)

        groups = list(conn.execute("select * from GroupContact"))

    return groups


def get_group_md5(group: dict) -> str:
    return md5(group[0])


def get_group_name(group: dict) -> str:
    return group[2]


def find_group(group_name: str) -> Optional[dict]:
    """

    :param group_name:
    :return: wxid_md5 of group
    """

    _group = [i for i in get_groups() if group_name in i[2]]

    if not _group:
        logger.warning(f"not found group of {group_name}")
        return

    if len(_group) > 1:
        logger.warning(f"can't decide group since there are {len(_group)}")
        logger.warning(_group)
        return

    group = _group[0]
    logger.info(f"found group: {group}")
    return group
