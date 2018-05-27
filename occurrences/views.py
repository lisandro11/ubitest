from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

from .models import Occurrence
from . import forms


'''
View that shows the list of all occurrences order by creation date
'''
def occurrences_list(request):
    occurrences = Occurrence.objects.all().order_by('creation_date');
    return render(request, 'occurrences/occurrences_list.html', {'occurrences': occurrences})

'''
View that return detail of an occurrence by a given id
'''
def occurrence_details(request, id):
    occurrence = Occurrence.objects.get(id=id)
    return render(request, 'occurrences/occurrence_detail.html', {'occurrence': occurrence})

'''
Create Occurrence View. Only authenticated user.
'''
@login_required(login_url="/accounts/login")
def occurrence_create(request):
    if request.method == 'POST':
        form = forms.CreateOccurrence(request.POST)
        if form.is_valid():
            #save occurence in db
            occurrence = form.save(commit=False)
            occurrence.author = request.user
            # occurrence.location = Point(occurrence.long,occurrence.lat)
            occurrence.save()
            return redirect('occurrences:list')
    else:
        form = forms.CreateOccurrence()
    return render(request, 'occurrences/occurrence_create.html', {'form':form})
