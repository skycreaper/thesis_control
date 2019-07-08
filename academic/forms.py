#from django.contrib.auth.models import CustomUser
from users.models import CustomUser

from django import forms

class StudentCreationForm(forms.ModelForm):
    cvlacStudent = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'movile', 'email', 'address', 'birth_date', 'cvlac' ,'password')