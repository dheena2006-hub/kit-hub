from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import Department, User


class Command(BaseCommand):
    help = "Seed database with initial departments and admin users"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create departments
        departments_data = [
            {"department_code": "CSE", "department_name": "Computer Science and Engineering", "hod_name": "Dr. Rajesh Kumar"},
            {"department_code": "ECE", "department_name": "Electronics and Communication Engineering", "hod_name": "Dr. Priya Sharma"},
            {"department_code": "ME", "department_name": "Mechanical Engineering", "hod_name": "Dr. Anil Patel"},
            {"department_code": "CE", "department_name": "Civil Engineering", "hod_name": "Dr. Meera Singh"},
            {"department_code": "EE", "department_name": "Electrical Engineering", "hod_name": "Dr. Vikram Desai"},
        ]

        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                department_code=dept_data["department_code"],
                defaults={
                    "department_name": dept_data["department_name"],
                    "hod_name": dept_data["hod_name"],
                }
            )
            departments[dept_data["department_code"]] = dept
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created department: {dept_data['department_name']}"))

        # Create admin and superadmin users
        admin_users = [
            {
                "name": "College Admin",
                "email": "admin@kit.edu",
                "role": "admin",
                "password": "admin123",
            },
            {
                "name": "Super Admin",
                "email": "superadmin@kit.edu",
                "role": "superadmin",
                "password": "superadmin123",
            },
            {
                "name": "CSE Department Admin",
                "email": "cse_admin@kit.edu",
                "role": "dept_admin",
                "department": departments.get("CSE"),
                "password": "cse_admin123",
            },
            {
                "name": "Test Student",
                "email": "student@kit.edu",
                "roll_no": "2021001",
                "department": departments.get("CSE"),
                "class_name": "4th Semester",
                "year": "2nd Year",
                "phone": "9876543210",
                "role": "student",
                "status": "approved",
                "password": "student123",
            },
        ]

        for user_data in admin_users:
            password = user_data.pop("password")
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    **user_data,
                    "password_hash": make_password(password),
                    "status": "approved",
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created user: {user_data['name']} ({user_data['email']})"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
