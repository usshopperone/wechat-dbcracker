from typing import List

from support.interface import IContact
from support.utils import cursor2dictList, getMsgKeyFromWxid

from db import DB
from db_center import DBCenter


class Contact:

    def __init__(self, data: IContact, wdd: DBCenter):
        self._data = data
        self._wdd = wdd

    @property
    def wxid(self) -> str:
        return self._data["m_nsUsrName"]

    @property
    def msgDbName(self) -> str:
        """
        数据库的名字（文件位置）
        :return:
        """
        return self._wdd.chatsMap[self._chatsKey]

    @property
    def _msgDb(self) -> DB:
        return self._wdd.dbs[self.msgDbName]

    @property
    def _chatsKey(self) -> str:
        """
        聊天记录的表名，每张表对应一个好友、群的聊天记录
        :return:
        """
        return getMsgKeyFromWxid(self.wxid)

    def queryChatHistory(self) -> List[dict]:
        """
        :return: 聊天记录
        """
        return cursor2dictList(self._msgDb.conn.execute(f"select * from {self._chatsKey}"))
