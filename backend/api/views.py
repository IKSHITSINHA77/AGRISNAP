from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.utils import timezone
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
from .serializers import (
    CropDiseaseReportSerializer,
    CropSerializer,
    DigitalTwinSimulationSerializer,
    FarmSerializer,
    IrrigationScheduleSerializer,
    MarketPriceSerializer,
    RegisterSerializer,
    SatelliteObservationSerializer,
    SoilDataSerializer,
    UserSerializer,
    WeatherDataSerializer,
    YieldPredictionSerializer,
)
from .services import fetch_market_prices, fetch_weather_forecast, run_disease_inference


SOIL_CROP_GUIDANCE = {
    'alluvial': ['Rice', 'Wheat', 'Sugarcane'],
    'black': ['Cotton', 'Soybean', 'Sorghum'],
    'red': ['Millets', 'Pulses', 'Groundnut'],
    'laterite': ['Tea', 'Coffee', 'Cashew'],
    'desert': ['Barley', 'Bajra', 'Guar'],
    'mountain': ['Apple', 'Pear', 'Potato'],
    'other': ['Wheat', 'Maize'],
}


def _risk_from_values(soil_moisture, ph, rainfall):
    score = 0
    if soil_moisture < 20:
        score += 2
    if ph < 5.5 or ph > 8.0:
        score += 1
    if rainfall < 5:
        score += 1
    if score >= 3:
        return 'high'
    if score == 2:
        return 'medium'
    return 'low'


