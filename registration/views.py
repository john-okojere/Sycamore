from django.shortcuts import render, redirect
from .forms import RegistrantForm
from .models import Registrant

#participant - p
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


#pastors - pst
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


#media - media
def media_register(request):
    if request.method == 'POST':
        form = RegistrantForm(request.POST)
        if form.is_valid():
            registrant = form.save()
            return redirect('media_success', registrant_id=registrant.id)
    else:
        form = RegistrantForm()
    
    return render(request, 'registration/media-register.html', {'form': form})

def media_success(request, registrant_id):
    registrant = Registrant.objects.get(id=registrant_id)
    return render(request, 'registration/media-success.html', {'registrant': registrant})









from .models import Volunteer

def volunteer(request, registrant_id):
    if request.method == 'POST':
        decision = request.POST.get('volunteer')
        # Handle volunteer decision here, you can redirect or display a message
        if decision == 'yes':
            volunteer = Volunteer.objects.filter(registrant_id = registrant_id)
            if not volunteer:
                Volunteer.objects.create(registrant_id = registrant_id)

            return render(request, 'registration/thank_you.html', {'message': 'Thank you for volunteering!'})
        else:
            return render(request, 'registration/thank_you.html', {'message': 'Thank you for registering!'})
    
    return render(request, 'registration/volunteer.html')

# def attendees_view(request):
#     registrants = Registrant.objects.all()
#     return render(request, 'attendees.html', {'registrants': registrants})

def manage_registration_and_volunteers(request):
    registrants = Registrant.objects.all()  # Get all registrants
    volunteers = Volunteer.objects.all()    # Get all volunteers

    if request.method == 'POST':
        # Here we are assuming you are sending the registrant_id to register as a volunteer
        registrant_id = request.POST.get('registrant_id')
        registrant = Registrant.objects.get(id=registrant_id)

        # Register the user as a volunteer
        volunteer = Volunteer(registrant=registrant)
        volunteer.save()

        return render(request, 'registration/manage.html', {
            'registrants': registrants,
            'volunteers': volunteers,
            'message': 'Thank you for volunteering!'
        })

    return render(request, 'registration/manage.html', {
        'registrants': registrants,
        'volunteers': volunteers,
    })
