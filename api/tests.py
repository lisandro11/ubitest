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
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse as api_reverse
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeoJsonDict
from rest_framework.authtoken.models import Token

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
        user_admin = User(username='ubiadmin', email='admin@test.com')
        user_admin.set_password("teste1234")
        user_admin.is_staff = True
        user_admin.save()
        occurrence = Occurrence.objects.create(description='OccurrenceTeste', location='POINT (13.0078125000020002 42.4234565179379999)', category='SPECIAL_EVENT', author=user_obj)

    def test_users(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)
        # print('Test: created users')

    def test_single_occurrence(self):
        occurrence = Occurrence.objects.count()
        self.assertEqual(occurrence, 1)
        # print('Test: created occurrence')

    def test_get_occurrences_list(self):
        data = {}
        url = api_reverse("api:list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_occurrence_by_id(self):
        occurrence = Occurrence.objects.first()
        data = {}
        url = api_reverse("api:list") #/api/occurrences/
        url = url + '?id=' + str(occurrence.id) #/api/occurrences/?id=1
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_occurrence_details(self):
        occurrence = Occurrence.objects.first()
        data = {}
        url = occurrence.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print('Test: get single occurrence')
        # print(response.data)

    def test_create_occurrence(self):
        # user = User.objects.first()
        data = {'description':'Post Occurrence', 'location':'POINT (13.0078125000020002 42.4234565179379999)', 'category':'SPECIAL_EVENT'}
        url = api_reverse("api:create")

        # test create occurrence without authenticated user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # print(response.data)

        # test create occurrence with authenticated user
        client = APIClient()
        client.login(username='ubitest', password='teste1234')
        response = client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #test author
        user = User.objects.get(username='ubitest')
        occurrence = Occurrence.objects.get(description='Post Occurrence')
        self.assertEqual(user, occurrence.author)

    def test_occurrence_update(self):
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        data = {'description':'OccurrenceUpdated', 'location':'POINT (13.0 42.0)', 'category':'CONSTRUCTION'}
        url = occurrence.get_api_url()

        #Post Not Allowed
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        #not_authenticated
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #authenticated user but not the author of occurrence
        client = APIClient()
        client.login(username='ubiadmin', password='teste1234')
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.logout()

        #authenticated user
        client = APIClient()
        client.login(username='ubitest', password='teste1234')
        response = client.put(url, data, format='json')
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        self.assertEqual(occurrence.description, 'OccurrenceUpdated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_occurrence_vatidate(self):
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        data = {}
        url = '/api/occurrences/validate/' + str(occurrence.id) + '/' #/api/occurrences/validate/8/
        self.assertEqual(occurrence.state, 'For Validating')

        #test GET occurrence without authenticated user
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #authenticated user but not admin/staff
        client = APIClient()
        client.login(username='ubitest', password='teste1234')
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #Validate Occurrence with authenticated user but not admin
        data = {'state', 'Resolved'}
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.logout()

        #GET occurrence with authenticated admin user
        data = {}
        client.login(username='ubiadmin', password='teste1234')
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Validate Occurrence with authenticated admin user
        data = {'state':'Resolved'}
        client.login(username='ubiadmin', password='teste1234')
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        self.assertEqual(occurrence.state, 'Resolved')

    def test_occurrence_by_author(self):
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        data = {}
        url = '/api/occurrences/author/' + str(occurrence.author.id) + '/' #/api/occurrences/author/<id>

        #test GET occurrence
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure if only 1 occurrence exists
        self.assertEqual(len(response.data['features']), 1)

        user = User.objects.get(username='ubiadmin')
        url = '/api/occurrences/author/' + str(user.id) + '/' #/api/occurrences/author/<id>

        #test GET occurrences
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure if don't exist occurrences
        self.assertEqual(len(response.data['features']), 0)

    def test_occurrence_by_category(self):
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        data = {}
        url = '/api/occurrences/category/' + str(occurrence.category) + '/' #/api/occurrences/category/<category_name>

        #test GET occurrence
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure if only 1 occurrence exists
        self.assertEqual(len(response.data['features']), 1)

        url = '/api/occurrences/category/CONSTRUCTION/' #/api/occurrences/category/<category_name>
        #test GET occurrences
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure if don't exist occurrences
        self.assertEqual(len(response.data['features']), 0)

    def test_get_occurrence_in_range(self):
        data = {}
        url = api_reverse("api:occurrence-in-range") # ?dist=4000&point=-122.4862,37.7694&format=json
        url = url + "?dist=4000&point=13.00,42.03"
        # POINT (13.0078125000020002 42.4234565179379999)
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

        url = api_reverse("api:occurrence-in-range")
        url = url + "?dist=50&point=70.00,60.03"
        # POINT (13.0078125000020002 42.4234565179379999)
        response = self.client.get(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 0)

    def test_occurrence_delete(self):
        occurrence = Occurrence.objects.first() #occurrene description = OccurrenceTeste
        data = {}
        url = occurrence.get_api_url()
        occurrences_count = Occurrence.objects.count()
        self.assertEqual(occurrences_count, 1)

        #Post Not Allowed
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        #not_authenticated
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #authenticated user but not the author of occurrence
        client = APIClient()
        client.login(username='ubiadmin', password='teste1234')
        response = client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.logout()

        #authenticated user
        client = APIClient()
        client.login(username='ubitest', password='teste1234')
        response = client.delete(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        occurrences_count = Occurrence.objects.count()
        self.assertEqual(occurrences_count, 0)
