from rest_framework import serializers
from .models import FwStaff, Client, FwRegions, FwActions


class FwStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = FwStaff
        fields = ['id', 'client', 'regions', 'ip', 'port', 'action']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']


class FwRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FwRegions
        fields = ['name']


class FwActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FwActions
        fields = ['name']


class FwStaffDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    regions = FwRegionsSerializer()
    action = FwActionsSerializer()

    class Meta:
        model = FwStaff
        fields = ['id', 'client', 'regions', 'ip', 'port', 'action']
