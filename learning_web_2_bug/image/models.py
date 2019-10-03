from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from slugify import slugify
from django.utils import timezone
from article.models import ArticlePost

class Image(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							related_name = "images")
	title = models.OneToOneField(ArticlePost, on_delete=models.CASCADE)
	url = models.URLField()
	slug = models.SlugField(max_length=500, blank=True)
	description =  models.TextField(blank=True)
	created = models.DateField(auto_now_add=True, db_index=True)
	image = models.ImageField(upload_to="images/%Y/%m/%d")
	name = models.CharField(max_length=300)
	
	class Meta:
		ordering = ("-created",)
			
	def __str__(self):
		return self.name
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Image, self).save(*args, **kwargs)
		
