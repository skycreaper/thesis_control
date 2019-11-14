from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, 'student'):
            if UpdateStudent(kwargs["pk"], request.POST, self.object.student.personal_information.photo) is None:
                print("error al actualizar")
                return self.render_to_response(self.get_context_data(form=form))
        else:
            if UpdateTeacher(kwargs["pk"], request.POST, self.object.teacher.personal_information.photo) is None:
                return self.render_to_response(self.get_context_data(form=form))
        return super().post(request, *args, **kwargs)

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