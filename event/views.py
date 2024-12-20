from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Event, EventList, Attendee, UserAttendee
from .forms import EventForm, EventListForm, AttendeeForm, UserAttendeeForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def event_list_view(request):
    events = Event.objects.annotate(
        everyone=Count('eventlist__userattendee__attendee', distinct=True) +
                      Count('eventlist__attendee__attendee', distinct=True),
        allworker=Count('eventlist__userattendee__attendee', distinct=True),
        allattendee=Count('eventlist__attendee__attendee', distinct=True)
    ).order_by('-created')

    event_form = EventForm()
    event_list_form = EventListForm()

    return render(request, 'event/event_list.html', {
        'events': events,
        'event_form': event_form,
        'event_list_form': event_list_form
    })



@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return JsonResponse({'id': event.id, 'name': event.name, 'description': event.description, 'start_date': event.start_date})
    return HttpResponseBadRequest("Invalid request")

@login_required
def create_event_list_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventListForm(request.POST)
        if form.is_valid():
            event_list = form.save(commit=False)
            event_list.event = event
            event_list.save()
            attendee_user_count = UserAttendee.objects.filter(list = event_list).count()
            attendee_count = Attendee.objects.filter(list = event_list).count()
            return JsonResponse({'id': event_list.id, 'description': event_list.description, 'name': event_list.name,'user_count':attendee_user_count ,'count':attendee_count})
    return HttpResponseBadRequest("Invalid request")


@login_required
def event_details_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    lists = []
    event_list = EventList.objects.filter(event=event)
    for events in event_list:
        attendee_count = Attendee.objects.filter(list = events).count()
        attendee_user_count = UserAttendee.objects.filter(list = events).count()
        lists.append({
            'id': events.id, 
            'description': events.description,
            'name': events.name, 
            'count':attendee_count,
            'user_count':attendee_user_count 
        })
    return JsonResponse({'lists': lists})

@login_required
def coming_soon(request):
    return render(request, 'coming_soon.html')

def list_view(request, list_id):
    event_list = get_object_or_404(EventList, id=list_id)
    form = AttendeeForm()
    return render(request, 'event/list_view.html', {
        'event_list': event_list,
        'form': form
    })

@login_required
def add_attendee_view(request, list_id):
    event_list = get_object_or_404(EventList, id=list_id)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee_id = form.cleaned_data.get('attendee')
            if Attendee.objects.filter(list=event_list, attendee=attendee_id):
                attendee = Attendee.objects.get(list=event_list, attendee=attendee_id)
                return JsonResponse({'error': f'ID: {attendee.attendee.id} is already present in the list'}, status=400)
            else:
                attendee = form.save(commit=False)
                attendee.list = event_list
                attendee.save()
            return JsonResponse({
                'id': attendee.attendee.id,
                'attendee_first_name': attendee.attendee.first_name,
                'attendee_last_name': attendee.attendee.last_name,
                'attendee_phone': attendee.attendee.phone_number,
                'check_in_time': attendee.check_in_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'error': 'Invalid form'}, status=400)


@login_required
def user_list_view(request, list_id):
    event_list = get_object_or_404(EventList, id=list_id)
    form = UserAttendeeForm()
    return render(request, 'event/list_user_view.html', {
        'event_list': event_list,
        'form': form
    })

@login_required
def add_user_attendee_view(request, list_id):
    event_list = get_object_or_404(EventList, id=list_id)
    if request.method == 'POST':
        form = UserAttendeeForm(request.POST)
        if form.is_valid():
            attendee_id = form.cleaned_data.get('attendee')
            if UserAttendee.objects.filter(list=event_list, attendee=attendee_id):
                attendee = UserAttendee.objects.get(list=event_list, attendee=attendee_id)
                return JsonResponse({'error': f'ID: {attendee.attendee.id} is already present in the list'}, status=400)
            else:
                attendee = form.save(commit=False)
                attendee.list = event_list
                attendee.save()
            return JsonResponse({
                'id': attendee.attendee.id,
                'attendee_first_name': attendee.attendee.first_name,
                'attendee_last_name': attendee.attendee.last_name,
                'attendee_phone': attendee.attendee.phone,
                'check_in_time': attendee.check_in_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'error': 'Invalid worker form'}, status=400)


