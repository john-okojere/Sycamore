from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),  # Main registration page
    path('workforce/', views.workforce_reg, name='workforce_reg'),  # Workforce registration
    path('pst/', views.pst_register, name='pst_register'),  # Pastor registration
    path('success/<int:registrant_id>/', views.success, name='success'),  # Registration success page
    path('pst_success/<int:registrant_id>/', views.pst_success, name='pst_success'),  # Pastor registration success
    path('workforce_success/<int:registrant_id>/', views.workforce_success, name='workforce_success'),  # Workforce success
    path('volunteer/<int:registrant_id>/', views.volunteer, name='volunteer'),  # Volunteer confirmation
    path('inhouse/', views.inhouse_register, name='inhouse_register'),  # InHouse registration page
    path('inhouse_success/<int:inhouse_id>/', views.inhouse_success, name='inhouse_success'),  # InHouse success page
    path('manage/', views.manage_registration_and_volunteers, name='manage_registrations'),  # Manage registrations and volunteers
    path('monitor/', views.monitor_registrations, name='monitor_registrations'),  # Monitor all registrations
    path('participantcards/', views.participant_cards, name='participant_cards'),  # View all registration cards
    path('inhousecards/', views.inhouse_cards, name='inhouse_cards'),  # View all registration cards
]