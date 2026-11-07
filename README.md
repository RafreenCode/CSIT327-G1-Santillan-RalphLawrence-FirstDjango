# CampusConnect

**Full name:** Ralph Lawrence Santillan

**Section:** G1

CampusConnect is a Django application with user registration, authentication, and a role-protected dashboard.

## Requirements

- Python 3.15 (verified local environment)
- Django 6.1.2

## Setup

Open PowerShell in the project directory:

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

These commands use the virtual environment directly; activation is not required.

Set a local secret key before starting the application:

```powershell
$env:DJANGO_SECRET_KEY = "replace-this-with-a-local-secret-key"
```

## Initialize the database

Apply the migrations:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Create an administrator account if needed:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Run the development server

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Routes

- `/` - Dashboard
- `/accounts/signup/` - User registration
- `/accounts/login/` - Login
- `/accounts/profile/` - Edit the signed-in user's profile using Django UpdateView
- `/admin_panel/` - Role-protected application admin panel
- `/admin/` - Django administration site

Users must be logged in to access the dashboard. The application admin panel is available to active superusers and users whose role is `ADMIN`. Staff status alone does not grant access to the application admin panel.

## Checks

Run Django's system checks with:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

Run the account and access-control tests with `.\.venv\Scripts\python.exe manage.py test`.

All application pages share a responsive Bootstrap 5 design loaded via CDN (internet access is required for Bootstrap). Registration displays a success message on the login page; profile updates display a confirmation on the profile page. Users can edit their username, name, email, and course; roles and permissions cannot be changed through these forms.

## Lab submission

Before submission, verify sign-up and its Bootstrap success alert, login, profile editing and saved values, logout, and profile login protection. Run the system checks and tests above.

1. Commit and push the final code before the assignment deadline.
2. Confirm the repository is public or shared with the instructor.
3. Submit your full name, section, and repository link at https://forms.gle/bgJn2qMnPkms17DW6.
4. Return to the assignment in Teams and click **Turn in**.

The role-protected admin panel is an additional feature; an admin account is not required for the lab profile and sign-up requirements.
