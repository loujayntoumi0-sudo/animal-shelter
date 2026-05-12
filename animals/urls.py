from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/add/', views.animal_add, name='animal_add'),
    path('animals/edit/<int:pk>/', views.animal_edit, name='animal_edit'),
    path('animals/delete/<int:pk>/', views.animal_delete, name='animal_delete'),


    path('adopters/', views.adopter_list, name='adopter_list'),
    path('adopters/add/', views.adopter_add, name='adopter_add'),
    path('adopters/edit/<int:pk>/', views.adopter_edit, name='adopter_edit'),
    path('adopters/delete/<int:pk>/', views.adopter_delete, name='adopter_delete'),
]