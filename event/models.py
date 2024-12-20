from django.db import models
from registration.models import Registrant as Person, InHouse as User
from django.conf import settings

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    start_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EventList(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    check_in_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserAttendee(models.Model):
    list = models.ForeignKey(EventList, on_delete=models.CASCADE, related_name='userattendee')
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attendee.first_name} - {self.list.event.name}"


class Attendee(models.Model):
    list = models.ForeignKey(EventList, on_delete=models.CASCADE, related_name='attendee' , null=True)
    attendee = models.ForeignKey(Person, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.list:
            return f"{self.attendee.first_name} - {self.list.event.name}"
        return f"{self.attendee.first_name} "


class FollowUp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Follow")
    goal = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} Follow Up Group'
    
class Soul(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    followup = models.ForeignKey(FollowUp, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.attendee.attendee.first_name} - {self.followup.user}'
    

class Comment(models.Model):
    soul = models.ForeignKey(Soul, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.soul.attendee.attendee.first_name} - {self.soul.followup.user}'