from django.contrib import admin
from .models import (
    Crop,
    CropDiseaseReport,
    DigitalTwinSimulation,
    Farm,
    IrrigationSchedule,
    MarketPrice,
    SatelliteObservation,
    SoilData,
    WeatherData,
    YieldPrediction,
)

@admin.register(CropDiseaseReport)
class CropDiseaseReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm', 'crop', 'prediction', 'severity', 'confidence', 'timestamp')
    list_filter = ('prediction', 'severity', 'timestamp')
    search_fields = ('user__username', 'prediction')


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location_name', 'area_hectares', 'created_at')
    search_fields = ('name', 'user__username', 'location_name')


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'variety', 'season', 'status')
    list_filter = ('status', 'season')


@admin.register(SoilData)
class SoilDataAdmin(admin.ModelAdmin):
    list_display = ('farm', 'soil_type', 'soil_ph', 'soil_moisture', 'captured_at')
    list_filter = ('soil_type',)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('farm', 'temperature', 'humidity', 'rainfall_mm', 'forecast_for')
    list_filter = ('source',)


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'mandi_name', 'location', 'price_per_quintal', 'captured_at')
    list_filter = ('location', 'source')


@admin.register(SatelliteObservation)
class SatelliteObservationAdmin(admin.ModelAdmin):
    list_display = ('farm', 'source', 'ndvi', 'crop_stress_score', 'drought_risk', 'observed_at')
    list_filter = ('source', 'drought_risk', 'pest_risk')


@admin.register(IrrigationSchedule)
class IrrigationScheduleAdmin(admin.ModelAdmin):
    list_display = ('farm', 'crop', 'recommended_water_mm', 'irrigation_method', 'recommended_time')
    list_filter = ('irrigation_method',)


@admin.register(YieldPrediction)
class YieldPredictionAdmin(admin.ModelAdmin):
    list_display = ('farm', 'crop', 'expected_harvest_tons', 'profit_estimate', 'risk_level', 'created_at')
    list_filter = ('risk_level', 'model_name')


@admin.register(DigitalTwinSimulation)
class DigitalTwinSimulationAdmin(admin.ModelAdmin):
    list_display = ('farm', 'scenario_name', 'projected_yield_change_pct', 'projected_risk_level', 'created_at')
    list_filter = ('projected_risk_level',)
