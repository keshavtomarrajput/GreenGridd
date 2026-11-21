"""
Django REST Framework Serializers for GreenGrid
"""

from rest_framework import serializers
from .models import (
    Role, UserAccount, Facility, Meter, TelemetryReading,
    Benchmark, UtilityProvider, UtilityBill, Recommendation,
    RenewableSystem, RenewableGenerationLog, DemandResponseEvent
)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):
    role_name = serializers.ReadOnlyField(source='role.role_name')

    class Meta:
        model = UserAccount
        fields = ['user_id', 'username', 'email', 'full_name', 'phone_number', 'role', 'role_name', 'is_active', 'last_login', 'created_at']
        extra_kwargs = {'password_hash': {'write_only': True}}


class MeterSerializer(serializers.ModelSerializer):
    facility_name = serializers.ReadOnlyField(source='facility.name')

    class Meta:
        model = Meter
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):
    manager_name = serializers.ReadOnlyField(source='manager.full_name')
    meter_count = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = '__all__'

    def get_meter_count(self, obj):
        return obj.meters.count()


class TelemetryReadingSerializer(serializers.ModelSerializer):
    meter_name = serializers.ReadOnlyField(source='meter.meter_name')
    meter_type = serializers.ReadOnlyField(source='meter.meter_type')
    facility_name = serializers.ReadOnlyField(source='meter.facility.name')

    class Meta:
        model = TelemetryReading
        fields = '__all__'


class BenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benchmark
        fields = '__all__'


class UtilityProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityProvider
        fields = '__all__'


class UtilityBillSerializer(serializers.ModelSerializer):
    facility_name = serializers.ReadOnlyField(source='facility.name')
    provider_name = serializers.ReadOnlyField(source='provider.provider_name')
    verified_by_name = serializers.ReadOnlyField(source='verified_by.full_name')

    class Meta:
        model = UtilityBill
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    facility_name = serializers.ReadOnlyField(source='facility.name')

    class Meta:
        model = Recommendation
        fields = '__all__'


class RenewableSystemSerializer(serializers.ModelSerializer):
    facility_name = serializers.ReadOnlyField(source='facility.name')

    class Meta:
        model = RenewableSystem
        fields = '__all__'


class RenewableGenerationLogSerializer(serializers.ModelSerializer):
    system_type = serializers.ReadOnlyField(source='system.system_type')
    facility_name = serializers.ReadOnlyField(source='system.facility.name')

    class Meta:
        model = RenewableGenerationLog
        fields = '__all__'


class DemandResponseEventSerializer(serializers.ModelSerializer):
    facility_name = serializers.ReadOnlyField(source='facility.name')

    class Meta:
        model = DemandResponseEvent
        fields = '__all__'
