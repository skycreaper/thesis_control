from users.models import CustomUser
from django.db import transaction
from django import forms
from .models import Student, Gender, Nationality, CivilState#, Rol
# class BoundField:
#     def label_tag(self, contents=None, attrs=None, label_suffix=None):


class StudentCreationForm(forms.ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), initial={'field1': Gender.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_gender'})
                    )

    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all(), initial={'field1': Nationality.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_nationality'})
                    )
    
    civil_state = forms.ModelChoiceField(queryset=CivilState.objects.all(), initial={'field1': CivilState.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_civilState'})
                    )
    # rol = forms.CharField(widget=forms.HiddenInput(), initial=Rol.objects.get(name="Estudiante").id, required=False)
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password')

class TeacherCreationForm(forms.ModelForm):
    cvlacTeacher = forms.CharField(required=False)

    # class Meta:
    #     model = CustomUser
    #     fields = ('first_name', 'last_name', 'mobile', 'email',
    #               'address', 'birth_date', 'cvlac', 'password')
