from django.conf import settings
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os

from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import get_user_roles, assign_role

from .models import Thesis as ThesisModel, Advance as AdvanceModel, Student as StudentModel, Teacher, ThesisState, CommentsThread, Document

from .forms import StudentCreationForm, TeacherCreationForm, ThesisCreationForm, AdvanceCreationForm, CommentaryThesisForm, DocumentForm
from .transactions import RegisterStudentTransaction, UpdateStudent, RegisterAdvance, RegisterTeacherTransaction

from users.models import CustomUser

student_rol = 'student'
teacher_rol = 'teacher'
LOGIN_URL = '/login'

def index(request):
    return HttpResponse("Academica index.")


###### Thesis ######
class Thesis(LoginRequiredMixin, ListView):
    model = ThesisModel
    template_name = "thesis_list.html"

    @login_required
    def register(request):
        template_name = 'academic/thesis_form.html'
        form = ThesisCreationForm(request.POST or None)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.state = ThesisState.objects.get(name="Activo")
            thesis.save()
            return redirect('thesis_list')
        context = {'form': form}
        return render(request, template_name, context)
    
    @login_required(login_url=LOGIN_URL)
    def upload_document(request, thesis_pk):
        template_name="academic/document_thesis/upload.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis_pk)
        form = DocumentForm(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                document = form.save(commit=False)
                document.thesis = thesis
                document.save()
                return redirect('thesis_documents_list', thesis_pk=thesis_pk)
        context = {"form": form}
        return render(request, template_name, context)

    @login_required(login_url=LOGIN_URL)
    def documents_list(request, thesis_pk): 
        template_name="academic/document_thesis/list_by_thesis.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis_pk)
        documents_list = Document.objects.filter(thesis=thesis)
        data = {"thesis":thesis, "documents_list": documents_list}
        return render(request, template_name, data)

    @login_required(login_url=LOGIN_URL)
    def document_viewer(request, document_path):
        filepath = os.path.join(settings.MEDIA_ROOT)
        with open(filepath+'/'+document_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
            return response
        pdf.closed
        
        
        

### CommentThesis ####
class ComentThesis(LoginRequiredMixin, ListView):
    template_name="academic/comments/list_comments.html"

    @login_required
    def register(request, thesis_pk):
        template_name="academic/thesis_commentary.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis_pk)
        form = CommentaryThesisForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.thesis = thesis
                comment.author = CustomUser.objects.get(pk=request.user.pk)
                comment.save()
        context = {"form": form, "thesis": thesis, "comments": CommentsThread.objects.filter(thesis=thesis)}
        return render(request, template_name, context)
    
class ThesisDetail(DetailView):
    model = ThesisModel


class ThesisCreation(CreateView):
    model = ThesisModel
    fields = [
        'name', 'description', 'period', 'direct', 'student', 'porcentage',
        'state', 'create_date'
    ]
    success_url = reverse_lazy('thesis_list')


class ThesisUpdate(UpdateView):
    model = ThesisModel
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
    model = AdvanceModel
    queryset = AdvanceModel.objects.select_related('thesis')
    
class Advance(LoginRequiredMixin, ListView):
    model = AdvanceModel 

    @login_required
    def register_modal(request, thesis):
        template_name="academic/advance_form.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis)
        form = AdvanceCreationForm(request.POST)
        
        context = {'form': form, "thesis": thesis}
        return render(request, template_name, context)

    @csrf_protect
    @login_required
    def register(request):
        if RegisterAdvance(request.POST):
            return redirect("thesis_list")
        return redirect("thesis_list")

    def advance_by_thesis(request, thesis):
        template_name = "student_list.html"
        
# class AdvanceDetail(DetailView):
#     model = Advance

# class AdvanceCreation(CreateView):
#     model = Advance
#     success_url = reverse_lazy('avance:list')
#     fields = ['name', 'start_date', 'end_date', 'picture']

###### Student ######
class Student(LoginRequiredMixin, ListView):
    template_name = "student_list.html"
    queryset = StudentModel.objects.select_related('personal_information')

    # Student register
    @login_required
    def register(request):
        template_name = 'student_form.html'
        form = StudentCreationForm(request.POST or None, request.FILES)
        if form.is_valid():
            if RegisterStudentTransaction(form.data, request.FILES['photo']):
                return redirect('student_list')
        context = {'form': form}
        return render(request, template_name, context)

    #Student disable
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

    #Student edit
    @csrf_protect
    @login_required
    def edit(request, user):
        template = 'edit/student_update_form.html'
        student = get_object_or_404(StudentModel, user=user)
        if request.method == "POST":
            form = StudentCreationForm(request.POST, request.FILES, instance=student)
            try: 
                if form.is_valid():
                    result = UpdateStudent(user, form.data, request.FILES['photo'])
                    if  result:    
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
class TeacherView(LoginRequiredMixin, ListView):
    template_name = "teacher_list.html"
    queryset = Teacher.objects.select_related('personal_information')
    paginate_by = 10

     # Student register
    @login_required
    def register(request):
        template_name = 'teacher_form.html'
        form = TeacherCreationForm(request.POST or None)
        if form.is_valid():
            if RegisterTeacherTransaction(form.data):
                return redirect('teacher_list')
        context = {'form': form}
        return render(request, template_name, context)

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
