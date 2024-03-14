from django.urls import path
from .views import *
from .import views

urlpatterns = [

    path('',home,name='home'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('register/',registerUser,name='register'),
    path('apply/',applyPage,name='apply'),
    path('AddCompany/',views.AddCompany.as_view(),name='AddCompany'),
    path('candidate_list/', views.view_candidates, name='candidate_list'),
    path('admin/',admin,name='admin')
    
]