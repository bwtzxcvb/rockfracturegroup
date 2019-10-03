from django.contrib import admin

# Register your models here.
from .models import NewsColumn, NewsPost


class NewsColumnAdmin(admin.ModelAdmin):
	list_display = ('column', 'user', 'createdtime')
	list_filter = ("column",)

admin.site.register(NewsColumn, NewsColumnAdmin)
admin.site.register(NewsPost)
