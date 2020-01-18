import os
import io
import xlwt

from django.db.models import Q
from django.conf import settings
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm

from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import get_user_roles, assign_role

from .models import (
    Thesis as ThesisModel, Advance as AdvanceModel, Student as StudentModel,
    Teacher, ThesisState, CommentsThread, Document
)
from .forms import (
    StudentCreationForm, TeacherCreationForm, ThesisCreationForm, AdvanceCreationForm,
    CommentaryThesisForm, DocumentForm
)
from .transactions import RegisterStudentTransaction, UpdateStudent, RegisterAdvance, RegisterTeacherTransaction, UpdateTeacher

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
    paginate_by = 1
    login_url = LOGIN_URL

    def get_queryset(self):
        query = self.request.GET.get('search_text')
        if hasattr(self.request.user, 'student'):
            if query:  # Query tiene un valor
                object_list = self.model.objects.filter(
                    name__icontains=query, student=self.request.user.student)
            elif not query or query is None:  # Query es vació o no existe
                object_list = self.model.objects.filter(
                    student=self.request.user.student)
        elif hasattr(self.request.user, 'teacher'):
            if query:  # Query tiene un valor
                object_list = self.model.objects.filter(Q(name__icontains=query), Q(
                    director=self.request.user.teacher) | Q(co_director=self.request.user.teacher))
            elif not query or query is None:  # Query es vació o no existe
                object_list = self.model.objects.filter(
                    Q(director=self.request.user.teacher) | Q(co_director=self.request.user.teacher))
        else:
            if query:  # Query tiene un valor
                object_list = self.model.objects.filter(name__icontains=query)
            elif not query or query is None:  # Query es vació o no existe
                object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for thesis in context['object_list']:
            advances = AdvanceModel.objects.filter(thesis=thesis)
            total_percentage = sum(advance.percentage for advance in advances)
            thesis.acumulate_percentage = total_percentage
        return context

    @login_required(login_url=LOGIN_URL)
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
        template_name = "academic/document_thesis/upload.html"
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
        template_name = "academic/document_thesis/list_by_thesis.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis_pk)
        documents_list = Document.objects.filter(thesis=thesis)
        data = {"thesis": thesis, "documents_list": documents_list}
        return render(request, template_name, data)

    @login_required(login_url=LOGIN_URL)
    def document_viewer(request, document_path):
        filepath = os.path.join(settings.MEDIA_ROOT)
        with open(filepath+'/'+document_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
            return response
        pdf.closed

### CommentThesis ####


class ComentThesis(LoginRequiredMixin, ListView):
    template_name = "academic/comments/list_comments.html"
    login_url = LOGIN_URL

    @login_required(login_url=LOGIN_URL)
    def register(request, thesis_pk):
        template_name = "academic/thesis_commentary.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis_pk)
        form = CommentaryThesisForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.thesis = thesis
                comment.author = CustomUser.objects.get(pk=request.user.pk)
                comment.save()
        context = {"form": form, "thesis": thesis,
                   "comments": CommentsThread.objects.filter(thesis=thesis).order_by('-submit_date')}
        return render(request, template_name, context)


class ThesisDetail(LoginRequiredMixin, DetailView):
    model = ThesisModel
    template_name = "academic/thesis/thesis_detail.html"
    login_url = LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advance_list'] = AdvanceModel.objects.filter(
            thesis=self.kwargs['pk']).order_by('-creation_date')
        return context


class ThesisCreation(CreateView):
    model = ThesisModel
    fields = [
        'name', 'description', 'director', 'co_director', 'student', 'investigation_line',
        'state', 'publication_date'
    ]
    success_url = reverse_lazy('thesis_list')


class ThesisUpdate(LoginRequiredMixin, UpdateView):
    model = ThesisModel
    template_name = "academic/thesis/thesis_update.html"
    form_class = ThesisCreationForm
    login_url = LOGIN_URL

    def get_success_url(self):
        return reverse_lazy('thesis_detail', kwargs={'pk': self.kwargs["pk"]})


class ThesisDelete(DeleteView):
    model = Thesis
    success_url = reverse_lazy('thesis_list')


###### Advance ######
class AdvanceList(ListView):
    model = AdvanceModel
    queryset = AdvanceModel.objects.select_related('thesis')


