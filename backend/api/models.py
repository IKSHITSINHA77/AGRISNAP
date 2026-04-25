from django.db import models
from django.contrib.auth.models import User


class Farm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=150)
    location_name = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    area_hectares = models.FloatField(default=0.0)
    boundary_geojson = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Crop(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=120)
    variety = models.CharField(max_length=120, blank=True)
    season = models.CharField(max_length=80, blank=True)
    sowing_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    area_hectares = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.farm.name}"


class SoilData(models.Model):
    SOIL_TYPES = [
        ('alluvial', 'Alluvial Soil'),
        ('black', 'Black Soil'),
        ('red', 'Red Soil'),
        ('laterite', 'Laterite Soil'),
        ('desert', 'Desert Soil'),
        ('mountain', 'Mountain Soil'),
        ('other', 'Other'),
    ]
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='soil_readings')
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES, default='other')
    soil_ph = models.FloatField()
    soil_moisture = models.FloatField(help_text='Percentage')
    nitrogen_level = models.FloatField(help_text='mg/kg')
    phosphorus_level = models.FloatField(help_text='mg/kg')
    potassium_level = models.FloatField(help_text='mg/kg')
    organic_matter = models.FloatField(help_text='Percentage')
    soil_temperature = models.FloatField(help_text='Celsius')
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SoilData({self.farm.name}, pH={self.soil_ph})"


class WeatherData(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_data')
    source = models.CharField(max_length=80, default='manual')
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall_mm = models.FloatField(default=0.0)
    wind_speed_kmph = models.FloatField(default=0.0)
    condition = models.CharField(max_length=120, blank=True)
    forecast_for = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather({self.farm.name}, {self.forecast_for.date()})"


class MarketPrice(models.Model):
    crop_name = models.CharField(max_length=120)
    mandi_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    price_per_quintal = models.FloatField()
    currency = models.CharField(max_length=10, default='INR')
    source = models.CharField(max_length=120, default='manual')
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} @ {self.mandi_name}"


class SatelliteObservation(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='satellite_observations')
    source = models.CharField(max_length=120, default='sentinel')
    ndvi = models.FloatField(null=True, blank=True)
    moisture_index = models.FloatField(null=True, blank=True)
    crop_stress_score = models.FloatField(default=0.0)
    drought_risk = models.CharField(max_length=20, default='low')
    pest_risk = models.CharField(max_length=20, default='low')
    raw_payload = models.JSONField(default=dict, blank=True)
    observed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Satellite({self.farm.name}, stress={self.crop_stress_score})"


class IrrigationSchedule(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='irrigation_schedules')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='irrigation_schedules', null=True, blank=True)
    recommended_water_mm = models.FloatField()
    recommended_time = models.DateTimeField()
    irrigation_method = models.CharField(max_length=50, default='drip')
    advisory = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Irrigation({self.farm.name}, {self.recommended_time})"


class YieldPrediction(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='yield_predictions')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='yield_predictions')
    expected_harvest_tons = models.FloatField()
    profit_estimate = models.FloatField()
    risk_level = models.CharField(max_length=20, default='medium')
    model_name = models.CharField(max_length=80, default='rule-based-baseline')
    input_snapshot = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Yield({self.crop.name}, {self.expected_harvest_tons}t)"


class DigitalTwinSimulation(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='digital_twin_runs')
    scenario_name = models.CharField(max_length=150)
    assumptions = models.JSONField(default=dict, blank=True)
    projected_yield_change_pct = models.FloatField(default=0.0)
    projected_water_change_pct = models.FloatField(default=0.0)
    projected_risk_level = models.CharField(max_length=20, default='medium')
    recommendations = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DigitalTwin({self.farm.name}, {self.scenario_name})"


class CropDiseaseReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True, blank=True, related_name='disease_reports')
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name='disease_reports')
    image = models.ImageField(upload_to='disease_reports/')
    prediction = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, default='low')
    treatment = models.TextField(blank=True)
    recommended_pesticide = models.CharField(max_length=200, blank=True)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.prediction}"
