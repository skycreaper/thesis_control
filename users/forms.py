from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from academic.models import Gender, CivilState, Nationality


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
# class CustomUserChangeForm(forms.ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), initial=Gender.pk,
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_gender'})
                    )

    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all(), initial={'field1': Nationality.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_nationality'})
                    )

    civil_state = forms.ModelChoiceField(queryset=CivilState.objects.all(), initial={'field1': CivilState.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_civilState'})
                    )

    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name')
