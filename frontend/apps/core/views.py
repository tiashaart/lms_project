from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import mock_data


def _user_context(request):
    user = request.demo_user
    return {
        'user': user,
        'profile': user,
        'unread_count': mock_data.get_unread_notification_count(),
    }


def home(request):
    ctx = {
        'featured_courses': mock_data.get_featured_courses(),
        'instructors': mock_data.INSTRUCTORS,
        'testimonials': mock_data.TESTIMONIALS,
        'stats': mock_data.PLATFORM_STATS,
    }
    return render(request, 'home/index.html', ctx)


def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'student') or 'student'
        request.session['demo_role'] = role
        messages.success(request, 'Welcome back! You are now logged in.')
        return redirect('core:dashboard')
    return render(request, 'authentication/login.html')


def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'student')
        request.session['demo_role'] = role
        messages.success(request, 'Account created successfully!')
        return redirect('core:dashboard')
    return render(request, 'authentication/register.html')


def forgot_password_view(request):
    if request.method == 'POST':
        messages.info(request, 'Password reset link sent to your email (demo).')
        return redirect('core:login')
    return render(request, 'authentication/forgot_password.html')


def reset_password_view(request, token):
    if request.method == 'POST':
        messages.success(request, 'Password reset successfully.')
        return redirect('core:login')
    return render(request, 'authentication/reset_password.html', {'token': token})


def change_password_view(request):
    if request.method == 'POST':
        messages.success(request, 'Password changed successfully.')
        return redirect('core:profile')
    return render(request, 'authentication/change_password.html', _user_context(request))


def logout_view(request):
    if request.method == 'POST':
        request.session.pop('demo_role', None)
        messages.info(request, 'You have been logged out.')
        return redirect('core:home')
    return render(request, 'authentication/logout_confirm.html', _user_context(request))


def dashboard_view(request):
    user = request.demo_user
    ctx = _user_context(request)
    if user.role == 'admin':
        ctx.update(mock_data.ADMIN_DASHBOARD)
        return render(request, 'dashboard/admin_dashboard.html', ctx)
    if user.role == 'instructor':
        ctx.update(mock_data.INSTRUCTOR_DASHBOARD)
        ctx['courses'] = mock_data.COURSES[:3]
        return render(request, 'dashboard/instructor_dashboard.html', ctx)
    ctx.update(mock_data.STUDENT_DASHBOARD)
    ctx['enrolled_courses'] = mock_data.get_enrolled_courses()
    ctx['assignments'] = mock_data.ASSIGNMENTS[:2]
    ctx['certificates'] = mock_data.CERTIFICATES
    return render(request, 'dashboard/student_dashboard.html', ctx)


def profile_view(request):
    return render(request, 'profile/profile.html', _user_context(request))


def profile_edit_view(request):
    if request.method == 'POST':
        messages.success(request, 'Profile updated successfully.')
        return redirect('core:profile')
    return render(request, 'profile/profile_edit.html', _user_context(request))


def course_list_view(request):
    q = request.GET.get('q', '').lower()
    category = request.GET.get('category', '')
    courses = mock_data.COURSES
    if q:
        courses = [c for c in courses if q in c['title'].lower() or q in c['description'].lower()]
    if category:
        courses = [c for c in courses if c['category_slug'] == category]
    page = int(request.GET.get('page', 1))
    ctx = {
        **_user_context(request),
        'courses': courses,
        'page_obj': mock_data.paginate(courses, page),
        'categories': mock_data.CATEGORIES,
        'search_query': request.GET.get('q', ''),
        'selected_category': category,
    }
    return render(request, 'courses/course_list.html', ctx)


def course_detail_view(request, course_id):
    course = mock_data.get_course(course_id)
    if not course:
        return redirect('core:course_list')
    ctx = {**_user_context(request), 'course': course}
    return render(request, 'courses/course_detail.html', ctx)


def category_list_view(request):
    ctx = {**_user_context(request), 'categories': mock_data.CATEGORIES}
    return render(request, 'categories/category_list.html', ctx)


def category_detail_view(request, slug):
    category = mock_data.get_category(slug)
    if not category:
        return redirect('core:category_list')
    ctx = {
        **_user_context(request),
        'category': category,
        'courses': mock_data.get_courses_by_category(slug),
    }
    return render(request, 'categories/category_detail.html', ctx)


def my_courses_view(request):
    ctx = {
        **_user_context(request),
        'enrolled_courses': mock_data.get_enrolled_courses(),
    }
    return render(request, 'enrollments/my_courses.html', ctx)


def enrollment_history_view(request):
    ctx = {**_user_context(request), 'enrollments': mock_data.ENROLLMENTS}
    return render(request, 'enrollments/enrollment_history.html', ctx)


def module_view(request, module_id):
    module = mock_data.get_module(module_id)
    if not module:
        return redirect('core:course_list')
    ctx = {**_user_context(request), 'module': module}
    return render(request, 'lessons/module_view.html', ctx)


def lesson_view(request, lesson_id):
    lesson = mock_data.get_lesson(lesson_id)
    if not lesson:
        return redirect('core:course_list')
    ctx = {**_user_context(request), 'lesson': lesson}
    return render(request, 'lessons/lesson_view.html', ctx)


def assignment_list_view(request):
    ctx = {**_user_context(request), 'assignments': mock_data.ASSIGNMENTS}
    return render(request, 'assignments/assignment_list.html', ctx)


def assignment_detail_view(request, assignment_id):
    assignment = mock_data.get_assignment(assignment_id)
    if not assignment:
        return redirect('core:assignment_list')
    ctx = {**_user_context(request), 'assignment': assignment}
    return render(request, 'assignments/assignment_detail.html', ctx)


