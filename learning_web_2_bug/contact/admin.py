from django.contrib import admin

# Register your models here.
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'message_subject', 'message_date')
    list_filter = ('message_date', 'name')
    search_fields = ('name', 'message_subject', 'message')

admin.site.register(ContactMessage, ContactMessageAdmin)
