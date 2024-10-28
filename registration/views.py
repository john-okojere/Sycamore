from django.shortcuts import render, redirect
from .forms import RegistrantForm
from .models import Registrant

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
