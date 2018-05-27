from rest_framework import generics, mixins, viewsets
from django.contrib.gis.geos import Point
from rest_framework_gis.filters import *
from rest_framework_gis.pagination import GeoJsonPagination
from django.utils.datastructures import *
from django.http import *


from occurrences.models import *
from .serializers import *
from .permissions import *


class OccurrencesListView(generics.ListAPIView):
    '''
    This view should return all occurences created.
    '''
    # lookup_field            = 'id' # slug, id # url(r'?P<id>\d+')
    serializer_class        = OccurrenceListSerializer
    permission_classes      = [AllowAny]

    def get_queryset(self):
        qs = Occurrence.objects.all()
        try:
            #allows get occurrence by the id portion of the URL.
            id = self.request.GET['id']
            if id is not None:
                qs = qs.filter(id=id)
        except MultiValueDictKeyError:
            # MultiValueDictKeyError happens when a key doesn't exist
            return qs
        except ValueError:
            # ValueError if something entered for a window that couldn't be interpreted
            return HttpResponse(status=400)
        count = qs.count()
        if count is 0:
            return HttpResponse('teste')
        return qs

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

occurrence_list = OccurrencesListView.as_view()

class OccurrenceDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Return an occurence with the id as determined by the id portion of the URL.
    Author of occurrence can edit or delete.
    """
    model = Occurrence
    lookup_field = 'id'
    serializer_class = OccurrenceListSerializer
    permission_classes = [AllowAny]
    queryset = Occurrence.objects.all()

    def get_permissions(self):
        # change permission for type of request
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        return super(OccurrenceDetails, self).get_permissions()

occurrence_details = OccurrenceDetails.as_view()

class OccurrencesCreateAPIView(generics.CreateAPIView):
    '''
    This view should gives the possibility for authenticated users to create occurrences
    '''
    serializer_class        = OccurrenceListSerializer
    permission_classes      = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Occurrence.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

occurrence_create = OccurrencesCreateAPIView.as_view()

class OccurrenceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Return an occurence with the id as determined by the id portion of the URL.
    Admin can update this Occurrence and change the state.
    """
    lookup_field            = 'id' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = OccurrenceUpdateSerializer
    permission_classes      = [IsAdminUser]
    #queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return Occurrence.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

occurrence_update = OccurrenceRetrieveUpdateView.as_view()

class OccurrencesByAuthorView(generics.ListAPIView):
    """
    This view should return a list of all the occurences for
    the user as determined by the author portion of the URL.
    """
    lookup_field            = 'author'
    serializer_class        = OccurrenceListSerializer
    permission_classes      = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        author = self.kwargs['author']
        return Occurrence.objects.filter(author=author)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

occurrence_by_author = OccurrencesByAuthorView.as_view()

class OccurrencesByCategoryView(generics.ListAPIView):
    """
    This view should return a list of all the occurences with
    the category as determined by the category portion of the URL.
    """
    lookup_field            = 'category' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = OccurrenceListSerializer
    permission_classes      = [IsAuthenticatedOrReadOnly]
    #queryset                = BlogPost.objects.all()

    def get_queryset(self):
        category = self.kwargs['category']
        return Occurrence.objects.filter(category=category)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

occurrence_by_category = OccurrencesByCategoryView.as_view()

class OccurrenceInRangeList(generics.ListAPIView):
    """
    Filters a queryset to only those Occurrences within a certain distance of a given point.
    Return a list of all the occurences returns only occurrence within the given distance of the given geometry defined by the URL parameter.
    eg:. /inrange/?dist=4000&point=-122.4862,37.7694&format=json which is equivalant to filtering within 4000 meters of the point (-122.4862, 37.7694).
    """
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceListSerializer
    # distance_filter_convert_meters = True #Convert meters to degrees
    distance_filter_field = 'location'
    filter_backends = (DistanceToPointFilter, )

occurrence_in_range = OccurrenceInRangeList.as_view()
