from django.shortcuts import render, redirect
from .forms import RegistrantForm, InHouseForm
from .models import Registrant, Volunteer, InHouse

# Participant Registration
def register(request):
    if request.method == 'POST':
        form = RegistrantForm(request.POST)
        if form.is_valid():
            registrant = form.save()
            return redirect('success', registrant_id=registrant.id)
    else:
        form = RegistrantForm()
    
    return render(request, 'registration/register.html', {'form': form})

def success(request, registrant_id):
    registrant = Registrant.objects.get(id=registrant_id)
    return render(request, 'registration/success.html', {'registrant': registrant})


# Pastor Registration
def pst_register(request):
    if request.method == 'POST':
        form = RegistrantForm(request.POST)
        if form.is_valid():
            registrant = form.save()
            return redirect('pst_success', registrant_id=registrant.id)
    else:
        form = RegistrantForm()
    
    return render(request, 'registration/pst-register.html', {'form': form})

def pst_success(request, registrant_id):
    registrant = Registrant.objects.get(id=registrant_id)
    return render(request, 'registration/pst-success.html', {'registrant': registrant})


# Workforce (Media) Registration
def workforce_reg(request):
    if request.method == 'POST':
        form = RegistrantForm(request.POST)
        if form.is_valid():
            registrant = form.save()
            return redirect('workforce_success', registrant_id=registrant.id)
    else:
        form = RegistrantForm()
    
    return render(request, 'registration/workforce-reg.html', {'form': form})

def workforce_success(request, registrant_id):
    registrant = Registrant.objects.get(id=registrant_id)
    return render(request, 'registration/workforce-success.html', {'registrant': registrant})


# Volunteer Registration
def volunteer(request, registrant_id):
    if request.method == 'POST':
        decision = request.POST.get('volunteer')
        if decision == 'yes':
            volunteer = Volunteer.objects.filter(registrant_id=registrant_id)
            if not volunteer:
                Volunteer.objects.create(registrant_id=registrant_id)
            return render(request, 'registration/thank_you.html', {'message': 'Thank you for volunteering!'})
        else:
            return render(request, 'registration/thank_you.html', {'message': 'Thank you for registering!'})
    
    return render(request, 'registration/volunteer.html')


# InHouse Registration
def inhouse_register(request):
    if request.method == 'POST':
        form = InHouseForm(request.POST)
        if form.is_valid():
            inhouse_member = form.save()
            return redirect('inhouse_success', inhouse_id=inhouse_member.id)
    else:
        form = InHouseForm()
    
    return render(request, 'registration/inhouse-register.html', {'form': form})

def inhouse_success(request, inhouse_id):
    inhouse_member = InHouse.objects.get(id=inhouse_id)
    return render(request, 'registration/inhouse-success.html', {'inhouse_member': inhouse_member})


# Manage Registration and Volunteers
def manage_registration_and_volunteers(request):
    registrants = Registrant.objects.all()
    volunteers = Volunteer.objects.all()
    inhouse_members = InHouse.objects.all()

    if request.method == 'POST':
        registrant_id = request.POST.get('registrant_id')
        registrant = Registrant.objects.get(id=registrant_id)

        volunteer = Volunteer(registrant=registrant)
        volunteer.save()

        return render(request, 'registration/manage.html', {
            'registrants': registrants,
            'volunteers': volunteers,
            'inhouse_members': inhouse_members,
            'message': 'Thank you for volunteering!'
        })

    return render(request, 'registration/manage.html', {
        'registrants': registrants,
        'volunteers': volunteers,
        'inhouse_members': inhouse_members,
    })


# Monitor Registered People
def monitor_registrations(request):
    registrants = Registrant.objects.all()
    volunteers = Volunteer.objects.all()
    inhouse_members = InHouse.objects.all()

    return render(request, 'registration/monitor.html', {
        'registrants': registrants,
        'volunteers': volunteers,
        'inhouse_members': inhouse_members,
    })

def participant_cards(request):
    registrant = Registrant.objects.all()    
    return render(request, 'registration/participantcards.html' , {'registrant':registrant})

def minister_cards(request):
    registrant = Minister.objects.all()    
    return render(request, 'registration/ministercards.html' , {'registrant':registrant})

def inhouse_cards(request):
    registrant = Registrant.objects.all()    
    return render(request, 'registration/inhousecards.html' , {'registrant':registrant})