KIT Hub backend skeleton

This folder contains a started Django project. I migrated from a lightweight MongoDB-based API to a full Django + PostgreSQL layout.

Next steps to finish backend setup:
- Install requirements: `pip install -r requirements.txt`
- Create PostgreSQL database and set env vars or use `.env`
- Run `python manage.py makemigrations` and `migrate`
- Create a superuser: `python manage.py createsuperuser`
- Seed initial departments and admin users
 - Run the development server: `python manage.py runserver`

Development notes:
- I scaffolded Django apps: `accounts`, `announcements`, `events`, `messaging`, `documents`, `placements`.
- Add these apps to installed apps in `kit/settings.py` (already added).
- Run migrations after creating them.

Files added:
- accounts app with models, serializers, views, urls

Note: The repo still contains a lightweight MongoDB `api/` app kept for reference; new features should be implemented in the Django apps.