class Advance(LoginRequiredMixin, ListView):
    model = AdvanceModel

    @login_required(login_url=LOGIN_URL)
    def register_modal(request, thesis):
        template_name = "academic/advance_form.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis)
        form = AdvanceCreationForm(request.POST)
        actual_advance = sum(
            advance.percentage for advance in AdvanceModel.objects.filter(thesis=thesis))
        context = {'form': form, "thesis": thesis,
                   'actual_advance': actual_advance}
        return render(request, template_name, context)

    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def register(request):
        if RegisterAdvance(request.POST):
            return redirect("thesis_list")
        return redirect("thesis_list")

    @login_required(login_url=LOGIN_URL)
    def advance_by_thesis(request, thesis):
        template_name = "academic/thesis/advance/advance_by_thesis.html"
        thesis = get_object_or_404(ThesisModel, pk=thesis)
        context = {'advance_list': advance_list}
        return render(request, template_name, context)

# class AdvanceDetail(DetailView):
#     model = Advance
#     queryset = StudentModel.objects.select_related('personal_information')

# class AdvanceCreation(CreateView):
#     model = Advance
#     success_url = reverse_lazy('avance:list')
#     fields = ['name', 'start_date', 'end_date', 'picture']

###### Student ######


class Student(LoginRequiredMixin, ListView):
    template_name = "student_list.html"
    paginate_by = 6
    login_url = LOGIN_URL

    def get_queryset(self):
        search_text = self.request.GET.get('search_text')
        if search_text:  # search_text tiene un valor
            object_list = [StudentModel.objects.filter(user__first_name__icontains=value) | StudentModel.objects.filter(
                user__last_name__icontains=value) for value in search_text.split(" ")][0]
        elif not search_text or search_text is None:  # search_text es un texto vació o no existe
            object_list = StudentModel.objects.select_related(
                'personal_information').order_by('user__first_name')
            for _object in object_list:
                _object.institutional_information.short_cvlac = _object.institutional_information.cvlac[0:10] + '...'
        return object_list

    # Student register
    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def register(request):
        template_name = 'student_form.html'
        form = StudentCreationForm(request.POST or None, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                try:
                    photo = request.FILES['photo']
                except:
                    photo = None
                finally:
                    if RegisterStudentTransaction(form.data, photo):
                        messages.success(request, 'Estudiante registrado')
                        return redirect('student_list')
            messages.warning(
                request, 'Parece que hubo un problema, reivsa los errores: ', 'danger')
        context = {'form': form}
        return render(request, template_name, context)

    # Student disable
    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def disabledStudent(request):
        if request.method == "POST":
            customUser = get_object_or_404(
            CustomUser, pk=request.POST.get("user"))
            customUser.is_active = False
            customUser.save()
            return HttpResponse("ok", content_type='text/plain')
        return redirect('student_list')

    # Student edit
    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def edit(request, user):
        template = 'edit/student_update_form.html'
        student = get_object_or_404(StudentModel, user=user)
        if request.method == "POST":
            form = StudentCreationForm(
                request.POST, request.FILES, instance=student)

            if form.is_valid():
                photo = student.personal_information.photo
                if 'photo' in request.FILES:
                    photo = request.FILES['photo']

                result = UpdateStudent(user, form.data, photo)
                if result:
                    messages.success(request, 'Estudiante actualizadó')
                    return redirect('student_list')
                else:
                    messages.warning(
                        request, 'No se pudo actualizar la información', 'danger')
        else:
            form = StudentCreationForm(instance=student)

        context = {
            'form': form,
            'student': student
        }
        return render(request, template, context)

    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def update_password(request, user):
        template_name = 'academic/update_password_form.html'
        user = get_object_or_404(CustomUser, id=user)
        student = get_object_or_404(StudentModel, user=user)
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=user)

            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Contraseña actualizada correctamente')
                return redirect('student_list')
            else:
                messages.warning(request, 'Corrige los errores')

        else:
            form = PasswordChangeForm(user=user)

        context = {'form': form, 'update_user': student}
        return render(request, template_name, context)

###### Teacher ######


