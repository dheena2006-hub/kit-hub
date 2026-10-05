import csv, io, json, re, datetime
from bson import ObjectId
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .auth import make_token, IsAdmin
from . import db
from .db import ser

now = lambda: datetime.datetime.now(datetime.timezone.utc)
BLOOD = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
open_ = dict(authentication_classes=[], permission_classes=[])

def check_links(d):
    li, pf = str(d.get("linkedin", "")).strip(), str(d.get("portfolio", "")).strip()
    if not re.match(r"^https?://([\w-]+\.)?linkedin\.com/.+", li): return "A valid LinkedIn profile URL is required"
    if pf and not re.match(r"^https?://\S+\.\S+", pf): return "Portfolio must be a valid http(s) URL (or left empty)"

def public(a): return api_view(a)
def noauth(methods):
    def deco(f):
        return authentication_classes([])(permission_classes([])(api_view(methods)(f)))
    return deco

@noauth(["POST"])
def register(r):
    d = r.data; need = ["name", "email", "password", "roll_no", "department", "class_name", "blood_group", "linkedin"]
    if any(not str(d.get(k, "")).strip() for k in need): return Response({"error": "All fields are required"}, 400)
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", d["email"]): return Response({"error": "Invalid email"}, 400)
    if len(d["password"]) < 8: return Response({"error": "Password must be at least 8 characters"}, 400)
    err = check_links(d)
    if err: return Response({"error": err}, 400)
    if d["blood_group"] not in BLOOD: return Response({"error": "Invalid blood group"}, 400)
    ok = db.valid_students.find_one({"roll_no": d["roll_no"].strip(), "department": d["department"].strip(),
                                     "class_name": d["class_name"].strip()})
    if not ok: return Response({"error": "Roll no / department / class not found in college records"}, 400)
    doc = {"name": d["name"].strip(), "email": d["email"].lower().strip(), "password": make_password(d["password"]),
           "role": "student", "roll_no": d["roll_no"].strip(), "department": d["department"].strip(),
           "class_name": d["class_name"].strip(), "blood_group": d["blood_group"], "phone": d.get("phone", ""),
           "linkedin": d["linkedin"].strip(), "portfolio": d.get("portfolio", "").strip(),
           "status": "pending", "created_at": now()}
    try: db.users.insert_one(doc)
    except Exception: return Response({"error": "Email or roll no already registered"}, 409)
    return Response({"message": "Registered. Awaiting admin approval."}, 201)

@noauth(["POST"])
def login(r):
    u = db.users.find_one({"email": str(r.data.get("email", "")).lower().strip()})
    if not u or not check_password(r.data.get("password", ""), u["password"]):
        return Response({"error": "Invalid credentials"}, 401)
    if u["status"] != "approved":
        return Response({"error": f"Account is {u['status']}. Login allowed only after admin approval."}, 403)
    return Response({"token": make_token(u), "user": ser(u)})

@api_view(["GET", "PATCH"])
def me(r):
    if r.method == "PATCH":  # profile page: LinkedIn compulsory, portfolio optional
        d = {"linkedin": r.data.get("linkedin", ""), "portfolio": r.data.get("portfolio", "")}
        err = check_links(d)
        if err: return Response({"error": err}, 400)
        upd = {"linkedin": d["linkedin"].strip(), "portfolio": d["portfolio"].strip()}
        if r.data.get("phone") is not None: upd["phone"] = r.data["phone"]
        db.users.update_one({"_id": r.user["_id"]}, {"$set": upd})
        return Response(ser(db.users.find_one({"_id": r.user["_id"]})))
    return Response(ser(r.user))

