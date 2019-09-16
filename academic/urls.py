from django.urls import path
from django.conf.urls import url, include

from academic.views import *


from . import views

urlpatterns = [
    path('', views.index, name='academic'),
    # Thesis
    path('thesis/', ThesisList.as_view(), name='thesis_list'),
    path('thesis/<int:pk>/', ThesisDetail.as_view(), name='thesis_detail'),
    path('thesis/new/', ThesisCreation.as_view(), name='thesis_new'),
    path('thesis/update/<int:pk>/', ThesisUpdate.as_view(), name='thesis_update'),
    path('thesis/delete/<int:pk>/', ThesisDelete.as_view(), name='thesis_delete'),
    # Advance
    path('advance/', AdvanceList.as_view(), name='advance_list'),
    #Student
    path('student/', StudentList.as_view(), name='student_list'),
    # path('student/new/', StudentCreation.as_view(), name='student_new'),
    path('student/new/', Student.register, name='student_new'),
    path('student/edit/<int:user>/', StudentEdit.edit, name='student_edit'),
    path('student/disable/', StudentDisable.disabledStudent, name='student_disable'),
    #Teacher
    path('teacher/', TeacherList.as_view(), name='teacher_list'),
    path('teacher/new/', TeacherCreation.as_view(), name='teacher_new'),
    path('teacher/edit/<int:user>/', TeacherEdit.edit, name='teacher_edit'),
    path('teacher/disable/', TeacherDisable.disabledTeacher, name='teacher_disable'),

]