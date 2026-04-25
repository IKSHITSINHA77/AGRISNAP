from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    CropDiseaseReport,
    Crop,
    DigitalTwinSimulation,
    Farm,
    IrrigationSchedule,
    MarketPrice,
    SatelliteObservation,
    SoilData,
    WeatherData,
    YieldPrediction,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CropDiseaseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropDiseaseReport
        fields = (
            'id',
            'user',
            'farm',
            'crop',
            'image',
            'prediction',
            'severity',
            'treatment',
            'recommended_pesticide',
            'confidence',
            'timestamp',
        )
        read_only_fields = ('prediction', 'severity', 'treatment', 'recommended_pesticide', 'confidence', 'timestamp')


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'
        read_only_fields = ('created_at',)


class SoilDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilData
        fields = '__all__'
        read_only_fields = ('captured_at',)


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'
        read_only_fields = ('created_at',)


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = '__all__'
        read_only_fields = ('captured_at',)


class SatelliteObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatelliteObservation
        fields = '__all__'
        read_only_fields = ('created_at',)


class IrrigationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationSchedule
        fields = '__all__'
        read_only_fields = ('created_at',)


class YieldPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldPrediction
        fields = '__all__'
        read_only_fields = ('created_at',)


class DigitalTwinSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalTwinSimulation
        fields = '__all__'
        read_only_fields = ('created_at',)
