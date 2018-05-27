from django.contrib.gis import forms
from . import models

'''
Form for create an occurrence
'''
class CreateOccurrence(forms.ModelForm):
    class Meta:
        model = models.Occurrence
        fields = ['description', 'category', 'location']
