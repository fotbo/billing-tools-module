from rest_framework import serializers
from .models import FwStaff, Client, FwRegions


class FwStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = FwStaff
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']


class FwRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FwRegions
        fields = ['name']


class FwStaffDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    regions = FwRegionsSerializer()

    class Meta:
        model = FwStaff
        fields = '__all__'
