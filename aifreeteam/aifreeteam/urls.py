"""
URL configuration for aifreeteam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from web.views import get_index,story, career, achievements, contact, post_email, register_email

from blogpost.views import blog, post

from course.views import get_course, courses

from academy.views import academy_main, academy_course_search, academy_course, academy_course_lesson, academy_login, academy_course_class
from academy.views import academy_login_post, academy_account, academy_my_course, academy_logout, api_course_list, academy_course_register

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", get_index),
    path("story/", story),
    path("blog/", blog),
    path("post/<str:slug>/", post),
    path('summernote/', include('django_summernote.urls')),
    path("courses/", courses),
    path("course/<str:slug>/", get_course),
    path("career/", career),
    path("achievements/", achievements),
    path("contact/", contact),
    path("contact_email", post_email),
    path("register_email", register_email),


    path("academy/main/", academy_main),
    path("academy/search/", academy_course_search),
    path("academy/course/<str:slug>/", academy_course),
    path("academy/course/<str:slug>/class/", academy_course_class),
    path("academy/course/<str:slug>/register/", academy_course_register),

    path("academy/course/<str:slug>/<int:progress>/", academy_course_lesson),
    path("academy/course/<str:slug>/<int:progress>/<str:status>/", academy_course_lesson),


    path("academy/login/", academy_login),
    path("academy/login/post", academy_login_post),
    path("academy/logout", academy_logout),

    path("academy/account/", academy_account),
    path("academy/my_course/", academy_my_course),

    path('academy/api/courses/', api_course_list, name='api_course_list'),





]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)