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
]

# urlpatterns = [

#     url(r'^$', CourseList.as_view(), name='list'),
#     url(r'^(?P<pk>\d+)$', CourseDetail.as_view(), name='detail'),
#     url(r'^nuevo$', CourseCreation.as_view(), name='new'),
#     url(r'^editar/(?P<pk>\d+)$', CourseUpdate.as_view(), name='edit'),
#     url(r'^borrar/(?P<pk>\d+)$', CourseDelete.as_view(), name='delete'),

# ]