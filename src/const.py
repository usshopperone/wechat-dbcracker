import os

FIELD_MD5_NAME = "md5"

PROJECT_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(os.path.dirname(PROJECT_DIR), "data")

DB_CRACK_PATH = os.path.join(DATA_DIR, "db-crack.json")

DB_FILES = (
    "Account/Beta.db",
    "ChatSync/ChatSync.db",
    "Contact/wccontact_new2.db",
    "Favorites/favorites.db",
    "FileStateSync/filestatesync.db",
    "Group/group_new.db",
    "MMLive/live_main.db",
    "Message/fileMsg.db",
    "Message/fts/ftsmessage.db",
    "Message/msg_0.db",
    "Message/msg_1.db",
    "Message/msg_2.db",
    "Message/msg_3.db",
    "Message/msg_4.db",
    "Message/msg_5.db",
    "Message/msg_6.db",
    "Message/msg_7.db",
    "Message/msg_8.db",
    "Message/msg_9.db",
    "Message/plaintext.db",
    "RevokeMsg/revokemsg.db",
    "Session/session_new.db",
    "Stickers/stickers.db",
    "Sync/openim_oplog.db",
    "Sync/oplog_1.1.db",
    "solitaire/solitaire_chat.db",
    "voip/multiTalk/multiTalk.db"
)
