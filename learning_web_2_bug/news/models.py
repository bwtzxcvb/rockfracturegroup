from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from slugify import slugify
from django.utils import timezone
from django.urls import reverse


class NewsColumn(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							 related_name = 'news_column')
	column = models.CharField(max_length=200)
	createdtime = models.DateField(auto_now_add=True)
	
	def __str__(self):
		return self.column
		
class NewsTag(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							related_name = 'news_alltag')
	tag =  models.CharField(max_length=200)
	
	def __str__(self):
		return self.tag

class NewsPost(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							related_name='news')
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)
	column = models.ForeignKey(NewsColumn, on_delete=models.CASCADE,
							   related_name = 'news_column')
	body = models.TextField()
	createtime = models.DateTimeField(default=timezone.now)
	updatetime = models.DateTimeField(auto_now=True)
	likes = models.PositiveIntegerField(default=0)
	news_tag = models.ManyToManyField(NewsTag, related_name="news_tag",blank=True)

	
	class Meta:
		ordering = ("-createtime",)
		index_together = (("id", "slug"),)
		
	def __str__(self):
		return self.title
	
	def save(self,*args,**kargs):
		self.slug = slugify(self.title)
		super(NewsPost,self).save(*args,**kargs)
	

