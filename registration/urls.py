from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('success/<int:registrant_id>/', views.success, name='success'),
    path('volunteer/<int:registrant_id>/', views.volunteer, name='volunteer'),
    path('attendees/', views.attendees, name='attendees'),
]
