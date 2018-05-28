from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

from .models import Occurrence
from . import forms



@login_required(login_url="/accounts/login")
def occurrences_list(request):
    '''
    View that shows the list of all occurrences order by creation date
    '''
    occurrences = Occurrence.objects.all().order_by('creation_date')
    return render(request, 'occurrences/occurrences_list.html', {'occurrences': occurrences})

@login_required(login_url="/accounts/login")
def occurrence_details(request, id):
    '''
    View that return detail of an occurrence by a given id
    '''
    occurrence = Occurrence.objects.get(id=id)
    return render(request, 'occurrences/occurrence_detail.html', {'occurrence': occurrence})

@login_required(login_url="/accounts/login")
def occurrence_create(request):
    '''
    Create Occurrence View. Only authenticated user.
    '''
    if request.method == 'POST':
        form = forms.CreateOccurrence(request.POST)
        if form.is_valid():
            #save occurence in db
            occurrence = form.save(commit=False)
            lat = form.cleaned_data['lat']
            long = form.cleaned_data['long']
            location = Point(lat,long)
            occurrence.location = location
            occurrence.author = request.user
            occurrence.save()
            return redirect('occurrences:list')
    else:
        form = forms.CreateOccurrence()
    return render(request, 'occurrences/occurrence_create.html', {'form':form})

@login_required(login_url="/accounts/login")
def occurrences_map(request):
    '''
    View that shows the list of all occurrences in a map
    '''
    occurrences = Occurrence.objects.all()
    return render(request, 'occurrences/occurrences_map.html', {'occurrences': occurrences})
