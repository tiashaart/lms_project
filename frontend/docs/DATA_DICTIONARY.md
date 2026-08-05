# HALMS Data Dictionary

## Users Domain

### User
| Field | Description |
|-------|-------------|
| email | Primary login identifier (unique) |
| role | student \| instructor \| admin |
| is_verified | Email verification status |
| avatar | Profile image upload path |

### StudentProfile
| Field | Description |
|-------|-------------|
| student_id | Auto-generated ID (STU-XXXXXXXX) |
| department | Academic department |
| academic_level | e.g., Year 1, Year 2 |

### InstructorProfile
| Field | Description |
|-------|-------------|
| employee_id | Auto-generated ID (INS-XXXXXXXX) |
| specialization | Area of expertise |
| years_of_experience | Teaching experience |

## Courses Domain

### Category
Organizational taxonomy for courses (e.g., Programming, Design).

### Course
| Field | Description |
|-------|-------------|
| status | draft \| published \| archived |
| level | beginner \| intermediate \| advanced |
| is_free | Free course flag (price = 0) |
| max_students | 0 = unlimited enrollment |

### Enrollment
| Field | Description |
|-------|-------------|
| status | active \| completed \| dropped \| suspended |
| progress_percentage | Synced from StudentProgress |

## Learning Content

### Module
Ordered container for lessons within a course.

### Lesson
| Field | Description |
|-------|-------------|
| content_type | video \| pdf \| text \| mixed |
| order | Display sequence within module |
| is_free_preview | Accessible without enrollment |

## Assessment

### Quiz
| Field | Description |
|-------|-------------|
| passing_score | Percentage required to pass (default 60%) |
| max_attempts | Maximum allowed attempts (0 = unlimited) |
| time_limit_minutes | 0 = no time limit |

### Question
| Field | Description |
|-------|-------------|
| question_type | mcq \| true_false \| short_answer |
| correct_answer_text | For short answer auto-grading |

### QuizAttempt
| Field | Description |
|-------|-------------|
| score | Percentage score (0-100) |
| passed | Boolean pass/fail status |

## Assignments

### Assignment
| Field | Description |
|-------|-------------|
| due_date | Submission deadline |
| allow_late_submission | Accept submissions after due date |
| late_penalty_percent | Score deduction for late work |

### AssignmentSubmission
| Field | Description |
|-------|-------------|
| status | draft \| submitted \| graded \| returned \| late |
| feedback | Instructor feedback text |

## Progress

### StudentProgress
| Field | Description |
|-------|-------------|
| completion_percentage | % of published lessons completed |
| quiz_average | Average quiz score for course |
| assignment_average | Average assignment score for course |

## Certificates

### Certificate
| Field | Description |
|-------|-------------|
| certificate_number | Unique ID (HALMS-CERT-XXXXXXXXXXXX) |
| pdf_file | Generated PDF certificate |
| is_valid | Revocation status |

## Payments

### Payment
| Field | Description |
|-------|-------------|
| transaction_id | Unique ID (HALMS-PAY-XXXXXXXXXXXX) |
| payment_method | card \| bank_transfer \| mobile_money \| cash \| free |
| status | pending \| completed \| failed \| refunded \| cancelled |

## Announcements

### Announcement
| Field | Description |
|-------|-------------|
| visibility | all \| students \| instructors \| admins \| course |
| expires_at | Auto-hide after this datetime |
| is_pinned | Pin to top of list |
