"""Centralized mock data for Hope Academy LMS demo views."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from types import SimpleNamespace


@dataclass
class DemoUser:
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_authenticated: bool = True
    is_anonymous: bool = False
    bio: str = ''
    phone: str = ''
    avatar: str = 'images/avatar-default.svg'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return self.full_name


USERS = {
    'student': DemoUser(
        id=1, username='ava_student', email='ava@hopeacademy.edu',
        first_name='Ava', last_name='Johnson', role='student',
        bio='Passionate learner focused on design and web development.',
        phone='+1 (555) 012-3456',
    ),
    'instructor': DemoUser(
        id=2, username='marcus_instructor', email='marcus@hopeacademy.edu',
        first_name='Marcus', last_name='Chen', role='instructor',
        bio='Senior UX designer with 10+ years teaching experience.',
        phone='+1 (555) 012-7890',
    ),
    'admin': DemoUser(
        id=3, username='admin', email='admin@hopeacademy.edu',
        first_name='Sarah', last_name='Williams', role='admin',
        bio='Hope Academy platform administrator.',
        phone='+1 (555) 012-1111',
    ),
}

ANONYMOUS_USER = SimpleNamespace(
    id=None, username='', email='', first_name='', last_name='',
    role='', is_authenticated=False, is_anonymous=True,
    full_name='', bio='', phone='', avatar='images/avatar-default.svg',
    get_full_name=lambda: '',
)

CATEGORIES = [
    {'id': 1, 'slug': 'design', 'name': 'Design', 'description': 'UI/UX, graphic design, and visual communication.', 'course_count': 12, 'icon': 'fa-palette'},
    {'id': 2, 'slug': 'development', 'name': 'Development', 'description': 'Web, mobile, and software engineering courses.', 'course_count': 18, 'icon': 'fa-code'},
    {'id': 3, 'slug': 'business', 'name': 'Business', 'description': 'Entrepreneurship, marketing, and leadership.', 'course_count': 9, 'icon': 'fa-briefcase'},
    {'id': 4, 'slug': 'data-science', 'name': 'Data Science', 'description': 'Analytics, machine learning, and data visualization.', 'course_count': 7, 'icon': 'fa-chart-bar'},
]

COURSES = [
    {
        'id': 1, 'title': 'UI/UX Design Foundations', 'slug': 'ui-ux-foundations',
        'category': 'Design', 'category_slug': 'design',
        'instructor': 'Marcus Chen', 'instructor_id': 2,
        'duration': '6 weeks', 'description': 'Master the fundamentals of user interface and experience design with hands-on projects.',
        'image': 'images/course-design.svg', 'progress': 73, 'enrolled': True,
        'lesson_count': 24, 'student_count': 342,
        'modules': [
            {'id': 1, 'title': 'Introduction to UX', 'lesson_count': 6},
            {'id': 2, 'title': 'Wireframing & Prototyping', 'lesson_count': 8},
            {'id': 3, 'title': 'Visual Design Systems', 'lesson_count': 10},
        ],
    },
    {
        'id': 2, 'title': 'Web Development Basics', 'slug': 'web-dev-basics',
        'category': 'Development', 'category_slug': 'development',
        'instructor': 'Elena Rodriguez', 'instructor_id': 4,
        'duration': '8 weeks', 'description': 'Learn HTML, CSS, JavaScript, and build responsive websites from scratch.',
        'image': 'images/course-web.svg', 'progress': 58, 'enrolled': True,
        'lesson_count': 32, 'student_count': 521,
        'modules': [
            {'id': 4, 'title': 'HTML & CSS Fundamentals', 'lesson_count': 10},
            {'id': 5, 'title': 'JavaScript Essentials', 'lesson_count': 12},
            {'id': 6, 'title': 'Building Projects', 'lesson_count': 10},
        ],
    },
    {
        'id': 3, 'title': 'Data Analytics Essentials', 'slug': 'data-analytics',
        'category': 'Data Science', 'category_slug': 'data-science',
        'instructor': 'James Okonkwo', 'instructor_id': 5,
        'duration': '5 weeks', 'description': 'Analyze data with Python, SQL, and visualization tools for actionable insights.',
        'image': 'images/course-data.svg', 'progress': 91, 'enrolled': True,
        'lesson_count': 20, 'student_count': 287,
        'modules': [
            {'id': 7, 'title': 'Data Fundamentals', 'lesson_count': 6},
            {'id': 8, 'title': 'Python for Analytics', 'lesson_count': 8},
            {'id': 9, 'title': 'Visualization & Reporting', 'lesson_count': 6},
        ],
    },
    {
        'id': 4, 'title': 'Digital Marketing Strategy', 'slug': 'digital-marketing',
        'category': 'Business', 'category_slug': 'business',
        'instructor': 'Lisa Park', 'instructor_id': 6,
        'duration': '4 weeks', 'description': 'Develop comprehensive digital marketing campaigns across social and search channels.',
        'image': 'images/course-marketing.svg', 'progress': 0, 'enrolled': False,
        'lesson_count': 16, 'student_count': 198,
        'modules': [
            {'id': 10, 'title': 'Marketing Fundamentals', 'lesson_count': 5},
            {'id': 11, 'title': 'Social Media Strategy', 'lesson_count': 6},
            {'id': 12, 'title': 'Analytics & ROI', 'lesson_count': 5},
        ],
    },
    {
        'id': 5, 'title': 'Python Programming', 'slug': 'python-programming',
        'category': 'Development', 'category_slug': 'development',
        'instructor': 'James Okonkwo', 'instructor_id': 5,
        'duration': '10 weeks', 'description': 'From beginner to intermediate Python with real-world applications.',
        'image': 'images/course-python.svg', 'progress': 0, 'enrolled': False,
        'lesson_count': 40, 'student_count': 612,
        'modules': [],
    },
    {
        'id': 6, 'title': 'Product Management 101', 'slug': 'product-management',
        'category': 'Business', 'category_slug': 'business',
        'instructor': 'Sarah Williams', 'instructor_id': 3,
        'duration': '6 weeks', 'description': 'Learn product lifecycle, roadmapping, and stakeholder management.',
        'image': 'images/course-product.svg', 'progress': 0, 'enrolled': False,
        'lesson_count': 22, 'student_count': 156,
        'modules': [],
    },
]

MODULES = {
    1: {
        'id': 1, 'title': 'Introduction to UX', 'course_id': 1, 'course_title': 'UI/UX Design Foundations',
        'description': 'Understand user-centered design principles and research methods.',
        'lessons': [
            {'id': 1, 'title': 'What is UX Design?', 'duration': '12 min', 'completed': True},
            {'id': 2, 'title': 'User Research Methods', 'duration': '18 min', 'completed': True},
            {'id': 3, 'title': 'Creating Personas', 'duration': '15 min', 'completed': True},
            {'id': 4, 'title': 'User Journey Mapping', 'duration': '20 min', 'completed': False},
            {'id': 5, 'title': 'Usability Testing Basics', 'duration': '22 min', 'completed': False},
            {'id': 6, 'title': 'Module Quiz', 'duration': '10 min', 'completed': False},
        ],
    },
}

LESSONS = {
    1: {
        'id': 1, 'title': 'What is UX Design?', 'module_id': 1, 'module_title': 'Introduction to UX',
        'course_id': 1, 'course_title': 'UI/UX Design Foundations',
        'description': 'An introduction to user experience design and its importance in product development.',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'duration': '12 min', 'completed': True,
        'materials': [
            {'name': 'UX Design Slides.pdf', 'type': 'pdf', 'url': '#'},
            {'name': 'Reading: Don Norman on UX', 'type': 'doc', 'url': '#'},
        ],
        'prev_lesson': None, 'next_lesson': 2,
    },
    2: {
        'id': 2, 'title': 'User Research Methods', 'module_id': 1, 'module_title': 'Introduction to UX',
        'course_id': 1, 'course_title': 'UI/UX Design Foundations',
        'description': 'Learn qualitative and quantitative research techniques for understanding users.',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'duration': '18 min', 'completed': True,
        'materials': [
            {'name': 'Research Template.xlsx', 'type': 'doc', 'url': '#'},
        ],
        'prev_lesson': 1, 'next_lesson': 3,
    },
}

ASSIGNMENTS = [
    {
        'id': 1, 'title': 'Design Critique', 'course': 'UI/UX Design Foundations', 'course_id': 1,
        'due_date': date.today() + timedelta(days=1), 'status': 'pending', 'points': 100,
        'description': 'Analyze an existing app interface and provide a detailed UX critique with improvement recommendations.',
        'instructions': 'Choose any mobile app, document 5 usability issues with screenshots, and propose solutions.',
        'submission_status': None, 'grade': None, 'feedback': None,
    },
    {
        'id': 2, 'title': 'JavaScript Practice', 'course': 'Web Development Basics', 'course_id': 2,
        'due_date': date.today() + timedelta(days=5), 'status': 'submitted', 'points': 50,
        'description': 'Complete the DOM manipulation exercises from Module 2.',
        'instructions': 'Build an interactive todo list using vanilla JavaScript.',
        'submission_status': 'in_review', 'grade': None, 'feedback': None,
    },
    {
        'id': 3, 'title': 'Data Visualization Report', 'course': 'Data Analytics Essentials', 'course_id': 3,
        'due_date': date.today() - timedelta(days=3), 'status': 'graded', 'points': 75,
        'description': 'Create a dashboard visualizing sample sales data.',
        'instructions': 'Use Python matplotlib or a BI tool to create 3 charts with insights.',
        'submission_status': 'graded', 'grade': 88, 'feedback': 'Excellent chart choices. Consider adding trend annotations.',
    },
]

SUBMISSIONS = [
    {
        'id': 1, 'assignment_id': 2, 'student_name': 'Ava Johnson', 'student_id': 1,
        'submitted_at': datetime.now() - timedelta(days=2),
        'content': 'I built an interactive todo list with add, delete, and mark-complete functionality.',
        'file_name': 'todo-app.zip', 'grade': None, 'feedback': None,
    },
]

QUIZZES = [
    {
        'id': 1, 'title': 'UX Fundamentals Quiz', 'course': 'UI/UX Design Foundations', 'course_id': 1,
        'questions_count': 10, 'time_limit': 600, 'passing_score': 70,
        'description': 'Test your knowledge of core UX principles covered in Module 1.',
        'attempted': False, 'score': None,
        'questions': [
            {
                'id': 1, 'text': 'What does UX stand for?',
                'options': ['User Experience', 'Universal Extension', 'Unified Exchange', 'User Extension'],
                'correct': 0,
            },
            {
                'id': 2, 'text': 'Which method is best for understanding user behavior?',
                'options': ['Usability Testing', 'Color Theory', 'Typography', 'Grid Systems'],
                'correct': 0,
            },
            {
                'id': 3, 'text': 'What is a persona in UX design?',
                'options': ['A fictional user profile', 'A color palette', 'A wireframe tool', 'A coding framework'],
                'correct': 0,
            },
        ],
    },
    {
        'id': 2, 'title': 'HTML & CSS Assessment', 'course': 'Web Development Basics', 'course_id': 2,
        'questions_count': 15, 'time_limit': 900, 'passing_score': 75,
        'description': 'Assess your HTML and CSS knowledge from the first two modules.',
        'attempted': True, 'score': 82,
        'questions': [],
    },
]

CERTIFICATES = [
    {
        'id': 1, 'title': 'Data Analytics Essentials', 'course_id': 3,
        'issued_date': date.today() - timedelta(days=30),
        'credential_id': 'HA-CERT-2026-0042',
        'student_name': 'Ava Johnson',
    },
    {
        'id': 2, 'title': 'Introduction to UX', 'course_id': 1,
        'issued_date': date.today() - timedelta(days=60),
        'credential_id': 'HA-CERT-2025-0198',
        'student_name': 'Ava Johnson',
    },
]

ANNOUNCEMENTS = [
    {
        'id': 1, 'title': 'New Course: Python Programming Now Available',
        'content': 'We are excited to announce our new Python Programming course. Enroll now and start your coding journey!',
        'author': 'Sarah Williams', 'created_at': datetime.now() - timedelta(days=2),
        'category': 'New Course',
    },
    {
        'id': 2, 'title': 'Platform Maintenance Scheduled',
        'content': 'Hope Academy LMS will undergo scheduled maintenance on July 10, 2026 from 2:00 AM to 4:00 AM UTC.',
        'author': 'Admin Team', 'created_at': datetime.now() - timedelta(days=5),
        'category': 'System',
    },
    {
        'id': 3, 'title': 'Assignment Deadline Extension',
        'content': 'The Design Critique assignment deadline has been extended by 48 hours for all students.',
        'author': 'Marcus Chen', 'created_at': datetime.now() - timedelta(days=1),
        'category': 'Course Update',
    },
]

NOTIFICATIONS = [
    {
        'id': 1, 'title': 'Assignment Due Tomorrow',
        'message': 'Your Design Critique assignment is due tomorrow. Submit before 11:59 PM.',
        'created_at': datetime.now() - timedelta(hours=3), 'read': False, 'type': 'assignment',
    },
    {
        'id': 2, 'title': 'New Certificate Earned',
        'message': 'Congratulations! You earned a certificate for Data Analytics Essentials.',
        'created_at': datetime.now() - timedelta(days=1), 'read': False, 'type': 'certificate',
    },
    {
        'id': 3, 'title': 'Quiz Available',
        'message': 'UX Fundamentals Quiz is now available for Module 1.',
        'created_at': datetime.now() - timedelta(days=2), 'read': True, 'type': 'quiz',
    },
    {
        'id': 4, 'title': 'Course Update',
        'message': 'New lessons added to Web Development Basics - Module 2.',
        'created_at': datetime.now() - timedelta(days=3), 'read': True, 'type': 'course',
    },
]

INSTRUCTORS = [
    {'id': 2, 'name': 'Marcus Chen', 'title': 'Senior UX Designer', 'courses': 4, 'students': 1200, 'avatar': 'images/instructor-1.svg'},
    {'id': 4, 'name': 'Elena Rodriguez', 'title': 'Full-Stack Developer', 'courses': 3, 'students': 890, 'avatar': 'images/instructor-2.svg'},
    {'id': 5, 'name': 'James Okonkwo', 'title': 'Data Scientist', 'courses': 2, 'students': 650, 'avatar': 'images/instructor-3.svg'},
]

TESTIMONIALS = [
    {'name': 'Emily R.', 'role': 'Student', 'text': 'Hope Academy transformed my career. The courses are practical and the instructors are incredibly supportive.', 'rating': 5},
    {'name': 'David K.', 'role': 'Student', 'text': 'The progress tracking and certificates helped me land my first design job within 6 months.', 'rating': 5},
    {'name': 'Maria S.', 'role': 'Instructor', 'text': 'Teaching on Hope Academy has been rewarding. The platform makes it easy to engage with students.', 'rating': 5},
]

ENROLLMENTS = [
    {'id': 1, 'course_id': 1, 'course_title': 'UI/UX Design Foundations', 'enrolled_date': date.today() - timedelta(days=45), 'status': 'active', 'progress': 73},
    {'id': 2, 'course_id': 2, 'course_title': 'Web Development Basics', 'enrolled_date': date.today() - timedelta(days=30), 'status': 'active', 'progress': 58},
    {'id': 3, 'course_id': 3, 'course_title': 'Data Analytics Essentials', 'enrolled_date': date.today() - timedelta(days=60), 'status': 'completed', 'progress': 100},
    {'id': 4, 'course_id': 4, 'course_title': 'Digital Marketing Strategy', 'enrolled_date': date.today() - timedelta(days=90), 'status': 'dropped', 'progress': 15},
]

PLATFORM_STATS = {
    'courses': 100, 'students': 12000, 'instructors': 45, 'certificates': 8500,
}

STUDENT_DASHBOARD = {
    'courses_enrolled': 8, 'courses_completed': 3, 'pending_assignments': 4, 'certificates_earned': 2,
    'progress_chart': {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [20, 35, 45, 55, 68, 82],
    },
    'recent_activity': [
        {'action': 'Completed lesson', 'detail': 'User Research Methods', 'time': '2 hours ago'},
        {'action': 'Submitted assignment', 'detail': 'JavaScript Practice', 'time': '1 day ago'},
        {'action': 'Earned certificate', 'detail': 'Data Analytics Essentials', 'time': '3 days ago'},
    ],
}

INSTRUCTOR_DASHBOARD = {
    'courses_created': 4, 'total_students': 342, 'pending_reviews': 12, 'avg_rating': 4.8,
    'performance_chart': {
        'labels': ['UI/UX', 'Design Systems', 'Prototyping', 'Research'],
        'data': [92, 88, 85, 90],
    },
    'recent_activity': [
        {'action': 'New submission', 'detail': 'Design Critique from Ava Johnson', 'time': '1 hour ago'},
        {'action': 'Student enrolled', 'detail': 'Web Development Basics', 'time': '3 hours ago'},
        {'action': 'Quiz completed', 'detail': 'UX Fundamentals - avg score 78%', 'time': '1 day ago'},
    ],
}

ADMIN_DASHBOARD = {
    'total_users': 12450, 'total_students': 11200, 'total_instructors': 45, 'total_courses': 100,
    'total_enrollments': 28500, 'revenue': 125000,
    'user_chart': {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [8500, 9200, 10100, 10800, 11500, 12450],
    },
    'enrollment_chart': {
        'labels': ['Design', 'Development', 'Business', 'Data Science'],
        'data': [35, 40, 15, 10],
    },
    'system_activity': [
        {'user': 'Ava Johnson', 'action': 'Enrolled in course', 'target': 'Python Programming', 'time': '5 min ago'},
        {'user': 'Marcus Chen', 'action': 'Created assignment', 'target': 'Design Critique', 'time': '1 hour ago'},
        {'user': 'Sarah Williams', 'action': 'Published announcement', 'target': 'Platform Maintenance', 'time': '2 hours ago'},
        {'user': 'James Okonkwo', 'action': 'Updated course', 'target': 'Data Analytics Essentials', 'time': '4 hours ago'},
    ],
}


def get_user(role='student'):
    return USERS.get(role, USERS['student'])


def get_course(course_id):
    return next((c for c in COURSES if c['id'] == course_id), None)


def get_category(slug):
    return next((c for c in CATEGORIES if c['slug'] == slug), None)


def get_courses_by_category(slug):
    return [c for c in COURSES if c['category_slug'] == slug]


def get_module(module_id):
    return MODULES.get(module_id)


def get_lesson(lesson_id):
    return LESSONS.get(lesson_id)


def get_assignment(assignment_id):
    return next((a for a in ASSIGNMENTS if a['id'] == assignment_id), None)


def get_quiz(quiz_id):
    return next((q for q in QUIZZES if q['id'] == quiz_id), None)


def get_certificate(cert_id):
    return next((c for c in CERTIFICATES if c['id'] == cert_id), None)


def get_announcement(ann_id):
    return next((a for a in ANNOUNCEMENTS if a['id'] == ann_id), None)


def get_notification(notif_id):
    return next((n for n in NOTIFICATIONS if n['id'] == notif_id), None)


def get_submission(assignment_id):
    return next((s for s in SUBMISSIONS if s['assignment_id'] == assignment_id), None)


def get_enrolled_courses():
    return [c for c in COURSES if c.get('enrolled')]


def get_featured_courses():
    return COURSES[:3]


def get_unread_notification_count():
    return sum(1 for n in NOTIFICATIONS if not n['read'])


def paginate(items, page=1, per_page=6):
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]
    total_pages = max(1, (total + per_page - 1) // per_page)
    return SimpleNamespace(
        object_list=page_items,
        number=page,
        paginator=SimpleNamespace(num_pages=total_pages, count=total),
        has_previous=page > 1,
        has_next=page < total_pages,
        previous_page_number=page - 1,
        next_page_number=page + 1,
    )
