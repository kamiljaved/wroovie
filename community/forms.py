from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.forms import TextInput, Textarea 
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Community

#####~~~~~ FORM ~~~~~#####
# community creation form
class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'title', 'about', 'icon']
        widgets = {
            'name': TextInput(attrs={'placeholder':'Community Name'}),
            'title': TextInput(attrs={'placeholder':'Community Title'}),
            'about': Textarea(attrs={'placeholder':'About the community'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        validate_name = UnicodeUsernameValidator()
        try:
            validate_name(name)
        except ValidationError:
            raise forms.ValidationError("Invalid Name for a Community!")

        if Community.objects.filter(name=name).exists():
            raise forms.ValidationError(f"The community name '{name}' already exists. Please choose another name.")

        # check if the name does not already exists
        return name

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title == '':
            raise forms.ValidationError("The community title cannot be empty.")

        return title

#####~~~~~ FORM ~~~~~#####
# community update form
class CommunityUpdateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['title', 'about', 'icon', 'banner']

        widgets = {
            'title': TextInput(attrs={'placeholder':'A one liner detail for the community'}),
            'about': Textarea(attrs={'placeholder':'About the community'}),
            # 'highlight_color_hex': TextInput(attrs={'placeholder': 'e.g. "4f5567"'})
        }
