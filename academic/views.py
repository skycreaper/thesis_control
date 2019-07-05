from django.shortcuts import HttpResponse
from .models import Thesis, Advance, Student, Teacher
from django.utils import timezone


from django.urls import reverse
from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)


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


class StudentCreation(CreateView):
    model = Student
    fields = ['cvlacStudent']
    success_url = reverse_lazy('student_list')

###### Teacher ######


class TeacherList(ListView):
    model = Teacher