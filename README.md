
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
Django Rest Framework 0.13
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

## Authors

* **Vitor Sousa**
