import os 
import zipfile

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Program, SubProgram, SubProgramTask, TaskAdvance

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
    fields = ['name', 'description', 'start_date', 'end_date']
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
        for s in data['subprograms']:
            tasks = SubProgramTask.objects.filter(sub_program=s)
            for t in tasks:
                advances = TaskAdvance.objects.filter(task=t)
                acum = sum(advance.percentage for advance in advances)
            try:
                s.acumulate_percentage = int(acum / len(tasks))
            except Exception:
                s.acumulate_percentage = 0
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

class SubProgramUpdate(LoginRequiredMixin, UpdateView):
    model = SubProgram
    template_name = "programs/subprogram/subprogram_update.html"
    fields = ['name', 'description', 'start_date', 'end_date']
    login_url = LOGIN_URL
    success_url = reverse_lazy('sub_program_list')


class SubProgramDetail(LoginRequiredMixin, DetailView):
    model = SubProgram
    template_name = "programs/subprogram/subprogram_detail.html"
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = SubProgramTask.objects.filter(sub_program=kwargs['object'])
        for t in data['task']:
            advances = TaskAdvance.objects.filter(task=t)
            t.acumulate_percentage = sum(advance.percentage for advance in advances)
        return data

class SubProgramTaskList(LoginRequiredMixin, ListView):
    model = SubProgramTask
    template_name = "programs/task/task_list.html"
    paginate_by = 10
    login_url = LOGIN_URL

class SubProgramTaskDetail(LoginRequiredMixin, DetailView):
    model = SubProgramTask
    template_name = "programs/task/task_detail.html"
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['advances'] = TaskAdvance.objects.filter(task=kwargs['object']).order_by('id')
        return data

class SubProgramTaskAdd(LoginRequiredMixin, CreateView):
    model = SubProgramTask
    template_name = "programs/task/task_add.html"
    login_url = LOGIN_URL
    fields = ['name', 'commentary']
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['subprogram'] = SubProgram.objects.get(pk=self.kwargs['subprogram'])
        return data

    def form_valid(self, form):
        form.instance.sub_program = SubProgram.objects.get(pk=self.kwargs['subprogram'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subprogram_detail', kwargs={'pk': self.kwargs["subprogram"]})

class TaskAdvanceDetail(LoginRequiredMixin, DetailView):
    model = TaskAdvance
    template_name = "programs/advance/advance_detail.html"
    login_url = LOGIN_URL

    def download_item(request, document_path):
        file_name, file_extension = os.path.splitext(document_path)
        filepath = os.path.join(settings.MEDIA_ROOT)
        file_extension = file_extension[1:] # removes dot
        
        with open(filepath+'/'+document_path, 'rb') as file:
            response = HttpResponse(file, content_type='file/%s' % file_extension)
            response["Content-Disposition"] = "attachment;filename=%s.%s" % (file_name.split('/')[1], file_extension)
            return response
        
        file.closed
        
class TaskAdvanceAdd(LoginRequiredMixin, CreateView):
    model = TaskAdvance
    template_name = "programs/advance/advance_add.html"
    login_url = LOGIN_URL
    fields = ['commentary', 'advance_file', 'percentage', 'completed' ]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = SubProgramTask.objects.get(pk=self.kwargs['task'])
        advances = TaskAdvance.objects.filter(task=data['task'])
        data['task'].acumulate_percentage = sum(advance.percentage for advance in advances)
        return data

    def form_valid(self, form):
        form.instance.task = SubProgramTask.objects.get(pk=self.kwargs['task'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subprogramtask_detail', kwargs={'pk': self.kwargs['task']})
