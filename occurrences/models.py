from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from rest_framework.reverse import reverse as api_reverse


class Occurrence(models.Model):
    #All States
    FOR_VALIDATING = 'For Validating'
    VALIDATED ='Validated'
    RESOLVED ='Resolved'

    STATE = (
        (FOR_VALIDATING, 'For Validating'),
        (VALIDATED, 'Validated'),
        (RESOLVED, 'Resolved'),
    )

    #All CATEGORIES
    CONSTRUCTION = 'CONSTRUCTION'
    SPECIAL_EVENT = 'SPECIAL_EVENT'
    INCIDENT = 'INCIDENT'
    WEATHER_CONDITION = 'WEATHER_CONDITION'
    ROAD_CONDITION = 'ROAD_CONDITION'

    CATEGORIES = (
       (CONSTRUCTION, 'planned road work'),
       (SPECIAL_EVENT, 'special events (fair, sport event, etc.)'),
       (INCIDENT, 'accidents and other unexpected events'),
       (WEATHER_CONDITION, 'weather condition affecting the road'),
       (ROAD_CONDITION, 'status of the road that might affect travellers (potholes, bad pavement, etc.)'),
    )

    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    location = models.PointField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    state = models.CharField(max_length=20, choices=STATE, default='For Validating')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.description

    def get_api_url(self, request=None):
        return api_reverse("api:details", kwargs={'id': self.id}, request=request)
