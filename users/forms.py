from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple
from .widgets import CustomPictureImageField
class Userform(forms.ModelForm):
    username=forms.CharField(disabled=True)
    class Meta:
        model=User
        fields={'first_name','last_name','username'}
        
class ProfileForm(forms.ModelForm):
    Photo=forms.ImageField(widget=CustomPictureImageField)
    class Meta:
        model=Profile
        fields={'Photo','bio','phone_number'}

