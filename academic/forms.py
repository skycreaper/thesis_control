from users.models import CustomUser
from django.db import transaction


from django import forms

class StudentCreationForm(forms.ModelForm):
    cvlacStudent = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'movile', 'email', 'address', 'birth_date', 'cvlac' ,'password')

    # sin resultado
    @transaction.atomic
    def save(self):
        customUser = super().save(commit=False)
        customUser.is_student = True
        customUser.save()
        student = Student.objects.create(user=user)
        return customUser