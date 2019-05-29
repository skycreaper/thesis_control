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