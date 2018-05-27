"""
unit tests for API in restframework_gis
"""

import django
import urllib
import sys
import json
import pickle
from django.test import TestCase
from django.contrib.auth import get_user_model
from occurrences.models import Occurrence
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeoJsonDict

from .models import *
from .serializers import *


User = get_user_model()

# Create your tests here.
class OccurrencesAPITestCase(TestCase):
    def setUp(self):
        self.geos_error_message = 'Invalid format: string or unicode input unrecognized as GeoJSON, WKT EWKT or HEXEWKB.'
        self.gdal_error_message = 'Unable to convert to python object: Invalid geometry pointer returned from "OGR_G_CreateGeometryFromJson".'
        if django.VERSION[0] == 2:
            self.value_error_message = "Unable to convert to python object: String input unrecognized as WKT EWKT, and HEXEWKB."
        else:
            self.value_error_message = "Unable to convert to python object: String or unicode input unrecognized as WKT EWKT, and HEXEWKB."
        self.type_error_message = "Unable to convert to python object: Improper geometry input type:"
        user_obj = User(username='ubitest', email='test@test.com')
        user_obj.set_password("teste1234")
        user_obj.save()
        occurrence = Occurrence.objects.create(description='OccurrenceTeste', location='POINT (13.0078125000020002 42.4234565179379999)', category='SPECIAL_EVENT', author=user_obj)

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_occurrence(self):
        occurrence = Occurrence.objects.count()
        self.assertEqual(occurrence, 1)

    def test_get_occurrences_list(self):
        data = {}
        url = api_reverse("api:list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_get_occurrence_details(self):
        occurrence = Occurrence.objects.first()
        data = {}
        url = occurrence.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
