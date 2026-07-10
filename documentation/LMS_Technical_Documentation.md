# LMS Project — Technical Documentation

**Stack:** Django · PostgreSQL
**Version:** 1.0
**Prepared by:** TEAM IT

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Requirements](#2-system-requirements)
3. [Installation Guide](#3-installation-guide)
4. [Database Setup](#4-database-setup)
5. [API Documentation](#5-api-documentation)
6. [User Manual](#6-user-manual)
7. [Deployment Guide](#7-deployment-guide)
8. [Appendix](#8-appendix)

---

## 1. Project Overview

The LMS (Learning Management System) is a web application built with Django and PostgreSQL that allows institutions to deliver online courses. The platform supports three user roles — **Student**, **Instructor**, and **Admin** — and provides course and lesson management, announcements, and quizzes.

### 1.1 Core Modules

- **Courses** — creation, enrollment, and organization of course content
- **Lessons** — structured content units within a course (text, video, attachments)
- **Announcements** — instructor-to-student broadcast messages per course
- **Quizzes** — timed assessments with auto-graded question types
- **User Roles** — Student, Instructor, and Admin, each with distinct permissions

### 1.2 User Roles Summary

| Role | Key Permissions |
|---|---|
| Student | Enroll in courses, view lessons, post to announcements (read-only), take quizzes, view own grades |
| Instructor | Create/edit own courses, lessons, announcements, and quizzes; grade submissions; manage enrolled students |
| Admin | Full access — manage all users, courses, and site configuration via Django Admin |

---

## 2. System Requirements

### 2.1 Software Requirements

| Component | Minimum Version |
|---|---|
| Python | 3.11+ |
| Django | 5.0+ |
| PostgreSQL | 14+ |
| Django REST Framework | 3.15+ (for API) |
| Node.js (optional, frontend tooling) | 18+ |
| Redis (optional, caching/Celery) | 7+ |
| Web server | Nginx or Apache |
| WSGI/ASGI server | Gunicorn or Daphne |

### 2.2 Hardware Requirements (recommended minimum)

| Environment | CPU | RAM | Storage |
|---|---|---|---|
| Development | 2 cores | 4 GB | 10 GB |
| Production (small) | 2 vCPU | 4 GB | 40 GB SSD |
| Production (medium) | 4 vCPU | 8 GB | 100 GB SSD |

### 2.3 Python Package Dependencies

Key packages listed in `requirements.txt`:

```
Django>=5.0,<5.1
djangorestframework>=3.15
psycopg2-binary>=2.9
django-cors-headers>=4.3
django-filter>=24.1
Pillow>=10.2          # image uploads (avatars, course thumbnails)
python-decouple>=3.8  # environment variable management
gunicorn>=21.2         # production WSGI server
whitenoise>=6.6        # static file serving
```

---

## 3. Installation Guide

### 3.1 Clone the Repository

```bash
git clone https://github.com/team-it/lms-project.git
cd lms-project
```

### 3.2 Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Configure Environment Variables

Create a `.env` file in the project root:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=lms_db
DATABASE_USER=lms_user
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3.5 Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3.6 Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 3.7 Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/` and the Django Admin at `http://127.0.0.1:8000/admin/`.

---

## 4. Database Setup

### 4.1 Creating the PostgreSQL Database

```sql
sudo -u postgres psql
CREATE DATABASE lms_db;
CREATE USER lms_user WITH PASSWORD 'your-password';
ALTER ROLE lms_user SET client_encoding TO 'utf8';
ALTER ROLE lms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE lms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_user;
\q
```

### 4.2 Django Database Configuration

`settings.py` reads database credentials from environment variables:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}
```

### 4.3 Core Data Model (ERD Summary)

| Model | Key Fields | Relationships |
|---|---|---|
| User | email, role, first_name, last_name | extends AbstractUser; role = student/instructor/admin |
| Course | title, description, instructor, is_published | FK → User (instructor); M2M → User (enrolled students) |
| Lesson | title, content, order, course, attachment | FK → Course |
| Announcement | title, message, course, posted_by, created_at | FK → Course, FK → User |
| Quiz | title, course, time_limit, due_date | FK → Course |
| Question | quiz, text, question_type, points | FK → Quiz |
| Choice | question, text, is_correct | FK → Question |
| Submission | quiz, student, score, submitted_at | FK → Quiz, FK → User |

### 4.4 Backups

```bash
# Backup
pg_dump -U lms_user -h localhost lms_db > backup_$(date +%F).sql

# Restore
psql -U lms_user -h localhost lms_db < backup_2026-07-09.sql
```

---

## 5. API Documentation

The API is built with Django REST Framework and uses token/JWT-based authentication. All endpoints are prefixed with `/api/v1/`.

### 5.1 Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register/` | Register a new user (student by default) |
| POST | `/api/v1/auth/login/` | Obtain access and refresh tokens |
| POST | `/api/v1/auth/refresh/` | Refresh an access token |
| POST | `/api/v1/auth/logout/` | Blacklist the refresh token |

### 5.2 Courses

| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/api/v1/courses/` | List all published courses | All |
| POST | `/api/v1/courses/` | Create a new course | Instructor, Admin |
| GET | `/api/v1/courses/{id}/` | Retrieve course detail | All |
| PUT/PATCH | `/api/v1/courses/{id}/` | Update a course | Owner Instructor, Admin |
| DELETE | `/api/v1/courses/{id}/` | Delete a course | Owner Instructor, Admin |
| POST | `/api/v1/courses/{id}/enroll/` | Enroll current user in course | Student |

### 5.3 Lessons

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/courses/{course_id}/lessons/` | List lessons in a course, ordered by sequence |
| POST | `/api/v1/courses/{course_id}/lessons/` | Create a lesson (Instructor of course, Admin) |
| GET | `/api/v1/lessons/{id}/` | Retrieve a single lesson |
| PUT/PATCH | `/api/v1/lessons/{id}/` | Update a lesson |
| DELETE | `/api/v1/lessons/{id}/` | Delete a lesson |

### 5.4 Announcements

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/courses/{course_id}/announcements/` | List announcements for a course |
| POST | `/api/v1/courses/{course_id}/announcements/` | Post an announcement (Instructor, Admin) |
| DELETE | `/api/v1/announcements/{id}/` | Remove an announcement |

### 5.5 Quizzes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/courses/{course_id}/quizzes/` | List quizzes for a course |
| POST | `/api/v1/courses/{course_id}/quizzes/` | Create a quiz with questions (Instructor, Admin) |
| GET | `/api/v1/quizzes/{id}/` | Retrieve quiz with questions (choices hidden from students until submission) |
| POST | `/api/v1/quizzes/{id}/submit/` | Submit answers (Student); auto-graded on save |
| GET | `/api/v1/quizzes/{id}/results/` | View own result (Student) or all results (Instructor, Admin) |

### 5.6 Example Request/Response

`POST /api/v1/courses/{id}/enroll/`

```
// Request headers
Authorization: Bearer <access_token>

// Response 200 OK
{
  "detail": "Enrolled successfully",
  "course_id": 12,
  "student_id": 45
}
```

### 5.7 Error Format

```json
{
  "status": 403,
  "error": "You do not have permission to perform this action."
}
```

---

## 6. User Manual

### 6.1 Student Guide

1. Register an account and log in.
2. Browse the course catalog and click Enroll on a course.
3. Open a course to view its lessons in sequence.
4. Check the Announcements tab for updates from the instructor.
5. Take quizzes before their due date; results appear immediately after submission for auto-graded questions.
6. View grades and progress from the student dashboard.

### 6.2 Instructor Guide

1. Log in and go to "My Courses" to create a new course.
2. Add lessons to the course in the desired order (text, video link, or file attachment).
3. Post announcements to notify enrolled students of updates or deadlines.
4. Build a quiz by adding questions (multiple-choice, true/false, or short answer) and setting a time limit and due date.
5. Review submissions and grades from the course's Gradebook tab.
6. Manage the enrolled student roster from the course settings page.

### 6.3 Admin Guide

1. Access the Django Admin panel at `/admin/`.
2. Manage all user accounts, including changing roles (student, instructor, admin).
3. Approve, edit, or remove any course, lesson, announcement, or quiz on the platform.
4. Monitor site-wide activity logs and manage global settings.

### 6.4 Common Tasks Quick Reference

| Task | Where |
|---|---|
| Reset password | Login page → "Forgot password" |
| Change role of a user | Admin panel → Users |
| Reorder lessons | Course → Lessons → drag handle |
| Extend quiz due date | Course → Quizzes → Edit |
| Export grades | Course → Gradebook → Export CSV |

---

## 7. Deployment Guide

### 7.1 Production Checklist

- Set `DEBUG=False` in environment variables
- Set a strong, unique `SECRET_KEY`
- Configure `ALLOWED_HOSTS` with the production domain
- Use PostgreSQL with a dedicated production database and credentials
- Serve static files via Whitenoise or a CDN (`collectstatic`)
- Enable HTTPS (SSL/TLS certificate, e.g. via Let's Encrypt)
- Set `SECURE_SSL_REDIRECT`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE` to `True`

### 7.2 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7.3 Run with Gunicorn

```bash
gunicorn lms_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### 7.4 Sample Nginx Configuration

```nginx
server {
    listen 80;
    server_name lms.example.com;

    location /static/ {
        alias /var/www/lms/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 7.5 Process Management (systemd example)

```ini
[Unit]
Description=LMS Gunicorn daemon
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/lms
ExecStart=/var/www/lms/venv/bin/gunicorn lms_project.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 7.6 Deployment Steps Summary

1. Push code to the main branch (post code review / GitHub workflow).
2. Pull latest changes on the server: `git pull origin main`
3. Install/update dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Collect static files: `python manage.py collectstatic --noinput`
6. Restart the application service: `sudo systemctl restart lms`
7. Verify the site is up and check logs for errors.

---

## 8. Appendix

### 8.1 Environment Variables Reference

| Variable | Description |
|---|---|
| `DEBUG` | `True` in development, `False` in production |
| `SECRET_KEY` | Django cryptographic signing key |
| `DATABASE_NAME/USER/PASSWORD/HOST/PORT` | PostgreSQL connection settings |
| `ALLOWED_HOSTS` | Comma-separated list of allowed domains |

### 8.2 Revision History

| Version | Date | Notes |
|---|---|---|
| 1.0 | July 2026 | Initial technical documentation |
