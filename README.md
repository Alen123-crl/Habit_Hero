Habit Hero - Backend

Django REST API for Habit Tracking Application

📋 Overview

Habit Hero backend provides secure APIs for:

User authentication & profile management

Habit creation, tracking, and analytics

Built with Django and Django REST Framework.

🛠 Tech Stack

Python 3.12+

Django 5.2.8

Django REST Framework 3.16.1

djangorestframework-simplejwt 5.5.1 (JWT auth)

Pillow 12.0.0 (image uploads)

SQLite (development)

django-cors-headers 4.9.0 (CORS)

⚡️ Features

User Authentication: Signup, login, JWT token refresh

Profile Management: Update info, upload profile picture, delete account

Habit Management: Create, edit, delete, and list habits

Habit Tracking: Daily/weekly check-ins, history

Analytics: Current/longest streak, success rate, category distribution


🗂 Project Structure
habit_hero/
├── habit_api/
│   ├── models/          # User, Profile, Habit, Check-in models
│   ├── views/           # API views
│   ├── serializers/     # DRF serializers
│   ├── validations/     # Custom validators
│   └── urls.py          # API routes
├── habit_hero/
│   ├── settings.py      # Django settings
│   └── urls.py          # Root URLs
├── media/               # Profile images
├── manage.py
└── requirements.txt

🔌 API Endpoints

Auth

POST /api/signup/ - Register user

POST /api/login/ - Login, get JWT tokens

POST /api/refresh/ - Refresh access token

User

GET /api/user/me/ - Current user profile

PATCH /api/user/me/ - Update profile

DELETE /api/user/me/ - Delete account

Habits

GET /api/habits/ - List habits

POST /api/habits/ - Create habit

PATCH /api/habits/<id>/ - Update habit

DELETE /api/habits/<id>/ - Soft delete habit

Habit Tracking

POST /api/habits/<id>/checkin/ - Add check-in

GET /api/habits/<id>/checkin/ - Check-in history

Analytics

GET /api/habits/<id>/analytics/ - Habit-specific analytics

GET /api/analytics/overview/ - Dashboard analytics

All protected endpoints require JWT in Authorization: Bearer <token>

🚀 Setup

Clone repo

git clone <repo-url>
cd Habit_Hero

Create virtual environment

python -m venv env
# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate


Install dependencies

pip install -r requirements.txt


Run migrations

python manage.py migrate


Create superuser (optional)

python manage.py createsuperuser


Start server

python manage.py runserver


Backend available at http://localhost:8000

🔒 Security

Password hashing with Django

JWT token authentication
