from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect, HttpResponseRedirect

from django.contrib.auth import (
    login as do_login, logout as do_logout,
    authenticate, update_session_auth_hash
)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from academic.transactions import UpdateTeacher, UpdateStudent

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/edit_profile.html'

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if hasattr(self.object, 'student'):
            if UpdateStudent(kwargs["pk"], request.POST, self.object.student.personal_information.photo) is None:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            if UpdateTeacher(kwargs["pk"], request.POST, self.object.teacher.personal_information.photo) is None:
                return self.render_to_response(self.get_context_data(form=form))

        super().post(request, *args, **kwargs)
        return self.form_valid(self.get_form())

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.kwargs["pk"]})

    def get_form(self, form=None):
        if hasattr(self.object, 'student'):
            form = self.form_class(initial=
                {   
                    'gender': self.object.student.personal_information.gender.pk,
                    'civil_state': self.object.student.personal_information.civil_state.pk,
                    'nationality': self.object.student.personal_information.nationality.pk
                })
        else:
            form = self.form_class(initial=
                {   
                    'gender': self.object.teacher.personal_information.gender.pk,
                    'civil_state': self.object.teacher.personal_information.civil_state.pk,
                    'nationality': self.object.teacher.personal_information.nationality.pk
                })
        return form

    @csrf_protect
    @login_required(login_url=login_url) 
    def update_password(request):
        template_name = 'academic/update_password_form.html'
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('home')
        else:
            form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, template_name, context)

class ProfileDetail(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = CustomUser
    template_name = "users/profile.html"

def login(request):
    form = AuthenticationForm
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return redirect('home')
        else:
            print("login errors: ", form.errors)
    return render(request, "registration/login.html", {'form':form})


def logout(request):
    do_logout(request)
    return redirect("login")