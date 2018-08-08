from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={'disabled' : 'true'}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'is_active', 'date_joined')
    def clean_password(self):
            return ""