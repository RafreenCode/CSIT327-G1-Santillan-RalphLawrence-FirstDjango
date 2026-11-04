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
- `/accounts/profile/` - Edit the signed-in user's profile using Django UpdateView
- `/admin_panel/` - Role-protected application admin panel
- `/admin/` - Django administration site

Users must be logged in to access the dashboard. The application admin panel is available to active superusers and users whose role is `ADMIN`. Staff status alone does not grant access to the application admin panel.

## Checks

Run Django's system checks with:

```powershell
python manage.py check
```

Run the account and access-control tests with `python manage.py test`.

All application pages share a responsive Bootstrap 5 design loaded via CDN (internet access is required for Bootstrap). Registration displays a success message on the login page; profile updates display a confirmation on the profile page. Users can edit their username, name, email, and course; roles and permissions cannot be changed through these forms.

## Lab submission

Submit your GitHub repository link and a two-minute demo video. In the demo, show sign-up and its success message, login, profile editing, and the role-protected admin panel. Create a superuser with `createsuperuser`, or set an application's administrator role to `ADMIN`, to access the application admin panel.
