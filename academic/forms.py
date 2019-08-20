from users.models import CustomUser
from django.db import transaction
from django import forms

# class BoundField:
#     def label_tag(self, contents=None, attrs=None, label_suffix=None):


class StudentCreationForm(forms.ModelForm):
    attrs = {"class": "form-control"}
    
    cvlacStudent = forms.CharField()
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'mobile', 'email', 'address', 'birth_date', 'cvlac' ,'password')


class TeacherCreationForm(forms.ModelForm):
    cvlacTeacher = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'mobile', 'email', 'address', 'birth_date', 'cvlac' ,'password')
