from django.contrib import admin
from .models import Event, EventList, Attendee, UserAttendee, Comment, FollowUp, Soul

class EventListInline(admin.TabularInline):
    model = EventList
    extra = 1  # Number of empty forms to display

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'created')
    inlines = [EventListInline]

class AttendeeInline(admin.TabularInline):
    model = Attendee
    extra = 1

class EventListAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'check_in_time')
    inlines = [AttendeeInline]
    search_fields = ('name', 'event__name')  # Add search functionality

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'list', 'check_in_time')
    search_fields = ('attendee__user__username', 'list__name', 'list__event__name')

class UserAttendeeAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'list', 'check_in_time')
    search_fields = ('attendee__user__username', 'list__name', 'list__event__name')

admin.site.register(Event, EventAdmin)
admin.site.register(EventList, EventListAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(UserAttendee, UserAttendeeAdmin)
admin.site.register(Comment)
admin.site.register(Soul)
admin.site.register(FollowUp)
