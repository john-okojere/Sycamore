from django.contrib import admin
from .models import Minister, Registrant, Volunteer, InHouse

@admin.register(Registrant)
class RegistrantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'state', 'country', 'accommodation', 'marital_status')
    list_filter = ('state', 'country', 'accommodation', 'marital_status')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('registrant',)
    search_fields = ('registrant__first_name', 'registrant__last_name', 'registrant__email')

@admin.register(InHouse)
class InHouseAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'department')
    list_filter = ('department',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

@admin.register(Minister)
class MinisterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')