@api_view(["GET"])
def export(r):
    fmt = r.GET.get("format", "json"); u = ser(r.user); uid = u["id"]
    msgs = [ser(m) for m in db.messages.find({"$or": [{"from": uid}, {"to": uid}]})]
    data = {"profile": u, "messages": msgs}
    if u["role"] == "admin": data["all_users"] = [ser(x) for x in db.users.find()]
    default = lambda o: o.isoformat() if hasattr(o, "isoformat") else str(o)
    if fmt == "json":
        body, ct = json.dumps(data, indent=2, default=default), "application/json"
    elif fmt == "csv":
        buf = io.StringIO(); w = csv.writer(buf); w.writerow(["section", "key", "value"])
        for k, val in u.items(): w.writerow(["profile", k, default(val)])
        for m in msgs: w.writerow(["message", m["from"] + "->" + m["to"], m["content"]])
        body, ct = buf.getvalue(), "text/csv"
    elif fmt == "pdf":
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=A4); y = 800
        c.setFont("Helvetica-Bold", 14); c.drawString(50, y, "KIT Hub - My Data"); y -= 30; c.setFont("Helvetica", 10)
        lines = [f"{k}: {default(val)}" for k, val in u.items()] + ["", "Messages:"] + \
                [f"{default(m['created_at'])[:16]} {m['content']}" for m in msgs]
        for ln in lines:
            if y < 50: c.showPage(); c.setFont("Helvetica", 10); y = 800
            c.drawString(50, y, ln[:100]); y -= 14
        c.save(); body, ct = buf.getvalue(), "application/pdf"
    else: return Response({"error": "format must be json, csv or pdf"}, 400)
    res = HttpResponse(body, content_type=ct); res["Content-Disposition"] = f'attachment; filename="my_data.{fmt}"'
    return res

@api_view(["GET"])
@permission_classes([IsAdmin])
def admin_users(r):
    q = {"status": r.GET["status"]} if r.GET.get("status") else {}
    return Response([ser(u) for u in db.users.find(q).sort("created_at", -1)])

@api_view(["POST", "DELETE"])
@permission_classes([IsAdmin])
def admin_user(r, uid):
    if r.method == "DELETE":
        db.users.delete_one({"_id": ObjectId(uid), "role": "student"}); return Response(status=204)
    st = {"approve": "approved", "reject": "rejected"}.get(r.data.get("action"))
    if not st: return Response({"error": "action must be approve or reject"}, 400)
    db.users.update_one({"_id": ObjectId(uid), "role": "student"}, {"$set": {"status": st, "reviewed_at": now()}})
    return Response({"status": st})

@api_view(["GET", "POST"])
def announcements_view(r):
    if r.method == "POST":
        if r.user["role"] != "admin": return Response({"error": "Admin only"}, 403)
        db.announcements.insert_one({"title": r.data["title"], "description": r.data["description"],
                                     "author": r.user["name"], "created_at": now()})
        return Response(status=201)
    return Response([ser(a) for a in db.announcements.find().sort("created_at", -1)])

@api_view(["GET"])
def contacts(r):  # students chat with admins, admins chat with students
    other = "student" if r.user["role"] == "admin" else "admin"
    return Response([ser(u) for u in db.users.find({"role": other, "status": "approved"})])

@api_view(["GET", "POST"])
def messages_view(r):
    me_id = str(r.user["_id"])
    if r.method == "POST":
        to = db.users.find_one({"_id": ObjectId(r.data["to"])})
        if not to or to["role"] == r.user["role"]: return Response({"error": "Only student-admin messaging allowed"}, 403)
        db.messages.insert_one({"from": me_id, "to": r.data["to"], "content": r.data["content"], "created_at": now()})
        return Response(status=201)
    o = r.GET.get("with")
    q = {"$or": [{"from": me_id, "to": o}, {"from": o, "to": me_id}]}
    return Response([ser(m) for m in db.messages.find(q).sort("created_at", 1)])

@api_view(["GET"])
def blood(r):
    q = {"status": "approved", "blood_group": r.GET["group"]} if r.GET.get("group") else {"status": "approved"}
    return Response([{"name": u["name"], "department": u["department"], "blood_group": u["blood_group"],
                      "phone": u.get("phone", "")} for u in db.users.find(q) if u["role"] == "student"])

@api_view(["GET"])
def staff_view(r):
    q = {"department": r.GET["department"]} if r.GET.get("department") else {}
    return Response([ser(s) for s in db.staff.find(q)])
