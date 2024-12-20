from django import forms
from .models import Event, EventList, Attendee, UserAttendee

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Event
        fields = ['name', 'description' ,'start_date']

class EventListForm(forms.ModelForm):
    class Meta:
        model = EventList
        fields = ['name', 'description']

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['attendee']


class UserAttendeeForm(forms.ModelForm):
    class Meta:
        model = UserAttendee
        fields = ['attendee']

from django import forms
from .models import FollowUp, Event, Person

class FollowUpForm(forms.ModelForm):
    SOURCE_CHOICES = [
        ('event', 'From Event'),
        ('no_event', 'Not in Any Event'),
    ]
    
    source = forms.ChoiceField(choices=SOURCE_CHOICES, required=True, label="Source")
    event = forms.ModelChoiceField(queryset=Event.objects.all(), required=False, label="Event")
    max_persons = forms.IntegerField(required=False, label="Max Persons")

    class Meta:
        model = FollowUp
        fields = ['name', 'goal', 'source', 'event', 'max_persons']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_persons'].widget.attrs.update({'class': 'form-control'})
        self.fields['goal'].widget.attrs.update({'class': 'form-control'})


class CommentForm(forms.Form):
    soul_id = forms.IntegerField(widget=forms.HiddenInput)
    comment = forms.CharField(widget=forms.Textarea)

class SinglePersonForm(forms.Form):
    person_id = forms.ModelChoiceField(queryset=Person.objects.all(), label='Person', widget=forms.Select(attrs={'class': 'form-control'}))