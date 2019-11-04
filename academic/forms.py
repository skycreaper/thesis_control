from users.models import CustomUser
from django.db import transaction
from django import forms
from .models import Student, Gender, Nationality, CivilState, Thesis, Teacher, InvestigationLine, Advance, CommentsThread, Document, Period

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

    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'nationality', 'civil_state', 'photo')

class TeacherCreationForm(forms.ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), initial={'field1': Gender.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_gender'})
                    )

    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all(), initial={'field1': Nationality.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_nationality'})
                    )
    
    civil_state = forms.ModelChoiceField(queryset=CivilState.objects.all(), initial={'field1': CivilState.pk},
                       widget=forms.Select(attrs={'class':'form-control', 'id':'id_civilState'})
                    )

    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'nationality', 'civil_state', 'photo')

class ThesisCreationForm(forms.ModelForm):
    director = forms.ModelChoiceField(queryset=Teacher.objects.all(), initial={'field1': Teacher.pk},
                       widget=forms.Select(attrs={'class':'form-control selector', 'id':'id_director'})
                    )

    student = forms.ModelChoiceField(queryset=Student.objects.all(), initial={'field1': Student.pk},
                       widget=forms.Select(attrs={'class':'form-control selector', 'id':'id_student'})
                    )
    co_director = forms.ModelChoiceField(queryset=Teacher.objects.all(), initial={'field1': Teacher.pk},
                       widget=forms.Select(attrs={'class':'form-control selector', 'id':'id_co_director'})
                    )
    investigation_line = forms.ModelChoiceField(queryset=InvestigationLine.objects.all(), initial={'field1': InvestigationLine.pk},
                        widget=forms.Select(attrs={'class':'form-control selector', 'id':'id_investigation_line'})
                    ) 
    class Meta:
        model = Thesis
        fields = ('name', 'description', "director", "co_director", "investigation_line", "student", "publication_date")
    

class AdvanceCreationForm(forms.ModelForm):
    period = forms.ModelChoiceField(queryset=Period.objects.filter(active=True), initial={'field1': Period.pk},
                        widget=forms.Select(attrs={'class':'form-control selector', 'id':'id_period'})
                    ) 
    class Meta:
        model = Advance
        fields = ("thesis","description", "percentage", "period", "observation")
    
    def __init__(self, *args, **kwargs):
        super(AdvanceCreationForm, self).__init__(*args, **kwargs)

class CommentaryThesisForm(forms.ModelForm):
    class Meta:
        model = CommentsThread
        fields = ("comment",)

class DocumentForm(forms.ModelForm):
    document_file = forms.FileField(required=True)
    
    class Meta:
        model = Document
        fields = ("document_file", "title", "description")