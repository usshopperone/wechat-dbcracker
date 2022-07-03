import json
import os
from unittest import TestCase

from support.const import DATA_PATH
from support.find import findEasy
from db_center import DBCenter


class TestWechatDecryptDbs(TestCase):

    def setUp(self) -> None:
        self.wdd = DBCenter()

        with open(os.path.join(DATA_PATH, "dbcracker.log")) as f:
            db_path = db_key = None
            for line in f.readlines():
                if line.startswith("sqlcipher"):
                    db_path = line.split(":", 1)[1].strip()[1:-1]
                elif line.startswith("PRAGMA"):
                    db_key = line.split(";", 1)[0].split("=", 1)[1].strip()[1:-1]
                else:
                    db_path = db_key = None

                if db_path and db_key:
                    self.wdd.addDatabase(db_path, db_key)
            self.wdd.addFinish()

    def test_queryChartHistory(self):
        contact = findEasy(self.wdd, "魔幻", group=True)
        print(contact.queryChatHistory())
