from django.urls import path
from . import views

# Spelling check: urlpatterns (s nahi lagana, aur P small rahega)
urlpatterns = [
    path('', views.home, name='home'),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('upload-pet/', views.upload_pet, name='upload_pet'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pet/edit/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('pet/delete/<int:pet_id>/', views.delete_pet, name='delete_pet'),
    path('pet/adopt-confirm/<int:pet_id>/', views.mark_as_adopted, name='mark_as_adopted'),
]
