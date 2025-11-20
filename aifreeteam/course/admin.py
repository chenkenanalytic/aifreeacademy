from django.contrib import admin
from .models import Category,Lesson
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


class categoriesAdmin(admin.ModelAdmin):
	list_display = ("name", "slug","intro", "display")

class lesson_Admin(SummernoteModelAdmin):
	summernote_fields = ('content',)
	list_display = ("title", "slug","pub_date", "update_time", "author")

admin.site.register(Category, categoriesAdmin)
admin.site.register(Lesson, lesson_Admin)
