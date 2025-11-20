from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from academy.models import Course, CourseEnrollment, Lesson
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def academy_main(request):
    top_courses = Course.objects.annotate(enroll_count=Count('enrollments')).order_by('-enroll_count')[:3]
    return render(request, 'academy/main.html', locals())

def academy_course_search(request):
    return render(request, 'academy/course_search.html', locals())

def academy_course(request, slug):
    course = Course.objects.annotate(enroll_count=Count('enrollments')).get(slug=slug)
    # 檢查是否已登入 & 是否有報名
    has_enrolled = False
    if request.user.is_authenticated:
        has_enrolled = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, 'academy/course.html', locals())

def academy_course_class(request, slug):
    course = Course.objects.get(slug=slug)
    if request.user.is_authenticated:
        try:
            enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
            num_progress = len(Lesson.objects.filter(chapter__course=course))
            progress = enrollment.progress
            progress = num_progress if progress > num_progress else progress
            return redirect(f'/academy/course/{course.slug}/{progress}/')
        except CourseEnrollment.DoesNotExist:
            enrollment = None
            return redirect(f'/academy/course/{course.slug}')
    # return render(request, 'academy/lesson.html', locals())

@login_required
def academy_course_register(request, slug):
    course = get_object_or_404(Course, slug=slug)

    # 檢查是否已報名
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'has_paid': True, 'progress': 1}
    )

    if not created:
        messages.info(request, "你已經報名過這門課程。")
    else:
        messages.success(request, f"成功報名：{course.title}")

    return redirect(f'/academy/course/{course.slug}')

@login_required
def academy_course_lesson(request, slug, progress, status=None):
    course = Course.objects.get(slug=slug)
    lesson = Lesson.objects.filter(
        chapter__course=course,  # 指定課程
        order=progress           # 指定單元順序
    ).first()

    if status == 'complete':
        user_enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
        user_enrollment.progress = progress
        user_enrollment.save()
    if status == 'complete_all':
        user_enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
        user_enrollment.progress = progress+1
        user_enrollment.save()
        messages.info(request,f"恭喜您，完成【{course.title}】！")
    
    user_progress = CourseEnrollment.objects.get(user=request.user, course=course).progress
    num_progress = len(Lesson.objects.filter(chapter__course=course))

    return render(request, 'academy/lesson.html', locals())

def academy_login(request):
    if request.user.is_authenticated:
        return redirect('/academy/main/')  # 換成你想導向的 URL name
    else:
        return render(request, 'academy/login.html', locals())

@login_required
def academy_logout(request):
    logout(request)
    messages.success(request, "你已成功登出。")
    return redirect('/academy/main/')  # 換成你想導向的 URL name


def academy_login_post(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        # user = authenticate(request, username=username, password=password)
        # print(login(request, user))
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return redirect('/academy/main/')  # 要導向的頁面
        else:
            messages.error(request, '帳號或密碼錯誤')

    return render(request, 'academy/login.html', locals())

@login_required
def academy_account(request):
    return render(request, 'academy/profile.html', locals())

@login_required
def academy_my_course(request):
    enrollments = CourseEnrollment.objects.select_related('course').filter(user=request.user)

    course_progress_data = []
    for enroll in enrollments:
        course = enroll.course
        # 計算總 lessons 數（跨所有章節）
        total_lessons = sum(chapter.lessons.count() for chapter in course.chapters.all())
        progress_count = enroll.progress - 1
        progress_percent = round((progress_count / total_lessons) * 100) if total_lessons > 0 else 0
        # print(progress_percent)

        course_progress_data.append({
            'course': course,
            'progress': progress_percent,
            'enroll': enroll,
        })
    return render(request, 'academy/my_course.html', locals())


### 測試前端用
# from copy import deepcopy
# template = Course.objects.first()
# fake_courses = [deepcopy(template) for _ in range(100)]

def api_course_list(request):
    page = int(request.GET.get('page', 1))
    per_page = 9  # 每次載入 6 筆

    courses = Course.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(courses, per_page)
    page_obj = paginator.get_page(page)

    data = []
    for course in page_obj:
        data.append({
            'title': course.title,
            'subtitle': course.subtitle,
            'category': ','.join([c.slug for c in course.cate.all()]),
            'img': course.img_link,
            'slug': course.slug,
            'price': course.price,
            'instructor': course.instructor,
            'students': course.enrollments.count()
        })

    return JsonResponse({'courses': data, 'has_next': page_obj.has_next()})