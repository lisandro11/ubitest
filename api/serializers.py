from rest_framework import serializers, pagination
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from django.contrib.gis.geos import Point
from occurrences.models import *

# converts to JSON
# validations for data passed
# fields = [  'url', 'id', 'description', 'location', 'category', 'state', 'creation_date', 'update_date', 'author']

class OccurrenceListSerializer(GeoFeatureModelSerializer):
    url         = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Occurrence
        lookup_field = 'id'
        geo_field = 'location'
        id_field = 'id'
        fields = '__all__'
        read_only_fields = ['url', 'id', 'author', 'state', 'creation_date', 'update_date']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class OccurrenceUpdateSerializer(serializers.ModelSerializer):
    url         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Occurrence
        fields = fields = '__all__'
        read_only_fields = [ 'url', 'id', 'description', 'location', 'category', 'creation_date', 'update_date', 'author']

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

# class OccurrenceCreateSerializer(GeoFeatureModelSerializer):
#     class Meta:
#         model = Occurrence
#         geo_field = 'location'
#         id_field = 'id'
#         fields = '__all__'
#         read_only_fields = ['url','id', 'author', 'state', 'creation_date', 'update_date']
