from django.urls import path

from . import views

urlpatterns = [
    path('getpersonal/', views.get_personal_tasks),
    path('addpersonal/', views.add_personal_tasks),
    path('archivepersonal/', views.archive_personal_tasks),
    path('deletepersonal/', views.delete_personal_tasks),
    path('googcal/', views.get_goog),
    path('outcal/', views.get_out),
    path('allcal/', views.get_all),
    path('updatepersonal/', views.update_personal_tasks),
    path('getwork/', views.get_work_tasks),
    path('addwork/', views.add_work_tasks),
    path('archivework/', views.archive_work_tasks),
    path('deletework/', views.delete_work_tasks),
    path('updatework/', views.update_work_tasks),
    path('addmeeting/', views.add_meeting),
    path('getmeeting/', views.get_meeting),
    path('deletemeeting/', views.get_meeting),
    path('addreminder/', views.add_reminder),
    path('getreminder/', views.get_reminder),
]