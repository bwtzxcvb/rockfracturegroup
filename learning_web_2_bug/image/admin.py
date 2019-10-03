from django.contrib import admin

# Register your models here.
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'slug', 'description', 'created')

    ordering = ['-created',]
    
admin.site.register(Image,ImageAdmin)
