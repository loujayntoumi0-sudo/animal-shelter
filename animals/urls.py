from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:vet_id>/', views.chat_thread, name='chat_thread'),
    path('chat/message/<int:message_id>/edit/', views.chat_message_edit, name='chat_message_edit'),
    path('chat/message/<int:message_id>/delete/', views.chat_message_delete, name='chat_message_delete'),
    path('health/', views.health_record_list, name='health_record_list'),
    path('health/add/', views.health_record_add, name='health_record_add'),

    path('vets/', views.vet_list, name='vet_list'),
    path('vets/add/', views.vet_add, name='vet_add'),
    path('vets/edit/<int:pk>/', views.vet_edit, name='vet_edit'),

    path('pharmacy/', views.pharmacy_list, name='pharmacy_list'),
    path('pharmacy/add/', views.medication_add, name='medication_add'),
    path('pharmacy/edit/<int:pk>/', views.medication_edit, name='medication_edit'),

    path('animals/', views.animal_list, name='animal_list'),
    path('animals/add/', views.animal_add, name='animal_add'),
    path('animals/edit/<int:pk>/', views.animal_edit, name='animal_edit'),
    path('animals/delete/<int:pk>/', views.animal_delete, name='animal_delete'),


    path('adopters/', views.adopter_list, name='adopter_list'),
    path('adopters/add/', views.adopter_add, name='adopter_add'),
    path('adopters/edit/<int:pk>/', views.adopter_edit, name='adopter_edit'),
    path('adopters/delete/<int:pk>/', views.adopter_delete, name='adopter_delete'),
]