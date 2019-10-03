from django import forms
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag

class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body","article_writer",) 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)