class TeacherView(LoginRequiredMixin, ListView):
    template_name = "teacher_list.html"
    paginate_by = 5
    login_url = LOGIN_URL

    def get_queryset(self):
        search_text = self.request.GET.get('search_text')
        if search_text:  # search_text tiene un valor
            object_list = [Teacher.objects.filter(user__first_name__icontains=value) | Teacher.objects.filter(
                user__last_name__icontains=value) for value in search_text.split(" ")][0]
        elif not search_text or search_text is None:  # search_text es un texto vació o no existe
            object_list = Teacher.objects.select_related(
                'personal_information').order_by('user__first_name')
            for _object in object_list:
                _object.institutional_information.short_cvlac = _object.institutional_information.cvlac[0:10] + '...'
        return object_list

     # Teacher register
    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def register(request):
        template_name = 'teacher_form.html'
        form = TeacherCreationForm(request.POST or None, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                try:
                    photo = request.FILES['photo']
                except:
                    photo = None
                finally:
                    if RegisterTeacherTransaction(form.data, photo):
                        messages.success(request, 'Profesor registrado')
                        return redirect('teacher_list')
            messages.warning(
                request, 'Parece que hubo un problema, revisa los errores: ', 'danger')
        context = {'form': form}
        return render(request, template_name, context)

    # Teacher edit
    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def edit(request, user):
        template = 'edit/teacher_update_form.html'
        teacher = get_object_or_404(Teacher, user=user)
        if request.method == "POST":
            form = TeacherCreationForm(
                request.POST, request.FILES, instance=teacher)

            if form.is_valid():
                photo = teacher.personal_information.photo
                if 'photo' in request.FILES:
                    photo = request.FILES['photo']

                result = UpdateTeacher(user, form.data, photo)
                if result:
                    messages.success(request, 'Profesor actualizadó')
                    return redirect('teacher_list')
                else:
                    messages.warning(
                        request, 'No se pudo actualizar la información', 'danger')
        else:
            form = TeacherCreationForm(instance=teacher)

        context = {
            'form': form,
            'teacher': teacher
        }
        return render(request, template, context)

    @csrf_protect
    @login_required(login_url=LOGIN_URL)
    def update_password(request, user):
        template_name = 'academic/update_password_form.html'
        user = get_object_or_404(CustomUser, id=user)
        teacher = get_object_or_404(Teacher, user=user)
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=user)

            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Contraseña actualizada correctamente')
                return redirect('teacher_list')
            else:
                messages.warning(request, 'Corrige los errores')

        else:
            form = PasswordChangeForm(user=user)

        context = {'form': form, 'update_user': teacher}
        return render(request, template_name, context)


class TeacherDisable(LoginRequiredMixin):
    login_url = LOGIN_URL
    @csrf_protect
    def disabledTeacher(request):
        if request.method == "POST":
            customUser = get_object_or_404(
                CustomUser, pk=request.POST.get("user"))
            customUser.is_active = False
            customUser.save()
            return HttpResponse("ok", content_type='text/plain')
        return redirect('teacher_list')

def export(request, data):
    response = HttpResponse(content_type='application/ms-excel')

    if data == 'student':
        response['Content-Disposition'] = 'attachment; filename="estudiantes.xls"'
        rows = StudentModel.objects.all().values_list('user__first_name', 'user__last_name', 'user__email',
                                                      'personal_information__gender__name',
                                                      'personal_information__birth_date', 'personal_information__civil_state__name', 'personal_information__nationality__name',
                                                      'personal_information__address', 'personal_information__mobile',
                                                      'personal_information__health_information__grupo_sanguineo', 'personal_information__health_information__rh',
                                                      'personal_information__health_information__eps', 'institutional_information__cvlac')
    else:
        response['Content-Disposition'] = 'attachment; filename="profesores.xls"'
        rows = Teacher.objects.all().values_list('user__first_name', 'user__last_name', 'user__email',
                                                 'personal_information__gender__name',
                                                 'personal_information__birth_date', 'personal_information__civil_state__name', 'personal_information__nationality__name',
                                                 'personal_information__address', 'personal_information__mobile',
                                                 'personal_information__health_information__grupo_sanguineo', 'personal_information__health_information__rh',
                                                 'personal_information__health_information__eps', 'institutional_information__cvlac')

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nombres', 'Apellidos', 'Correo electrónico', 'Genero', 'Fecha de nacimiento', 'Estado civil',
               'Nacionalidad', 'Dirección', 'Teléfono', 'Grupo sanguíneo', 'RH', 'EPS', 'CVLAC']

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    font_style.num_format_str = 'dd/mm/yyyy'

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response
