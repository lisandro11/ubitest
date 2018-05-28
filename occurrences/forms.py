from django.contrib.gis import forms
from . import models


class CreateOccurrence(forms.ModelForm):
    '''
    Form for create an occurrence
    '''
    lat = forms.FloatField(required=True)
    long = forms.FloatField(required=True)
    class Meta:
        model = models.Occurrence
        fields = ('description', 'category', 'lat', 'long')
