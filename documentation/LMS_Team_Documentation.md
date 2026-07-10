# LMS Project — Team Documentation

**Team:** TEAM IT
**Version:** 1.0

---

## Table of Contents

1. [Member Responsibilities](#1-member-responsibilities)
2. [GitHub Workflow](#2-github-workflow)
3. [Meeting Records](#3-meeting-records)
4. [Timeline / Gantt Chart](#4-timeline--gantt-chart)

---

## 1. Member Responsibilities

> Note: names and role assignments below are placeholders — replace with your actual team roster.

| Name | Role | Responsibilities |
|---|---|---|
| shahida  | Project Lead / Scrum Master | Coordinates sprints, runs stand-ups, tracks progress against timeline, liaises with stakeholders |
| Amna     | Backend Developer (Django) | Models, views, business logic for Courses, Lessons, Quizzes; database migrations |
| Amna     | Backend Developer (API) | REST API endpoints, authentication, permissions, API documentation |
| Ashka    | Frontend Developer | UI templates/pages, student & instructor dashboards, API integration |
| All      | QA / Tester | Writing test cases, manual & automated testing, bug tracking |
| All      | DevOps / Deployment | Server setup, CI/CD, environment configuration, deployment & backups |

### 1.1 Escalation Path

Technical blockers are raised in the team channel first. If unresolved within 24 hours, escalate to the Project Lead for reprioritization or reassignment.

---

## 2. GitHub Workflow

### 2.1 Branching Strategy

The repository follows a simplified Git Flow model:

| Branch                      | Purpose                                                                                                   | Responsible                             |
| --------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `main`                      | Production-ready code only. Protected branch. Only the Team Leader merges after final review and testing. | **Team Leader**                         |
| `develop`                   | Main development branch where completed features are integrated and tested before merging to `main`.      | **Team Leader + All Members**           |
| `feature/authentication`    | User registration, login, role-based authentication, password reset, email verification.                  | **Backend Developer**                   |
| `feature/course-management` | Course CRUD, enrollment, categories, lesson management APIs.                                              | **Backend Developer**                   |
| `feature/quiz-announcement` | Quiz, assignments, announcements, grading features.                                                       | **Backend Developer**                   |
| `feature/database`          | Database schema, ERD updates, migrations, indexing, sample data, query optimization.                      | **Database Developer**                  |
| `feature/frontend-ui`       | Login, registration, dashboards, course pages, responsive UI, API integration.                            | **Frontend Developer**                  |
| `fix/<issue-name>`          | Bug fixes discovered during testing (e.g., `fix/login-validation`, `fix/course-enrollment`).              | **Member who owns the affected module** |
| `release/v1.0`              | Final stabilization branch before project submission, documentation updates, and deployment.              | **Team Leader**                         |


### 2.2 Commit Message Convention

Follow Conventional Commits format:

```
<type>(<scope>): <short description>

| Type       | Purpose                                               |
| ---------- | ----------------------------------------------------- |
| `feat`     | Add a new feature                                     |
| `fix`      | Fix a bug                                             |
| `docs`     | Update documentation                                  |
| `style`    | Formatting changes (no code logic changes)            |
| `refactor` | Improve code without changing functionality           |
| `test`     | Add or update tests                                   |
| `perf`     | Improve performance                                   |
| `chore`    | Maintenance tasks (dependencies, configuration, etc.) |


Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

### 2.3 Pull Request Process

1. Create a `feature/` or `fix/` branch from `develop`.
2. Commit changes with conventional commit messages; push regularly.
3. Open a Pull Request into `develop` with a clear title and description of what changed and why.
4. Link the related issue/task number in the PR description.
5. Request at least one code review before merging.
6. Resolve review comments; ensure CI checks (tests, linting) pass.
7. Squash-merge into `develop` once approved; delete the feature branch.

### 2.4 Code Review Guidelines

- Check for adherence to Django best practices (fat models, thin views)
- Verify migrations are included and reversible
- Confirm new endpoints have permission checks for the correct role(s)
- Look for missing tests on new logic
- Keep feedback constructive and specific

### 2.5 Issue Tracking

Tasks are tracked as GitHub Issues, labeled by type (`bug`, `feature`, `docs`) and priority (`high`, `medium`, `low`), and organized on a Kanban-style Project board with columns: **Backlog → To Do → In Progress → In Review → Done**.

---

## 3. Meeting Records

Standing meeting: weekly team sync. Use the template below for each entry; add new rows as meetings occur.

| Date       | Attendees        | Topics Discussed                                                                                                                 | Action Items                                                                                                                                                                                                                           |
| ---------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-06-20 | All team members | Finalized project idea, client requirements, user roles (Admin, Instructor, Student), technology stack (Django, React, Supabase) | Team Leader: finalize requirements and project plan. Database Developer: draft ER diagram. Backend Developer: set up Django project. Frontend Developer: prepare UI wireframes.                                                        |
| 2026-06-27 | All team members | Reviewed database design, ER diagram, normalization, and API requirements                                                        | Database Developer: complete schema and migrations. Backend Developer: begin authentication APIs. Frontend Developer: design login and registration pages.                                                                             |
| 2026-07-02 | All team members | Progress review on backend and frontend, discussed GitHub workflow and branch management                                         | Backend Developer: implement CRUD APIs. Frontend Developer: integrate authentication UI. Team Leader: manage GitHub branches and review progress.                                                                                      |
| 2026-07-06 | All team members | Reviewed API implementation, database integration, and security requirements                                                     | Backend Developer: add password hashing, input validation, and role-based authorization. Database Developer: optimize database and verify relationships. Frontend Developer: connect APIs to UI.                                       |
| 2026-07-09 | All team members | Discussed deployment, testing strategy, documentation, and project report preparation                                            | Backend Developer: perform API testing with Postman. Frontend Developer: complete responsive UI testing. Database Developer: verify sample data and migrations. Team Leader: compile documentation and prepare presentation materials. |
| 2026-07-10 | All team members | Reviewed remaining tasks, testing checklist, and final submission plan                                                           | All Members: complete integration testing and bug fixing. Team Leader: organize GitHub repository, finalize report, and prepare project demonstration.                                                                                 |


### 3.1 Meeting Notes Format

For detailed minutes, each meeting record should capture:

- Date, time, and attendees (and absentees)
- Agenda items
- Decisions made
- Action items with owner and due date
- Blockers or risks raised

---

## 4. Timeline / Gantt Chart

> Placeholder 8-week project timeline — adjust phase durations and dates to match your actual sprint plan.
| Phase                                                  | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 |
| ------------------------------------------------------ | -- | -- | -- | -- | -- | -- | -- | -- |
| Requirements Gathering & Planning                      | ██ |    |    |    |    |    |    |    |
| System Design (Architecture, UML, Wireframes)          | ██ | ██ |    |    |    |    |    |    |
| Database Design (ERD, Schema, Migrations)              | ██ | ██ |    |    |    |    |    |    |
| Project Setup (GitHub, Django, React, Supabase)        | ██ | ██ |    |    |    |    |    |    |
| Authentication & User Management                       |    | ██ | ██ |    |    |    |    |    |
| Backend Development (Courses, Lessons, Enrollment)     |    |    | ██ | ██ | ██ |    |    |    |
| Backend Development (Announcements, Assignments, Quiz) |    |    |    | ██ | ██ | ██ |    |    |
| API Development & Documentation                        |    |    | ██ | ██ | ██ | ██ |    |    |
| Frontend Development & API Integration                 |    |    |    | ██ | ██ | ██ | ██ |    |
| Security Implementation                                |    |    |    |    | ██ | ██ |    |    |
| Performance Optimization                               |    |    |    |    |    | ██ | ██ |    |
| Testing (Unit, API, Integration, UI, UAT)              |    |    |    |    |    | ██ | ██ | ██ |
| Bug Fixing & Final Review                              |    |    |    |    |    |    | ██ | ██ |
| Deployment (Render, Vercel, Supabase)                  |    |    |    |    |    |    | ██ | ██ |
| Documentation & Report Writing                         | ██ | ██ | ██ | ██ | ██ | ██ | ██ | ██ |
| Final Presentation & Submission                        |    |    |    |    |    |    |    | ██ |


### 4.1 | Milestone                                                     | Target Week |
| ------------------------------------------------------------- | ----------- |
| Project requirements finalized                                | Week 1      |
| SRS and project planning completed                            | Week 1      |
| System architecture, UML diagrams, and wireframes completed   | Week 2      |
| Database schema and ER diagram finalized                      | Week 2      |
| Project setup (GitHub, Django, React, Supabase) completed     | Week 2      |
| Authentication and user management completed                  | Week 3      |
| Core backend modules (Courses, Lessons, Enrollment) completed | Week 4      |
| Announcement, Assignment, and Quiz modules completed          | Week 5      |
| API development and documentation completed                   | Week 5      |
| Frontend integrated with backend APIs                         | Week 6      |
| Security implementation completed                             | Week 6      |
| Performance optimization completed                            | Week 7      |
| System testing (Unit, API, Integration, UI, UAT) completed    | Week 7      |
| Bug fixing and final review completed                         | Week 7      |
| Production deployment (Render, Vercel, Supabase) completed    | Week 8      |
| Documentation and project report completed                    | Week 8      |
| Final presentation and project submission                     | Week 8      |
