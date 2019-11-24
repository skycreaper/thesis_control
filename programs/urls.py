from django.urls import path
from django.conf.urls import url, include

from .views import ProgramList, ProgramCreation, ProgramUpdate, SubProgramList

urlpatterns = [
    path('program_list', ProgramList.as_view(), name='program_list'),
    path('program_add', ProgramCreation.as_view(), name='program_add'),
    path('program_edit/<int:pk>', ProgramUpdate.as_view(), name='program_edit'),
    path('sub_program_list', SubProgramList.as_view(), name='sub_program_list'),
]