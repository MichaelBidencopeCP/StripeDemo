from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
]