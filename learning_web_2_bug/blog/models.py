from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

    
class BlogArticles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="blog_posts")
    title = models.CharField(max_length=300)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    avatar_thumbnail = ProcessedImageField(upload_to='avatars', processors=[ResizeToFill(825,550)], format='JPEG', options={'quality':60})    
    
    class Meta:
        ordering = ("-publish",)
        
    def __str__(self):
        return self.title
    
