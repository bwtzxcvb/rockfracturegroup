from django.contrib import admin

# Register your models here.
from .models import ArticleColumn, Comment


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user')
    list_filter = ("column",)
    
admin.site.register(ArticleColumn, ArticleColumnAdmin)
admin.site.register(Comment)
