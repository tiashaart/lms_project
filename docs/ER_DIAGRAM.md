# HALMS Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o| StudentProfile : has
    User ||--o| InstructorProfile : has
    User ||--o| AdministratorProfile : has
    User ||--o{ Course : teaches
    User ||--o{ Enrollment : enrolls
    User ||--o{ QuizAttempt : attempts
    User ||--o{ AssignmentSubmission : submits
    User ||--o{ StudentProgress : tracks
    User ||--o{ Certificate : receives
    User ||--o{ Payment : makes
    User ||--o{ Announcement : authors

    Category ||--o{ Course : categorizes

    Course ||--o{ Module : contains
    Course ||--o{ Enrollment : has
    Course ||--o{ Quiz : has
    Course ||--o{ Assignment : has
    Course ||--o{ StudentProgress : tracks
    Course ||--o{ Certificate : awards
    Course ||--o{ Payment : paid_for
    Course ||--o{ Announcement : scoped_to

    Module ||--o{ Lesson : contains
    Module ||--o{ Quiz : optional
    Module ||--o{ Assignment : optional

    Lesson }o--o{ StudentProgress : completed_by

    Quiz ||--o{ Question : contains
    Quiz ||--o{ QuizAttempt : attempted

    Question ||--o{ Choice : has
    Question ||--o{ QuizAnswer : answered

    QuizAttempt ||--o{ QuizAnswer : contains

    Assignment ||--o{ AssignmentSubmission : receives

    Enrollment ||--o| Payment : linked

    User {
        bigint id PK
        string email UK
        string role
        string first_name
        string last_name
        boolean is_active
    }

    Course {
        bigint id PK
        string title
        string slug UK
        bigint category_id FK
        bigint instructor_id FK
        decimal price
        string status
    }

    Enrollment {
        bigint id PK
        bigint student_id FK
        bigint course_id FK
        string status
        decimal progress_percentage
    }

    Module {
        bigint id PK
        bigint course_id FK
        string title
        int order
    }

    Lesson {
        bigint id PK
        bigint module_id FK
        string title
        string content_type
        int order
    }

    Quiz {
        bigint id PK
        bigint course_id FK
        string title
        decimal passing_score
    }

    Question {
        bigint id PK
        bigint quiz_id FK
        string question_type
        int points
    }

    QuizAttempt {
        bigint id PK
        bigint student_id FK
        bigint quiz_id FK
        decimal score
        boolean passed
    }

    Assignment {
        bigint id PK
        bigint course_id FK
        string title
        datetime due_date
    }

    AssignmentSubmission {
        bigint id PK
        bigint assignment_id FK
        bigint student_id FK
        decimal score
        string status
    }

    StudentProgress {
        bigint id PK
        bigint student_id FK
        bigint course_id FK
        decimal completion_percentage
        decimal quiz_average
    }

    Certificate {
        bigint id PK
        bigint student_id FK
        bigint course_id FK
        string certificate_number UK
    }

    Payment {
        bigint id PK
        string transaction_id UK
        bigint student_id FK
        bigint course_id FK
        decimal amount
        string status
    }

    Announcement {
        bigint id PK
        string title
        bigint author_id FK
        string visibility
        datetime expires_at
    }
```

## Key Relationships

1. **User → Profile**: One-to-one based on role (Student/Instructor/Admin)
2. **Course → Module → Lesson**: Hierarchical content structure
3. **Student → Enrollment → Course**: Many-to-many through enrollment
4. **Student → StudentProgress → Course**: Progress tracking per enrollment
5. **Course completion → Certificate**: Auto-generated at 100% progress
6. **Payment → Enrollment**: Payment confirms enrollment for paid courses