def submit_assignment_view(request, assignment_id):
    assignment = mock_data.get_assignment(assignment_id)
    if not assignment:
        return redirect('core:assignment_list')
    if request.method == 'POST':
        messages.success(request, 'Assignment submitted successfully.')
        return redirect('core:assignment_detail', assignment_id=assignment_id)
    ctx = {**_user_context(request), 'assignment': assignment}
    return render(request, 'assignments/submit_assignment.html', ctx)


def assignment_feedback_view(request, assignment_id):
    assignment = mock_data.get_assignment(assignment_id)
    if not assignment:
        return redirect('core:assignment_list')
    ctx = {**_user_context(request), 'assignment': assignment}
    return render(request, 'assignments/assignment_feedback.html', ctx)


def create_assignment_view(request):
    if request.method == 'POST':
        messages.success(request, 'Assignment created successfully.')
        return redirect('core:assignment_list')
    ctx = {**_user_context(request), 'courses': mock_data.COURSES}
    return render(request, 'assignments/create_assignment.html', ctx)


def edit_assignment_view(request, assignment_id):
    assignment = mock_data.get_assignment(assignment_id)
    if not assignment:
        return redirect('core:assignment_list')
    if request.method == 'POST':
        messages.success(request, 'Assignment updated successfully.')
        return redirect('core:assignment_list')
    ctx = {**_user_context(request), 'assignment': assignment, 'courses': mock_data.COURSES}
    return render(request, 'assignments/edit_assignment.html', ctx)


def view_submission_view(request, assignment_id):
    assignment = mock_data.get_assignment(assignment_id)
    submission = mock_data.get_submission(assignment_id)
    if not assignment:
        return redirect('core:assignment_list')
    ctx = {**_user_context(request), 'assignment': assignment, 'submission': submission}
    return render(request, 'assignments/view_submission.html', ctx)


def grade_submission_view(request, assignment_id):
    assignment = mock_data.get_assignment(assignment_id)
    submission = mock_data.get_submission(assignment_id)
    if not assignment:
        return redirect('core:assignment_list')
    if request.method == 'POST':
        messages.success(request, 'Submission graded successfully.')
        return redirect('core:assignment_list')
    ctx = {**_user_context(request), 'assignment': assignment, 'submission': submission}
    return render(request, 'assignments/grade_submission.html', ctx)


def quiz_list_view(request):
    ctx = {**_user_context(request), 'quizzes': mock_data.QUIZZES}
    return render(request, 'quizzes/quiz_list.html', ctx)


def quiz_detail_view(request, quiz_id):
    quiz = mock_data.get_quiz(quiz_id)
    if not quiz:
        return redirect('core:quiz_list')
    ctx = {**_user_context(request), 'quiz': quiz}
    return render(request, 'quizzes/quiz_detail.html', ctx)


def quiz_attempt_view(request, quiz_id):
    quiz = mock_data.get_quiz(quiz_id)
    if not quiz:
        return redirect('core:quiz_list')
    if request.method == 'POST':
        return redirect('core:quiz_result', quiz_id=quiz_id)
    ctx = {**_user_context(request), 'quiz': quiz}
    return render(request, 'quizzes/quiz_attempt.html', ctx)


def quiz_result_view(request, quiz_id):
    quiz = mock_data.get_quiz(quiz_id)
    if not quiz:
        return redirect('core:quiz_list')
    ctx = {
        **_user_context(request),
        'quiz': quiz,
        'score': 85,
        'passed': True,
        'total_questions': len(quiz.get('questions', [])) or quiz['questions_count'],
        'correct_answers': 8,
    }
    return render(request, 'quizzes/quiz_result.html', ctx)


def progress_view(request):
    ctx = {
        **_user_context(request),
        'enrolled_courses': mock_data.get_enrolled_courses(),
        'progress_chart': mock_data.STUDENT_DASHBOARD['progress_chart'],
    }
    return render(request, 'progress/progress_overview.html', ctx)


def certificate_list_view(request):
    ctx = {**_user_context(request), 'certificates': mock_data.CERTIFICATES}
    return render(request, 'certificates/certificate_list.html', ctx)


def certificate_view(request, cert_id):
    cert = mock_data.get_certificate(cert_id)
    if not cert:
        return redirect('core:certificate_list')
    ctx = {**_user_context(request), 'certificate': cert}
    return render(request, 'certificates/certificate_view.html', ctx)


def announcement_list_view(request):
    ctx = {**_user_context(request), 'announcements': mock_data.ANNOUNCEMENTS}
    return render(request, 'announcements/announcement_list.html', ctx)


def announcement_detail_view(request, ann_id):
    announcement = mock_data.get_announcement(ann_id)
    if not announcement:
        return redirect('core:announcement_list')
    ctx = {**_user_context(request), 'announcement': announcement}
    return render(request, 'announcements/announcement_detail.html', ctx)


def notification_list_view(request):
    ctx = {**_user_context(request), 'notifications': mock_data.NOTIFICATIONS}
    return render(request, 'notifications/notifications.html', ctx)


def notification_detail_view(request, notif_id):
    notification = mock_data.get_notification(notif_id)
    if not notification:
        return redirect('core:notification_list')
    ctx = {**_user_context(request), 'notification': notification}
    return render(request, 'notifications/notification_detail.html', ctx)


@require_POST
def mark_notification_read(request, notif_id):
    for n in mock_data.NOTIFICATIONS:
        if n['id'] == notif_id:
            n['read'] = True
            break
    return JsonResponse({'success': True})
