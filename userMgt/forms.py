from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Company

class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()
    company = forms.CharField(max_length=45)
    deparment = forms.CharField(max_length=45)

    class Meta:
        model = User
        fields = [  
                    'username',
                    'email',
                    'password1',
                    'password2',
                    ] 



#user update form for username and email
class UserUpdateForm(forms.ModelForm):

        email = forms.EmailField()

        class Meta:

            model = User

            fields = ['username','email']

#user update form for profile image
class UpdateProfileForm(forms.ModelForm):

    class Meta:

        model = Profile
        fields = ['image','company', ]
