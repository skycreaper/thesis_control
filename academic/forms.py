from users.models import CustomUser
from django.db import transaction
from django import forms

# class BoundField:
#     def label_tag(self, contents=None, attrs=None, label_suffix=None):


class StudentCreationForm(forms.ModelForm):
    attrs = {"class": "form-control"}

    # cvlacStudent = forms.CharField(label="Código del CvLAC", max_length=50, required=True, widget=forms.TextInput(attrs))
    # first_name = forms.CharField(label="Nombre", max_length=50, required=True, widget=forms.TextInput(attrs))
    # last_name = forms.CharField(label="Apellido", max_length=50, required=False, widget=forms.TextInput(attrs))
    # mobile = forms.CharField(label="Celular", max_length=13, required=False, widget=forms.TextInput(attrs))
    # email = forms.CharField(label="Correo electrónico institucional", max_length=50, required=True, widget=forms.TextInput(attrs))
    # address = forms.CharField(label="Dirección", max_length=50, required=False, widget=forms.TextInput(attrs))
    # birth_date = forms.DateField(label="Fecha de Nacimiento", required=True)
    # cvlac = forms.CharField(label="CvLAC", max_length=50, required=False, widget=forms.TextInput(attrs))
    # password = forms.CharField(label="Contraseña", max_length=28, required=True, widget=forms.TextInput(attrs))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'mobile', 'email', 'address', 'birth_date', 'cvlac' ,'password')


class TeacherCreationForm(forms.ModelForm):
    cvlacTeacher = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'mobile', 'email', 'address', 'birth_date', 'cvlac' ,'password')
