# Hope Academy Learning Management System (HALMS)

A production-ready Learning Management System backend built with **Django 5**, **Django REST Framework**, **PostgreSQL**, and **JWT Authentication**.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Framework | Django 5+ |
| API | Django REST Framework |
| Database | PostgreSQL |
| Authentication | Simple JWT |
| Filtering | Django Filters |
| CORS | django-cors-headers |
| Images/Files | Pillow |
| API Docs | drf-spectacular (Swagger/OpenAPI) |
| PDF Certificates | ReportLab |

## Project Structure

```
lms_project/
├── halms/              # Django project settings
├── users/              # User management & RBAC
├── courses/            # Course & enrollment management
├── lessons/            # Modules & lesson content
├── quizzes/            # Quizzes & auto-grading
├── assignments/        # Assignments & submissions
├── progress/           # Student progress tracking
├── certificates/       # Certificate generation
├── payments/           # Payment processing
├── announcements/      # Announcements
├── reports/            # Analytics & reports
├── api/                # API routing & utilities
├── docs/               # Documentation
├── manage.py
├── requirements.txt
└── .env.example
```

## Installation Guide

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- pip / virtualenv

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd lms-project
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

### 3. Create PostgreSQL Database

```sql
CREATE DATABASE halms_db;
CREATE USER halms_user WITH PASSWORD 'halms_password';
ALTER ROLE halms_user SET client_encoding TO 'utf8';
ALTER ROLE halms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE halms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE halms_db TO halms_user;
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

### 7. Access API Documentation

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/
- **Admin Panel:** http://localhost:8000/admin/

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register/` | Register new user |
| POST | `/api/v1/auth/login/` | Login (JWT tokens) |
| POST | `/api/v1/auth/logout/` | Logout (blacklist token) |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| POST | `/api/v1/auth/password-reset/` | Request password reset |
| POST | `/api/v1/auth/password-reset/confirm/` | Confirm password reset |

### Core Resources

| Resource | Base URL |
|----------|----------|
| Users | `/api/v1/users/` |
| Categories | `/api/v1/categories/` |
| Courses | `/api/v1/courses/` |
| Enrollments | `/api/v1/enrollments/` |
| Modules | `/api/v1/modules/` |
| Lessons | `/api/v1/lessons/` |
| Quizzes | `/api/v1/quizzes/` |
| Quiz Attempts | `/api/v1/quiz-attempts/` |
| Assignments | `/api/v1/assignments/` |
| Submissions | `/api/v1/submissions/` |
| Progress | `/api/v1/progress/` |
| Certificates | `/api/v1/certificates/` |
| Payments | `/api/v1/payments/` |
| Announcements | `/api/v1/announcements/` |
| Reports | `/api/v1/reports/` |

### Authentication Header

```
Authorization: Bearer <access_token>
```

## User Roles (RBAC)

| Role | Permissions |
|------|-------------|
| **Student** | Enroll, view courses, submit assignments, take quizzes |
| **Instructor** | Create/manage courses, grade submissions, view reports |
| **Administrator** | Full system access, user management, payments, reports |

## Running Tests

```bash
python manage.py test
```

## Production Deployment Notes

1. Set `DEBUG=False` in `.env`
2. Generate a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
4. Use a production WSGI server (Gunicorn/uWSGI)
5. Serve static/media files via Nginx or cloud storage
6. Enable HTTPS and secure cookie settings

## License

Academic project — Hope Academy Learning Management System.
