from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Pdf
from article.models import ArticlePost

class PdfForm(forms.ModelForm):
	class Meta:
		model = Pdf
		fields = ('name', 'url', 'description')
	
	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['pdf',]
		extension = url.rsplit('.', 1)[1].lower()
		if extension not in valid_extensions:
			raise forms.ValidationError("not match")
		return url
	
	def save(self, force_insert=False, force_update=False, commit=True):
		pdf = super(PdfForm, self).save(commit=False)
		pdf_url = self.cleaned_data['url']
		pdf_name = '{0}.{1}'.format(slugify(pdf.name),pdf_url.rsplit('.', 1)[1].lower())
		response = request.urlopen(pdf_url)
		pdf.pdf.save(pdf_name, ContentFile(response.read()), save=False)
		if commit:
			pdf.save()
		
		return pdf
