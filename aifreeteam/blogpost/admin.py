from django.contrib import admin
from .models import Column,Article
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


class columnsAdmin(admin.ModelAdmin):
	list_display = ("name", "slug","intro", "display")

class article_Admin(SummernoteModelAdmin):
	summernote_fields = ('content',)
	list_display = ("title", "slug","pub_date", "update_time", "author")

admin.site.register(Column, columnsAdmin)
admin.site.register(Article, article_Admin)
