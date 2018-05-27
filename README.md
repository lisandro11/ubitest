# Occurrences Administration


Software
----------
Python  3.6.5
Django 2.0.5
Django Rest Framework 3.8.2
Django Rest Framework 0.13

Update your settings to reflect the following:
------------------------------------------------
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

Initial Setup
--------------
$pip install python==3.6.5
$pip install django==2.0.5
$pip install djangorestframework==3.2.8
$pip install djangorestframework-gis==0.13

$cd ubi

$python manage.py makemigrations
$python manage.py migrate
$python manage.py createsuperuser
$python manage.py runserver
