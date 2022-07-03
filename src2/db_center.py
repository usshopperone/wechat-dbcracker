import json
import os
from typing import Dict, List

from db import DB
from support.const import DATA_PATH
from support.log import logger


class DBCenter:

    def __init__(self):
        self.dbs: Dict[str, DB] = {}  # file_name: DB
        self.chatsMap: Dict[str, str] = {}  # chat_md5: msg_db_no

    def addDatabase(self, fp, key):
        fn = os.path.basename(fp)
        if fn in self.dbs:
            # logger.warning("database existed: " + fn)
            return
        self.dbs[fn] = DB(fp, key)
        logger.info("added one db: " + fn)

    def addFinish(self):
        # gen chat maps
        for db in self.dbOfMsgs:
            for table_name in db.getAllTableNames():
                # 若不为空，且不等，则报错，以保证唯一性
                assert db.db_name == self.chatsMap.get(table_name, db.db_name)
                self.chatsMap[table_name] = db.db_name

        chatmap_fp = os.path.join(DATA_PATH, "chatmap.json")
        with open(chatmap_fp, "w") as f:
            json.dump(self.chatsMap, f, indent=2, ensure_ascii=False)
            print(f"generated chatmap to {chatmap_fp}")

    @property
    def dbOfContact(self) -> DB:
        return self.dbs["wccontact_new2.db"]

    @property
    def dbOfGroup(self) -> DB:
        return self.dbs["group_new.db"]

    @property
    def dbOfMsgs(self) -> List[DB]:
        return [self.dbs[i] for i in self.dbs if i.startswith("msg")]
