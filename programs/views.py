from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Program, SubProgram, ProgramTask, TaskAdvance

LOGIN_URL = '/login'

class ProgramList(LoginRequiredMixin, ListView):
    model = Program
    template_name= "programs/program_list.html"
    paginate_by = 10
    login_url = LOGIN_URL

class ProgramCreation(LoginRequiredMixin, CreateView):
    model = Program
    template_name = "programs/program_add.html"
    login_url = LOGIN_URL
    fields = ['name', 'start_date', 'end_date']
    success_url = reverse_lazy('program_list')

class ProgramUpdate(LoginRequiredMixin, UpdateView):
    model = Program
    template_name = "programs/program_update.html"
    login_url = LOGIN_URL
    fields = ['name', 'start_date', 'end_date']

class SubProgramList(LoginRequiredMixin, ListView):
    model = SubProgram
    template_name = "programs/subprograms_list.html"
    paginate_by = 10
    login_url = LOGIN_URL



