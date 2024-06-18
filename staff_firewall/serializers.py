from rest_framework import serializers
from .models import FwStaff, Client, FwRegions


class FwStaffSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(
        queryset=FwRegions.objects.all(),
        slug_field='name'
    )
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
    region = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = FwStaff
        fields = '__all__'
