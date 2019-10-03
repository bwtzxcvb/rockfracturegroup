from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
	class Meta:
		model = ContactMessage
		fields = ('name', 'email', 'message_subject', 'message',)
		widgets = {
            'name': forms.TextInput(attrs={'placeholder':'姓名'}),
            'email': forms.TextInput(attrs={'placeholder':'email'}),
            'message_subject': forms.TextInput(attrs={'placeholder':'主题'}),
            'message': forms.TextInput(attrs={'placeholder':'留言'}),
            }
