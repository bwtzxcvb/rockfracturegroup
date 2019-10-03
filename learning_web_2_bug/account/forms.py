from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': 'xxx'} ))
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'col-md-3 text-left ','placeholder': 'qqq'}))

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username", "email")
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("password do not match.")
        return cd["password2"]
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder':'可选项'}),
            'birth': forms.TextInput(attrs={'placeholder':'可选项，输入格式为xxxx/xx/xx'}),
            }
        
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
