from django.urls import path
from django.conf.urls import url, include

from .views import ProgramList, ProgramCreation, ProgramUpdate, ProgramDetail, SubProgramList, SubProgramList, SubprogramCreation, SubProgramUpdate, SubProgramDetail, SubProgramTaskDetail, SubProgramTaskAdd, TaskAdvanceDetail

urlpatterns = [
    path('program_list', ProgramList.as_view(), name='program_list'),
    path('program_add', ProgramCreation.as_view(), name='program_add'),
    path('program_edit/<int:pk>', ProgramUpdate.as_view(), name='program_edit'),
    path('program_detail/<int:pk>', ProgramDetail.as_view(), name='program_detail'),
    path('subprogram_by_program_list/<int:pk>', SubProgramList.as_view(), name='subprogram_by_program'),
    path('sub_program_list', SubProgramList.as_view(), name='sub_program_list'),
    path('subprogram_add/<int:program>', SubprogramCreation.as_view(), name='subprogram_add'),
    path('subprogram_update/<int:pk>', SubProgramUpdate.as_view(), name='subprogram_update'),
    path('subprogram_detail/<int:pk>', SubProgramDetail.as_view(), name='subprogram_detail'),
    path('subprogramtask_detail/<int:pk>', SubProgramTaskDetail.as_view(), name='subprogramtask_detail'),
    path('subprogramtask_add/<int:subprogram>', SubProgramTaskAdd.as_view(), name='subprogramtask_add'),
    path('taskadvance_detail/download/<path:document_path>', TaskAdvanceDetail.download_item, name='task_advance_download'),
]