from django.urls import path
from django.conf.urls import url, include

from academic.views import *


from . import views

urlpatterns = [
    path('', views.index, name='academic'),
    # Thesis
    path('thesis/', Thesis.as_view(), name='thesis_list'),
    path('thesis/new/', Thesis.register, name='thesis_new'),

    path('thesis/<int:pk>/', ThesisDetail.as_view(), name='thesis_detail'),
    path('thesis/update/<int:pk>/', ThesisUpdate.as_view(), name='thesis_update'),
    path('thesis/delete/<int:pk>/', ThesisDelete.as_view(), name='thesis_delete'),
    ## Comments
    #path('thesis/list_comment/<int:thesis_pk>', ComentThesis.as_view(), name='comment_thesis_list'),
    path('thesis/add_comment/<int:thesis_pk>', ComentThesis.register, name='comment_thesis_new'),
    path('thesis/upload_document/<int:thesis_pk>', Thesis.upload_document, name='upload_thesis_document'),
    path('thesis/documents_list/<int:thesis_pk>', Thesis.documents_list, name='thesis_documents_list'),
    path('thesis/document_viewer/<path:document_path>', Thesis.document_viewer, name='thesis_document_viewer'),
    # Advance
    path('advance/', AdvanceList.as_view(), name='advance_list'),
    path('advance/modal/<int:thesis>', Advance.register_modal, name='advance_modal'),
    path('advance/new/', Advance.register, name='advance_new'),
    path('advance/thesis/<int:thesis>', Advance.advance_by_thesis, name='advances_list'),

    #Student
    path('student/', Student.as_view(), name='student_list'),
    path('student/new/', Student.register, name='student_new'),
    path('student/edit/<int:user>/', Student.edit, name='student_edit'),
    path('student/disable/', Student.disabledStudent, name='student_disable'),

    #Teacher
    path('teacher/', TeacherView.as_view(), name='teacher_list'),
    path('teacher/new/', TeacherView.register, name='teacher_new'),
    path('teacher/edit/<int:user>/', TeacherView.edit, name='teacher_edit'),
    path('teacher/disable/', TeacherDisable.disabledTeacher, name='teacher_disable'),

]