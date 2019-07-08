from django.shortcuts import HttpResponse
from .models import Thesis, Advance, Student, Teacher
from django.utils import timezone


from django.urls import reverse
from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic import DetailView, FormView

from django.shortcuts import render
from .forms import StudentCreationForm
from users.models import CustomUser



def index(request):
    return HttpResponse("Academica index.")

###### Thesis ######


class ThesisList(ListView):
    model = Thesis


class ThesisDetail(DetailView):
    model = Thesis


class ThesisCreation(CreateView):
    model = Thesis
    fields = ['name', 'description', 'period', 'direct',
              'student', 'porcentage', 'state', 'create_date']
    success_url = reverse_lazy('thesis_list')


class ThesisUpdate(UpdateView):
    model = Thesis
    fields = ['name', 'description', 'period',
              'direct', 'student', 'porcentage', 'state']
    success_url = reverse_lazy('thesis_list')


class ThesisDelete(DeleteView):
    model = Thesis
    success_url = reverse_lazy('thesis_list')

###### Advance ######


class AdvanceList(ListView):
    model = Advance

# class AdvanceDetail(DetailView):
#     model = Advance

# class AdvanceCreation(CreateView):
#     model = Advance
#     success_url = reverse_lazy('avance:list')
#     fields = ['name', 'start_date', 'end_date', 'picture']


###### Student ######


class StudentList(ListView):
    model = Student


class StudentCreation(FormView):
    template_name = 'student_form.html'
    form_class = StudentCreationForm
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        data = form.cleaned_data
        user = CustomUser.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            movile=data['movile'],
            address=data['address'],
            birth_date=data['birth_date'],
            cvlac=data['cvlac'],
            password=data['password']
        )
        user.student.cvlacStudent = data['cvlacStudent']
        user.save()

        return HttpResponse('ok')

###### Teacher ######


class TeacherList(ListView):
    model = Teacher