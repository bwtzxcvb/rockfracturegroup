from django import forms
from .models import NewsColumn, NewsPost, NewsTag

class NewsColumnForm(forms.ModelForm):
    class Meta:
        model = NewsColumn
        fields = ('column',)

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ("title", "body") 

class NewsTagForm(forms.ModelForm):
    class Meta:
        model = NewsTag
        fields = ('tag',)
