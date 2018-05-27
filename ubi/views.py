from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse(html)
    return render(request, 'homepage.html')

def about(request):
    # return HttpResponse("About Section")
    return render(request, 'about.html')