@login_required
def scan(request, list_id):
    event_list = get_object_or_404(EventList, id=list_id)
    return render(request, 'event/scan.html', {'event_list':event_list} )


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from registration.models import Registrant as Person, InHouse as User
from urllib.parse import urlparse


@login_required
def getscan(request, list_id):
    event_list = get_object_or_404(EventList, id=list_id)
    data = json.loads(request.body)
    url_string = data.get('text')
    parsed_url = urlparse(url_string) #https://dashboard.layersoftruth.org/Special/1
    path = parsed_url.path
    component = 'Siloam'

    category = component[0]
    uid = url_string
    
    if uid:
        person = Person.objects.get(uid = uid)
        if Attendee.objects.filter(list=event_list, attendee=person):
            attendee = Attendee.objects.filter(list=event_list, attendee=person).first()
            return JsonResponse({'message': f'ID: {attendee.attendee.id} is already present in the list'})
        else:
            Attendee.objects.create(list = event_list, attendee=person)

        return JsonResponse({'success': 'successfully added to the list'})
    else:
        return JsonResponse({'error': 'No string data received'}, status=400)
    


from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Event, FollowUp, EventList, Attendee, Soul, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import FollowUpForm, CommentForm, SinglePersonForm
import datetime
from django.db.models import Count

def follow_up_system(request):
    follow_ups = FollowUp.objects.all().order_by('-date')
    form = FollowUpForm()

    # Query to find persons not in any follow-up group
    persons_not_in_follow_up = Person.objects.annotate(follow_up_count=Count('attendee__soul')).filter(follow_up_count=0)
    number_of_persons_not_in_follow_up = persons_not_in_follow_up.count()

    context = {
        'follow_ups': follow_ups,
        'form': form,
        'persons_not_in_follow_up': persons_not_in_follow_up,
        'number_of_persons_not_in_follow_up': number_of_persons_not_in_follow_up,
    }
    return render(request, 'event/followup.html', context)

@login_required
def get_persons_not_in_follow_up(request):
    persons_not_in_follow_up = Person.objects.annotate(follow_up_count=Count('attendee__soul')).filter(follow_up_count=0).values('id', 'first_name', 'last_name', 'email', 'phone_number')
    return JsonResponse(list(persons_not_in_follow_up), safe=False)

# Event search view
def event_search(request):
    term = request.GET.get('term', '')
    events = Event.objects.filter(name__icontains=term)
    results = [{'id': event.id, 'label': event.name} for event in events]
    return JsonResponse(results, safe=False)


from django.db.models import Prefetch

@login_required
@csrf_exempt
@require_POST
def create_follow_up(request):
    form = FollowUpForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        goal = form.cleaned_data['goal']
        source = form.cleaned_data['source']
        max_persons = form.cleaned_data['max_persons']
        follow_up = FollowUp.objects.create(name=name, user=request.user, goal=goal)
        
        unique_person_ids = set()

        if source == 'event':
            try:
                event_id = form.cleaned_data['event'].id
            except:
                follow_up.delete()
                return JsonResponse({'message':'Group creation canceled!'})
            event = get_object_or_404(Event, id=event_id)
            
            # Fetch all attendees for the event
            attendees = Attendee.objects.filter(list__event=event).select_related('attendee')[:max_persons]

            # Use Prefetch to prefetch related Soul objects and attendee__id field
            attendees = attendees.prefetch_related(Prefetch('soul_set', queryset=Soul.objects.only('attendee__id')))
            
            unique_person_ids = set()
            for attendee in attendees:
                person_id = attendee.attendee.id
                # Check if the person is already in any follow-up group
                if person_id not in unique_person_ids and not attendee.soul_set.exists():
                    unique_person_ids.add(person_id)
                    Soul.objects.create(attendee=attendee, followup=follow_up)
        
        elif source == 'no_event':
            persons_in_follow_up = Soul.objects.values_list('attendee__attendee__id', flat=True)
            persons = Person.objects.exclude(id__in=persons_in_follow_up).exclude(attendee__list__event__isnull=False).distinct()[:max_persons]

            for person in persons:
                # Check if the person is already in any follow-up group
                if person.id not in unique_person_ids and not Soul.objects.filter(attendee__attendee__id=person.id).exists():
                    # Check if the person has any attendance in any event
                    if not Attendee.objects.filter(attendee=person).exists():
                        unique_person_ids.add(person.id)
                        attendeelist = f'noevent'
                        no_event, index = Event.objects.get_or_create(name = attendeelist, description="People that dont have attendance but has to be followed up." ,start_date  = datetime.datetime.now())
                        no_eventlist, i = EventList.objects.get_or_create(event=no_event, name=f'noeventlist_{follow_up.id}', description=f"people that have not attended service before but are about to join {follow_up.name} follow up group")
                        attendee = Attendee.objects.create(list=no_eventlist, attendee=person)  
                        Soul.objects.create(attendee=attendee, followup=follow_up)
        else:
            follow_up.delete()
            return JsonResponse({'message':'Group creation canceled!'})
        return JsonResponse({'message': 'Follow-up created successfully'})
    return JsonResponse({'message': 'Invalid form data'}, status=400)


