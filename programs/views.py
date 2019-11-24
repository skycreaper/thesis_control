from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Program, SubProgram, ProgramTask, TaskAdvance

LOGIN_URL = '/login'

class ProgramList(LoginRequiredMixin, ListView):
    model = Program
    template_name= "programs/program/program_list.html"
    paginate_by = 10
    login_url = LOGIN_URL

class ProgramCreation(LoginRequiredMixin, CreateView):
    model = Program
    template_name = "programs/program/program_add.html"
    login_url = LOGIN_URL
    fields = ['name', 'start_date', 'end_date']
    success_url = reverse_lazy('program_list')

class ProgramUpdate(LoginRequiredMixin, UpdateView):
    model = Program
    template_name = "programs/program/program_update.html"
    login_url = LOGIN_URL
    fields = ['name', 'description', 'start_date', 'end_date']
    success_url = reverse_lazy('program_list')

class ProgramDetail(LoginRequiredMixin, DetailView):
    model = Program
    template_name = "programs/program/program_detail.html"
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['subprograms'] = SubProgram.objects.filter(program=kwargs['object'])
        return data

class SubProgramList(LoginRequiredMixin, ListView):
    model = SubProgram
    template_name = "programs/subprogram/subprograms_list.html"
    paginate_by = 10
    login_url = LOGIN_URL

class SubprogramCreation(LoginRequiredMixin, CreateView):
    model = SubProgram
    template_name = "programs/subprogram/subprogram_add.html"
    fields = ['name', 'description', 'start_date', 'end_date']
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['program'] = Program.objects.get(pk=self.kwargs['program'])
        return data
    
    def form_valid(self, form):
        form.instance.program = Program.objects.get(pk=self.kwargs['program'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('program_detail', kwargs={'pk': self.kwargs["program"]})



