from django.urls import path

from . import views

urlpatterns = [
    path('getpersonal/', views.get_personal_tasks),
    path('addpersonal/', views.add_personal_tasks),
    path('archivepersonal/', views.archive_personal_tasks),
    path('deletepersonal/', views.delete_personal_tasks),
    path('googcal/', views.get_google_calendar_events),
]