from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('media/', views.media_register, name='media_register'),
    path('pst/', views.pst_register, name='pst_register'),
    path('success/<int:registrant_id>/', views.success, name='success'),
    path('pst_success/<int:registrant_id>/', views.pst_success, name='pst_success'),
    path('media_success/<int:registrant_id>/', views.media_success, name='media_success'),
    path('volunteer/<int:registrant_id>/', views.volunteer, name='volunteer'),
    path('manage/', views.manage_registration_and_volunteers, name='manage_registrations'),
]
