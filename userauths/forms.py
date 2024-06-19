from django import forms
from django.contrib.auth.forms import UserCreationForm #handles all the validation
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs={"placeholder":"Username"})
    )
    email = forms.EmailField(
        max_length = 100,
        widget = forms.EmailInput(attrs={"placeholder":"Email"})
    )
    password1 = forms.CharField(
        max_length = 30,
        widget = forms.PasswordInput(attrs={"placeholder":"Password"})
    )
    password2 = forms.CharField(
        max_length = 30,
        widget = forms.PasswordInput(attrs={"placeholder":"Confirm Password"})
    )

    class Meta:
        #User is from userauths.models
        model = User
        fields = ['username', 'email']