@login_required
def view_comments(request):
    soul_id = request.GET.get('soul_id')
    soul = get_object_or_404(Soul, pk=soul_id)
    comments = Comment.objects.filter(soul=soul).order_by('-date')
    comments_list = list(comments.values('user__first_name', 'user__last_name', 'comments', 'date'))
    return JsonResponse({'comments': comments_list})


@login_required
@require_POST
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        soul_id = form.cleaned_data['soul_id']
        soul = get_object_or_404(Soul, pk=soul_id)
        comment = form.cleaned_data['comment']
        soul.comments = comment
        Comment.objects.create(soul=soul, user=request.user,comments = comment)
        soul.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def attendee_bio(request, attendee_id):
    attendee = get_object_or_404(Attendee, pk=attendee_id)
    attendee_details = {
        'aid': attendee.attendee.id,
        'first_name': attendee.attendee.first_name,
        'last_name': attendee.attendee.last_name,
        'email': attendee.attendee.email,
        'phone': attendee.attendee.phone_number,
        'event': attendee.list.event.name,
        'check_in_time': attendee.check_in_time,
    }
    return JsonResponse(attendee_details)


@login_required
def follow_up_view(request, pk):
    follow_ups = FollowUp.objects.get(pk=pk)
    persons_not_in_follow_up = Person.objects.annotate(follow_up_count=Count('attendee__soul')).filter(follow_up_count=0)
    return render(request, 'event/followupdetail.html', {'follow_ups': follow_ups, 'persons_not_in_follow_up':persons_not_in_follow_up})


@login_required
def follow_up_delete(request, pk):
    follow_ups = FollowUp.objects.get(pk=pk)
    if EventList.objects.filter(name=f'noeventlist_{follow_ups.id}'):
        no_eventlist = EventList.objects.get(name=f'noeventlist_{follow_ups.id}')
        no_eventlist.delete()
    for souls in follow_ups.soul_set.all():
        souls.delete()
    follow_ups.delete()
    return JsonResponse({'success': True})


@login_required
def soul_delete(request, attendee_id):
    attendee = get_object_or_404(Soul, pk=attendee_id)
    attendee.delete()
    return JsonResponse({'success': True})


@login_required
def add_single_person(request, pk):
    follow_up = FollowUp.objects.get(pk=pk)
    if request.method == 'POST':
        form = SinglePersonForm(request.POST)
        if form.is_valid():
            person_id = request.POST.get('person_id')
            print(person_id)
            person = get_object_or_404(Person, pk=person_id)
            
            # Check if the person is already in any follow-up group
            if Soul.objects.filter(followup=follow_up, attendee__attendee=person).exists():
                return JsonResponse({'message': 'Person is already in the follow-up group.'}, status=400)
            
            # Create an Attendee object
            attendee = Attendee.objects.create(attendee=person)
            
            # Create a Soul object
            Soul.objects.create(attendee=attendee, followup=follow_up)

            return JsonResponse({'message': 'Person added successfully to the follow-up group.'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)