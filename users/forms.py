from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import TextInput 


#####~~~~~ FORM ~~~~~#####
# user+profile registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.count() > 0:
            raise forms.ValidationError("A profile with this email already exists.")
        return email

#####~~~~~ FORM ~~~~~#####
# user update form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

#####~~~~~ FORM ~~~~~#####
# profile update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'banner']
