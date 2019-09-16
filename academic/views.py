from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import get_user_roles, assign_role

from .models import Thesis, Advance, Student, Teacher, Rol
from .forms import StudentCreationForm, TeacherCreationForm
from .transactions import RegisterStudentTransaction

from users.models import CustomUser

student_rol = 'student'
teacher_rol = 'teacher'

def index(request):
    return HttpResponse("Academica index.")


###### Thesis ######


class ThesisList(ListView):
    model = Thesis


class ThesisDetail(DetailView):
    model = Thesis


class ThesisCreation(CreateView):
    model = Thesis
    fields = [
        'name', 'description', 'period', 'direct', 'student', 'porcentage',
        'state', 'create_date'
    ]
    success_url = reverse_lazy('thesis_list')


class ThesisUpdate(UpdateView):
    model = Thesis
    fields = [
        'name', 'description', 'period', 'direct', 'student', 'porcentage',
        'state'
    ]
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
class Student(LoginRequiredMixin, ListView):
    template_name = "student_list.html"
    queryset = Student.objects.select_related('personal_information')

    # Student register
    def register(request):
        template_name = 'student_form.html'
        form = StudentCreationForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            if RegisterStudentTransaction(form.data):
                return redirect('student_list')
        context = {'form': form}
        return render(request, template_name, context)

    #s Student disable
    @csrf_protect
    @login_required
    def disabledStudent(request):
        if request.method == "POST":
            customUser = get_object_or_404(
                CustomUser, pk=request.POST.get("user"))
            customUser.is_active = False
            customUser.save()
            return HttpResponse("ok", content_type='text/plain')
        return redirect('student_list')
class StudentEdit():
    @csrf_protect
    @login_required
    def edit(request, user):
        template = 'edit/student_update_form.html'
        student = get_object_or_404(Student, user=user)
        if request.method == "POST":
            form = StudentCreationForm(request.POST, instance=student)

            try: 
                if form.is_valid():
                    data = form.cleaned_data
                    custom_user = CustomUser.objects.get(pk=user)
                    custom_user.first_name = data["first_name"]
                    custom_user.last_name = data["last_name"]
                    custom_user.mobile = data["mobile"]
                    custom_user.email = data["email"]
                    custom_user.address = data["address"]
                    custom_user.birth_date = data["birth_date"]
                    custom_user.cvlac = data["cvlac"]
                    custom_user.password = data["password"]
                    student.user = custom_user
                    
                    student = form.save(commit=False)
                    student.save()
                    custom_user.save()
                    
                    return redirect('student_list')
            except Exception as e:
                print("error in StudentEdit(): {}".format(e))
        else:
            form = StudentCreationForm(instance=student)

        context = {
            'form': form,
            'student': student
        }
        return render(request, template, context)

###### Teacher ######
class TeacherList(LoginRequiredMixin, ListView):
    model = Teacher
    paginate_by = 10


class TeacherCreation(LoginRequiredMixin, FormView):
    template_name = 'teacher_form.html'
    form_class = TeacherCreationForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = CustomUser.objects.create_user(first_name=data['first_name'],
                                              last_name=data['last_name'],
                                              email=data['email'],
                                              mobile=data['mobile'],
                                              address=data['address'],
                                              birth_date=data['birth_date'],
                                              cvlac=data['cvlac'],
                                              password=data['password'])
        user.teacher.cvlacTeacher = data['cvlacTeacher']
        user.is_teacher = True
        user.save()
        assign_role(user, teacher_rol)
        return redirect('teacher_list')

class TeacherEdit():
    @csrf_protect
    @login_required
    def edit(request, user):
        template = 'edit/teacher_update_form.html'
        teacher = get_object_or_404(Teacher, user=user)
        if request.method == "POST":
            form = TeacherCreationForm(request.POST, instance=teacher)

            try: 
                if form.is_valid():
                    data = form.cleaned_data
                    custom_user = CustomUser.objects.get(pk=user)
                    custom_user.first_name = data["first_name"]
                    custom_user.last_name = data["last_name"]
                    custom_user.mobile = data["mobile"]
                    custom_user.email = data["email"]
                    custom_user.address = data["address"]
                    custom_user.birth_date = data["birth_date"]
                    custom_user.cvlac = data["cvlac"]
                    custom_user.password = data["password"]
                    teacher.user = custom_user
                    
                    teacher = form.save(commit=False)
                    teacher.save()
                    custom_user.save()
                    
                    return redirect('teacher_list')
            except Exception as e:
                print("error in TeacherEdit(): {}".format(e))
        else:
            form = TeacherCreationForm(instance=teacher)

        context = {
            'form': form,
            'teacher': teacher
        }
        return render(request, template, context)

class TeacherDisable():
    @csrf_protect
    def disabledTeacher(request):
        if request.method == "POST":
            customUser = get_object_or_404(CustomUser, pk=request.POST.get("user"))
            customUser.is_active = False
            customUser.save()
            return HttpResponse("ok",content_type='text/plain')
        return redirect('teacher_list')
