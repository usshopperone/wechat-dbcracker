import os

from db_center import DBCenter
from support.const import DATA_PATH

dbc = DBCenter()

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
            dbc.addDatabase(db_path, db_key)
    dbc.addFinish()

if __name__ == '__main__':
    import argparse

    pass
