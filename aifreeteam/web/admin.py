from django.contrib import admin
from .models import achievement,contact_email, collect_email
# Register your models here.

class achievementsAdmin(admin.ModelAdmin):
	list_display = ("year", "name","award")

admin.site.register(achievement, achievementsAdmin)

class contact_emailsAdmin(admin.ModelAdmin):
	list_display = ("contact_name", "contact_email","contact_phone", "contact_need","contact_date")

admin.site.register(contact_email, contact_emailsAdmin)


class collect_emailsAdmin(admin.ModelAdmin):
	list_display = ("email", "collect_date", "is_subscribed")

admin.site.register(collect_email, collect_emailsAdmin)