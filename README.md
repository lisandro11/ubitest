
# Event Management in Urban Environment

Record of occurrences with description, a geographical location, author, date of creation, date of update, state (to validate, validate, solve) and one of the following categories:
CONSTRUCTION: planned road work
SPECIAL_EVENT: special events (fair, sport event, etc.)
INCIDENT: accidents and other unexpected events
WEATHER_CONDITION: weather condition affecting the road
ROAD_CONDITION: status of the road that might affect travelers (potholes, bad pavement, etc.)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
Python  3.6.5
Django 2.0.5
Django Rest Framework 3.8.2
Django Rest Framework GIS 0.13
```

### Installing

A step by step series of examples that tell you how to get a development env running

Update your settings to reflect the following:

```
$pip install python==3.6.5
$pip install django==2.0.5
$pip install djangorestframework==3.2.8
$pip install djangorestframework-gis==0.13

```

And

```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'xxxxxx',
        'USER': 'xxxxx',
        'PASSWORD': 'xxxxxxx',
        'HOST': 'xxxxxx',
        'PORT': 'xxxxx',
    }
}

$cd ubi

$python manage.py makemigrations
$python manage.py migrate
$python manage.py createsuperuser
$python manage.py runserver
```

### Some API Endpoints
```
Create Occurrence(description, location, category)
POST: /api/occurrences/create/

List all occurrences
GET: /api/occurrences/

List Occurrence with id = <id>
GET: /api/occurrences/?id=<id>
GET: /api/occurrences/<id>/

Update Occurrence with id = <id>
PUT: /api/occurrences/<id>/

Update Occurrence with id = <id>
PATCH: /api/occurrences/<id>/

Delete Occurrence with id = <id>
DELETE: /api/occurrences/<id>/

Validate Occurrence with id = <id> (Change state)
PUT: /api/occurrences/validate/<id>/

List of occurrences created by author with id = <author_id>
GET: /api/occurrences/author/<author_id>/

List of occurrences created with category = <category>
GET: /api/occurrences/category/<category>/

List of occurrences in indicated range
GET: /api/occurrences/inrange/?dist=<int>&point=<double>,<double>
```

## Authors

* **Vitor Sousa**
