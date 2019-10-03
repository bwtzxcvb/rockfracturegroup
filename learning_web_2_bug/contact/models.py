from django.db import models

# Create your models here.

from django.utils import timezone

class ContactMessage(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField()
	message_subject = models.CharField(max_length=300)
	message = models.TextField()
	message_date = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ("-message_date",)
	
	def __str__(self):
		return self.name
