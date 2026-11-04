# CampusConnect

CampusConnect is a Django application with user registration, authentication, and a role-protected dashboard.

## Requirements

- Python 3.14 or later
- Django 6.1.2

## Setup

Open PowerShell in the project directory:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Django==6.1.2
```

If PowerShell prevents activation, run the following command once for the current user, then activate the environment again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Set a local secret key before starting the application:

```powershell
$env:DJANGO_SECRET_KEY = "replace-this-with-a-local-secret-key"
```

## Initialize the database

Apply the migrations:

```powershell
python manage.py migrate
```

Create an administrator account if needed:

```powershell
python manage.py createsuperuser
```

## Run the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Routes

- `/` - Dashboard
- `/accounts/signup/` - User registration
- `/accounts/login/` - Login
- `/admin_panel/` - Role-protected application admin panel
- `/admin/` - Django administration site

Users must be logged in to access the dashboard. The application admin panel is available only to users whose role is `ADMIN`.

## Checks

Run Django's system checks with:

```powershell
python manage.py check
```
