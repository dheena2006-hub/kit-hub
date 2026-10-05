from pymongo import MongoClient
from django.conf import settings
db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB]
users, valid_students, announcements = db.users, db.valid_students, db.announcements
messages, staff = db.messages, db.staff
users.create_index("email", unique=True)
users.create_index("roll_no", unique=True, sparse=True)
def ser(d):
    if d is None: return None
    d = dict(d); d["id"] = str(d.pop("_id")); d.pop("password", None)
    return d
