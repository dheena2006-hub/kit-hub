# KIT Hub (Django + DRF + MongoDB + React)
Backend: `cd backend && pip install -r requirements.txt && python seed.py && python manage.py runserver`
Frontend: `cd frontend && npm install && npm run dev`  (proxies /api to :8000)
Needs MongoDB running (MONGO_URI env, default localhost:27017). Set SECRET_KEY in production.
Default admin: admin@kit.edu / Admin@12345 — change immediately. Seeded valid students: CSE / III-A / CS202401..05.
