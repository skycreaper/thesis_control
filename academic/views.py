from django.shortcuts import HttpResponse
from .models import Thesis, Advance
from django.utils import timezone


from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)

# Create your views here.
def index(request):
    return HttpResponse("Academica index.")

# Thesis
class ThesisList(ListView):
    model = Thesis

class ThesisDetail(DetailView):
    model = Thesis

class ThesisCreation(CreateView):
    model = Thesis
    # success_url = reverse('thesis:list')
    fields = ['name', 'description', 'period', 'direct', 'student', 'porcentage', 'state']

# class ThesisUpdate(UpdateView):
#     model = Thesis
#     success_url = reverse_lazy('thesis:list')
#     fields = ['name', 'description', 'period', 'direct', 'student', 'porcentage', 'state']

# class ThesisDelete(DeleteView):
#     model = Thesis
#     success_url = reverse_lazy('thesis:list')

# Advance
# class AdvanceList(ListView):
#     model = Advance

# class AdvanceDetail(DetailView):
#     model = Advance

# class AdvanceCreation(CreateView):
#     model = Advance
#     success_url = reverse_lazy('avance:list')
#     fields = ['name', 'start_date', 'end_date', 'picture']