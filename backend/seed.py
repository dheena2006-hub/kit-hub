"""Run: python seed.py  — creates admin + pre-stored valid students + staff."""
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kit.settings"); django.setup()
from django.contrib.auth.hashers import make_password
from api import db
import datetime
if not db.users.find_one({"email": "admin@kit.edu"}):
    db.users.insert_one({"name": "Admin", "email": "admin@kit.edu", "password": make_password("Admin@12345"),
        "role": "admin", "status": "approved", "created_at": datetime.datetime.now(datetime.timezone.utc)})
for i in range(1, 6):
    db.valid_students.update_one({"roll_no": f"CS2024{i:02d}"},
        {"$set": {"department": "CSE", "class_name": "III-A"}}, upsert=True)
if not db.staff.count_documents({}):
    db.staff.insert_many([{"name": "Dr. Sample Faculty", "department": "CSE", "designation": "Professor"}])
print("Seeded. Admin: admin@kit.edu / Admin@12345 (change it!)")
