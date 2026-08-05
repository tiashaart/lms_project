# HALMS PostgreSQL Schema

This document describes the database schema for Hope Academy LMS.

## Entity Relationship Overview

See [ER_DIAGRAM.md](./ER_DIAGRAM.md) for the visual diagram.

## Tables

### users_user
Custom user table with email-based authentication and RBAC.

| Column | Type | Constraints |
|--------|------|-------------|
| id | BIGSERIAL | PRIMARY KEY |
| email | VARCHAR(254) | UNIQUE, NOT NULL |
| password | VARCHAR(128) | NOT NULL |
| first_name | VARCHAR(150) | |
| last_name | VARCHAR(150) | |
| role | VARCHAR(20) | NOT NULL, INDEX |
| phone | VARCHAR(20) | |
| avatar | VARCHAR(100) | |
| bio | TEXT | |
| date_of_birth | DATE | |
| is_verified | BOOLEAN | DEFAULT FALSE |
| is_active | BOOLEAN | DEFAULT TRUE |
| is_staff | BOOLEAN | DEFAULT FALSE |
| is_superuser | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

**Indexes:** `(email)`, `(role, is_active)`

### users_student_profile / users_instructor_profile / users_administrator_profile
Role-specific profile extensions (OneToOne → users_user, CASCADE DELETE).

### courses_category
| Column | Type | Constraints |
|--------|------|-------------|
| id | BIGSERIAL | PRIMARY KEY |
| name | VARCHAR(100) | UNIQUE |
| slug | VARCHAR(120) | UNIQUE |

### courses_course
| Column | Type | Constraints |
|--------|------|-------------|
| id | BIGSERIAL | PRIMARY KEY |
| title | VARCHAR(200) | NOT NULL |
| slug | VARCHAR(220) | UNIQUE |
| category_id | BIGINT | FK → courses_category (SET NULL) |
| instructor_id | BIGINT | FK → users_user (CASCADE) |
| status | VARCHAR(20) | INDEX |
| price | DECIMAL(10,2) | DEFAULT 0.00 |

**Indexes:** `(status, category_id)`, `(instructor_id, status)`, `(slug)`

### courses_enrollment
| Column | Type | Constraints |
|--------|------|-------------|
| id | BIGSERIAL | PRIMARY KEY |
| student_id | BIGINT | FK → users_user (CASCADE) |
| course_id | BIGINT | FK → courses_course (CASCADE) |
| status | VARCHAR(20) | INDEX |
| progress_percentage | DECIMAL(5,2) | CHECK 0-100 |

**Unique:** `(student_id, course_id)`

### lessons_module / lessons_lesson
Module groups lessons within a course. CASCADE DELETE from course.

### quizzes_quiz / quizzes_question / quizzes_choice / quizzes_attempt / quizzes_answer
Quiz hierarchy with attempt tracking and auto-grading support.

### assignments_assignment / assignments_submission
Assignment with file upload and instructor grading. CASCADE DELETE from course.

### progress_student_progress
Tracks completion %, quiz/assignment averages. M2M to completed lessons.

### certificates_certificate
Auto-generated on 100% completion. Unique certificate_number.

### payments_payment
Transaction records linked to enrollments.

### announcements_announcement
Role-based visibility with expiry dates.

## Cascade Delete Rules

| Parent | Child | On Delete |
|--------|-------|-----------|
| User | StudentProfile | CASCADE |
| User | Course (instructor) | CASCADE |
| User | Enrollment | CASCADE |
| Course | Module | CASCADE |
| Module | Lesson | CASCADE |
| Course | Quiz | CASCADE |
| Quiz | Question | CASCADE |
| Question | Choice | CASCADE |
| Course | Assignment | CASCADE |
| Assignment | Submission | CASCADE |

## Sample SQL (PostgreSQL)

```sql
-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Performance indexes (created by Django migrations)
CREATE INDEX IF NOT EXISTS idx_enrollment_student_status
    ON courses_enrollment (student_id, status);

CREATE INDEX IF NOT EXISTS idx_payment_transaction
    ON payments_payment (transaction_id);

CREATE INDEX IF NOT EXISTS idx_certificate_number
    ON certificates_certificate (certificate_number);
```

## Migration Commands

```bash
python manage.py makemigrations users courses lessons quizzes assignments progress certificates payments announcements
python manage.py migrate
python manage.py sqlmigrate <app> <migration_number>  # View generated SQL
```
