from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('update_profile/<int:pk>', views.UpdateProfile.as_view(), name='update_profile'),
]