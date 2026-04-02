🎓 Learning Management System (LMS)

🚀 A full-stack Learning Management System built using **Django (Backend)** and **React (Frontend)** that enables students and teachers to manage courses, lessons, and assignments efficiently.

🌐 Live Demo

👉 Frontend: 
👉 Backend API: 
👉 Admin Panel: /admin

📸 Screenshots

🏠 Dashboard



📚 Courses Page



🎥 Lesson View


 📌 Project Overview

This LMS platform provides a complete digital learning environment:

👨‍🏫 Teachers can:
Create courses
Upload lessons
Assign assignments
Evaluate submissions

👨‍🎓 Students can:
Enroll in courses
Watch lessons
Submit assignments
Track progress

🚀 Key Features

👤 Authentication System
User registration (Student / Teacher)
JWT-based login system
Role-based access control

📚 Course Management

Create / update / delete courses (Teacher only)
View all courses (Students)
Course detail view with lessons

🎥 Lesson System

Video-based learning content
Organized by course structure

🎓 Enrollment System

Students can enroll in courses
Track enrolled courses

📝 Assignment System
Teacher creates assignments
Student submissions
Submission tracking

🔐 Security Features
Protected routes
Token authentication
Role-based permissions

🛠️ Tech Stack
Backend
Python 🐍
Django 🌐
Django REST Framework (DRF)

Frontend
HTMl
CSS
JavaScript

Database
SQLite (Development)
PostgreSQL (Production Ready)

📂 Project Architecture

```bash id="final001"
lms_project/
├── manage.py
├── apps/
│   ├── users/
│   ├── courses/
│   ├── lessons/
│   ├── enrollments/
│   ├── assignments/
│   └── submissions/
├── core/
├── media/
├── static/
├── templates/
├── docs/
└── db/
```

⚙️ Installation Guide
1️⃣ Clone Repository

```bash id="final002"
git clone https://github.com/tiashaart/lms_project.git
cd lms-project
```

2️⃣ Backend Setup

```bash id="final003"
python -m venv venv
source venv/bin/activate
```

```bash id="final004"
pip install -r requirements.txt
```

```bash id="final005"
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


3️⃣ Frontend Setup

```bash id="final006"
cd frontend
npm install
npm start
```

🔐 API Endpoints

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| POST   | /api/register/     | User registration |
| POST   | /api/login/        | Login             |
| GET    | /api/courses/      | List courses      |
| POST   | /api/courses/      | Create course     |
| GET    | /api/courses/{id}/ | Course details    |
| POST   | /api/enroll/       | Enroll in course  |
| POST   | /api/assignments/  | Create assignment |


👥 Team Members

| Role                                   | Member    |
| -------------------------------------- | --------- |
| 👑 Database                             | Member 1 |
| ⚙️ Backend Developer                   | Member 2  |
| 🎨 Frontend Developer                  | Member 3  |

 📊 Project Status

🟢 Active Development
🟡 Testing Phase
🔵 Completed (update when finished)

🧠 System Design Highlights

Modular Django apps architecture
RESTful API design
Role-based authentication system
Scalable and clean folder structure
Separation of frontend & backend

---

# 🧪 Testing Strategy

* Unit testing (backend APIs)
* Manual UI testing
* Postman API testing
* Integration testing (frontend + backend)

---

# 🚀 Deployment (Future Plan)

* Backend: Render / Railway / AWS
* Frontend: Vercel / Netlify
* Database: PostgreSQL Cloud

---

# 📌 Future Improvements

* 🔴 Live video classes integration
* 🔔 Notification system
* 📱 Mobile app (React Native)
* 📊 Analytics dashboard
* 💬 Chat system between students & teachers

---

# 📄 License

This project is developed for **educational purposes only**.

---

# ⭐ Acknowledgements

Thanks to mentors, teammates, and open-source tools that supported this project.

---

# 🏁 Final Note

This project demonstrates:

* Real-world full-stack development
* Team collaboration workflow
* Scalable backend architecture
* Production-ready design thinking