def _soil_recommendation_payload(soil_data):
    recommended_crop = SOIL_CROP_GUIDANCE.get(soil_data.soil_type, SOIL_CROP_GUIDANCE['other'])[0]

    fertilizer = []
    if soil_data.nitrogen_level < 40:
        fertilizer.append('Nitrogen-rich fertilizer (Urea / Ammonium Sulphate)')
    if soil_data.phosphorus_level < 20:
        fertilizer.append('Phosphorus booster (DAP / SSP)')
    if soil_data.potassium_level < 150:
        fertilizer.append('Potassium source (MOP)')
    if soil_data.organic_matter < 1.5:
        fertilizer.append('Compost / farmyard manure')
    if not fertilizer:
        fertilizer.append('Balanced NPK with micronutrient blend')

    if soil_data.soil_moisture < 25:
        irrigation = 'Irrigate every 1-2 days with drip in short cycles'
    elif soil_data.soil_moisture < 40:
        irrigation = 'Irrigate every 3-4 days and monitor root-zone moisture'
    else:
        irrigation = 'Irrigate every 5-7 days based on evapotranspiration'

    yield_prediction = max(1.0, round((soil_data.nitrogen_level + soil_data.phosphorus_level + soil_data.potassium_level) / 120, 2))
    return {
        'best_crop': recommended_crop,
        'fertilizer_recommendation': fertilizer,
        'irrigation_schedule': irrigation,
        'yield_prediction_tons_per_hectare': yield_prediction,
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def predict(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    
    # Baseline response until production CNN/YOLO model is integrated.
    prediction = "Healthy Crop"
    confidence = 0.95
    severity = "low"
    treatment = "Continue regular monitoring and balanced nutrition."
    recommended_pesticide = "Not required"
    
    report = CropDiseaseReport.objects.create(
        user=request.user if request.user.is_authenticated else None,
        farm_id=request.data.get('farm'),
        crop_id=request.data.get('crop'),
        image=image,
        prediction=prediction,
        severity=severity,
        treatment=treatment,
        recommended_pesticide=recommended_pesticide,
        confidence=confidence
    )

    # If ML inference service is configured, enrich the report.
    image_url = request.build_absolute_uri(report.image.url)
    ml_result = run_disease_inference(image_url=image_url)
    if ml_result.ok:
        payload = ml_result.data
        report.prediction = payload.get('disease_name', report.prediction)
        report.confidence = float(payload.get('confidence', report.confidence))
        report.severity = payload.get('severity', report.severity)
        report.treatment = payload.get('treatment', report.treatment)
        report.recommended_pesticide = payload.get('recommended_pesticide', report.recommended_pesticide)
        report.save(update_fields=['prediction', 'confidence', 'severity', 'treatment', 'recommended_pesticide'])
    
    serializer = CropDiseaseReportSerializer(report)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def reports(request):
    if request.user.is_authenticated:
        reports = CropDiseaseReport.objects.filter(user=request.user)
    else:
        reports = CropDiseaseReport.objects.all()
    
    serializer = CropDiseaseReportSerializer(reports, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def market_prices(request):
    crop = request.query_params.get('crop')
    qs = MarketPrice.objects.all().order_by('-captured_at')
    if crop:
        qs = qs.filter(crop_name__iexact=crop)
    if qs.exists():
        return Response(MarketPriceSerializer(qs[:50], many=True).data)

    return Response({
        'wheat': {'price': 2100, 'unit': 'quintal', 'location': 'Delhi'},
        'rice': {'price': 2900, 'unit': 'quintal', 'location': 'Punjab'},
        'maize': {'price': 1850, 'unit': 'quintal', 'location': 'Haryana'},
        'cotton': {'price': 6200, 'unit': 'quintal', 'location': 'Gujarat'},
        'soybean': {'price': 4200, 'unit': 'quintal', 'location': 'Madhya Pradesh'},
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def weather_info(request):
    farm_id = request.query_params.get('farm_id')
    qs = WeatherData.objects.all().order_by('-forecast_for')
    if farm_id:
        qs = qs.filter(farm_id=farm_id)
    if qs.exists():
        return Response(WeatherDataSerializer(qs[:24], many=True).data)

    return Response({
        'temperature': 28,
        'humidity': 65,
        'condition': 'Partly Cloudy',
        'rainfall': 0,
        'wind_speed': 12,
        'location': 'Default Location'
    })


@api_view(['POST'])
def ingest_weather(request):
    farm_id = request.data.get('farm_id')
    if not farm_id:
        return Response({'error': 'farm_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    farm = Farm.objects.filter(id=farm_id).first()
    if not farm:
        return Response({'error': 'Farm not found'}, status=status.HTTP_404_NOT_FOUND)
    if farm.latitude is None or farm.longitude is None:
        return Response({'error': 'Farm latitude/longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

    service_result = fetch_weather_forecast(float(farm.latitude), float(farm.longitude))
    if not service_result.ok:
        return Response({'error': service_result.error}, status=status.HTTP_502_BAD_GATEWAY)

    payload = service_result.data
    weather_record = WeatherData.objects.create(
        farm=farm,
        source=payload.get('source', 'openweather'),
        temperature=payload.get('temperature', 0),
        humidity=payload.get('humidity', 0),
        rainfall_mm=payload.get('rainfall_mm', 0),
        wind_speed_kmph=payload.get('wind_speed_kmph', 0),
        condition=payload.get('condition', ''),
        forecast_for=payload.get('forecast_for') or timezone.now(),
    )
    return Response(WeatherDataSerializer(weather_record).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def ingest_market_prices(request):
    crop_name = request.data.get('crop_name')
    location = request.data.get('location', '')
    if not crop_name:
        return Response({'error': 'crop_name is required'}, status=status.HTTP_400_BAD_REQUEST)

    service_result = fetch_market_prices(crop_name=crop_name, location=location)
    if not service_result.ok:
        return Response({'error': service_result.error}, status=status.HTTP_502_BAD_GATEWAY)

    created_records = []
    for item in service_result.data.get('entries', []):
        record = MarketPrice.objects.create(
            crop_name=item.get('crop_name', crop_name),
            mandi_name=item.get('mandi_name', item.get('market', 'Unknown')),
            location=item.get('location', location or 'Unknown'),
            price_per_quintal=float(item.get('price_per_quintal', item.get('price', 0))),
            currency=item.get('currency', 'INR'),
            source=item.get('source', 'external-market-api'),
        )
        created_records.append(record)

    return Response(MarketPriceSerializer(created_records, many=True).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def ingest_satellite_observation(request):
    serializer = SatelliteObservationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return Response({
        'observation': SatelliteObservationSerializer(instance).data,
        'insights': {
            'crop_stress_alert': instance.crop_stress_score > 0.7,
            'drought_warning': instance.drought_risk in {'medium', 'high'},
            'recommended_action': 'Increase field scouting and irrigation scheduling' if instance.crop_stress_score > 0.7 else 'Maintain current plan',
        },
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def soil_recommendation(request):
    serializer = SoilDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    soil_data = serializer.save()
    return Response({
        'soil_data': SoilDataSerializer(soil_data).data,
        'recommendation': _soil_recommendation_payload(soil_data),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def irrigation_recommendation(request):
    farm_id = request.data.get('farm_id')
    crop_id = request.data.get('crop_id')

    if not farm_id:
        return Response({'error': 'farm_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    latest_soil = SoilData.objects.filter(farm_id=farm_id).order_by('-captured_at').first()
    latest_weather = WeatherData.objects.filter(farm_id=farm_id).order_by('-forecast_for').first()

    if not latest_soil:
        return Response({'error': 'No soil data available for this farm'}, status=status.HTTP_404_NOT_FOUND)

    rainfall = latest_weather.rainfall_mm if latest_weather else 0.0
    water_required = max(8.0, 35.0 - latest_soil.soil_moisture - (rainfall * 0.4))
    method = 'drip' if water_required < 20 else 'sprinkler'
    advisory = (
        f"Recommended {round(water_required, 2)} mm water using {method}. "
        "Prefer early morning irrigation and avoid peak afternoon heat."
    )

    payload = {
        'farm': farm_id,
        'crop': crop_id,
        'recommended_water_mm': round(water_required, 2),
        'recommended_time': request.data.get('recommended_time'),
        'irrigation_method': method,
        'advisory': advisory,
    }
    schedule_serializer = IrrigationScheduleSerializer(data=payload)
    schedule_serializer.is_valid(raise_exception=True)
    schedule_serializer.save()
    return Response(schedule_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def yield_prediction(request):
    farm_id = request.data.get('farm_id')
    crop_id = request.data.get('crop_id')
    if not farm_id or not crop_id:
        return Response({'error': 'farm_id and crop_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    soil = SoilData.objects.filter(farm_id=farm_id).order_by('-captured_at').first()
    weather = WeatherData.objects.filter(farm_id=farm_id).order_by('-forecast_for').first()
    crop = Crop.objects.filter(id=crop_id, farm_id=farm_id).first()
    if not crop:
        return Response({'error': 'Crop not found for farm'}, status=status.HTTP_404_NOT_FOUND)
    if not soil:
        return Response({'error': 'Soil data required before yield prediction'}, status=status.HTTP_400_BAD_REQUEST)

    rainfall = weather.rainfall_mm if weather else 0.0
    productivity = (soil.nitrogen_level + soil.phosphorus_level + soil.potassium_level) / 100
    moisture_factor = max(0.6, min(1.25, soil.soil_moisture / 35))
    weather_factor = 1.05 if 10 <= rainfall <= 45 else 0.88
    expected_harvest_tons = round(max(0.5, crop.area_hectares * productivity * moisture_factor * weather_factor), 2)
    profit_estimate = round(expected_harvest_tons * 21000, 2)
    risk_level = _risk_from_values(soil.soil_moisture, soil.soil_ph, rainfall)

    model_payload = {
        'farm': farm_id,
        'crop': crop_id,
        'expected_harvest_tons': expected_harvest_tons,
        'profit_estimate': profit_estimate,
        'risk_level': risk_level,
        'model_name': 'xgboost-ready-baseline',
        'input_snapshot': {
            'soil_ph': soil.soil_ph,
            'soil_moisture': soil.soil_moisture,
            'npk': [soil.nitrogen_level, soil.phosphorus_level, soil.potassium_level],
            'rainfall_mm': rainfall,
        },
    }
    prediction_serializer = YieldPredictionSerializer(data=model_payload)
    prediction_serializer.is_valid(raise_exception=True)
    prediction_serializer.save()
    return Response(prediction_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def digital_twin_simulation(request):
    farm_id = request.data.get('farm_id')
    if not farm_id:
        return Response({'error': 'farm_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    assumptions = request.data.get('assumptions', {})
    rainfall_change = float(assumptions.get('rainfall_change_pct', 0))
    fertilizer_change = float(assumptions.get('fertilizer_change_pct', 0))
    irrigation_change = float(assumptions.get('irrigation_change_pct', 0))

    projected_yield_change = round((fertilizer_change * 0.35) + (irrigation_change * 0.3) - (max(0, -rainfall_change) * 0.25), 2)
    projected_water_change = round(irrigation_change - (rainfall_change * 0.2), 2)
    projected_risk = 'high' if rainfall_change < -20 else 'medium' if rainfall_change < -5 else 'low'

    result = {
        'farm': farm_id,
        'scenario_name': request.data.get('scenario_name', 'Digital Twin Scenario'),
        'assumptions': assumptions,
        'projected_yield_change_pct': projected_yield_change,
        'projected_water_change_pct': projected_water_change,
        'projected_risk_level': projected_risk,
        'recommendations': {
            'crop_switch': 'Consider drought-resistant variety' if projected_risk == 'high' else 'Current crop plan is acceptable',
            'fertilizer_plan': 'Increase organic matter and split N-application',
            'irrigation_plan': 'Adopt drip with moisture-sensor based schedules',
        },
    }
    serializer = DigitalTwinSimulationSerializer(data=result)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def smart_dashboard(request):
    farm_id = request.query_params.get('farm_id')
    farm_qs = Farm.objects.all()
    if farm_id:
        farm_qs = farm_qs.filter(id=farm_id)

    soil_qs = SoilData.objects.filter(farm__in=farm_qs)
    weather_qs = WeatherData.objects.filter(farm__in=farm_qs)
    yield_qs = YieldPrediction.objects.filter(farm__in=farm_qs)

    payload = {
        'farms_count': farm_qs.count(),
        'soil_health_index': round((soil_qs.aggregate(avg_ph=Avg('soil_ph'))['avg_ph'] or 0) * 12, 2),
        'avg_soil_moisture': round(soil_qs.aggregate(avg=Avg('soil_moisture'))['avg'] or 0, 2),
        'avg_temperature': round(weather_qs.aggregate(avg=Avg('temperature'))['avg'] or 0, 2),
        'water_usage_signal': 'optimized' if (soil_qs.aggregate(avg=Avg('soil_moisture'))['avg'] or 0) > 28 else 'needs attention',
        'yield_forecast_tons': round(yield_qs.aggregate(total=Avg('expected_harvest_tons'))['total'] or 0, 2),
    }
    return Response(payload)


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all().order_by('-created_at')
    serializer_class = FarmSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            serializer.save(user=user)
        else:
            serializer.save(user_id=self.request.data.get('user'))


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all().order_by('-created_at')
    serializer_class = CropSerializer


class SoilDataViewSet(viewsets.ModelViewSet):
    queryset = SoilData.objects.all().order_by('-captured_at')
    serializer_class = SoilDataSerializer

    @action(detail=True, methods=['get'])
    def recommendation(self, request, pk=None):
        soil_data = self.get_object()
        return Response(_soil_recommendation_payload(soil_data))


class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all().order_by('-forecast_for')
    serializer_class = WeatherDataSerializer


class MarketPriceViewSet(viewsets.ModelViewSet):
    queryset = MarketPrice.objects.all().order_by('-captured_at')
    serializer_class = MarketPriceSerializer


class SatelliteObservationViewSet(viewsets.ModelViewSet):
    queryset = SatelliteObservation.objects.all().order_by('-observed_at')
    serializer_class = SatelliteObservationSerializer


class IrrigationScheduleViewSet(viewsets.ModelViewSet):
    queryset = IrrigationSchedule.objects.all().order_by('-recommended_time')
    serializer_class = IrrigationScheduleSerializer


class YieldPredictionViewSet(viewsets.ModelViewSet):
    queryset = YieldPrediction.objects.all().order_by('-created_at')
    serializer_class = YieldPredictionSerializer


class DigitalTwinSimulationViewSet(viewsets.ModelViewSet):
    queryset = DigitalTwinSimulation.objects.all().order_by('-created_at')
    serializer_class = DigitalTwinSimulationSerializer
