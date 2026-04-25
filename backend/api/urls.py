from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'farms', views.FarmViewSet, basename='farm')
router.register(r'crops', views.CropViewSet, basename='crop')
router.register(r'soil-data', views.SoilDataViewSet, basename='soil-data')
router.register(r'weather-data', views.WeatherDataViewSet, basename='weather-data')
router.register(r'market-data', views.MarketPriceViewSet, basename='market-data')
router.register(r'satellite-observations', views.SatelliteObservationViewSet, basename='satellite-observation')
router.register(r'irrigation-schedules', views.IrrigationScheduleViewSet, basename='irrigation-schedule')
router.register(r'yield-predictions', views.YieldPredictionViewSet, basename='yield-prediction')
router.register(r'digital-twin-simulations', views.DigitalTwinSimulationViewSet, basename='digital-twin-simulation')

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/token/', views.get_token, name='get_token'),
    path('predict/', views.predict, name='predict'),
    path('reports/', views.reports, name='reports'),
    path('market-prices/', views.market_prices, name='market_prices'),
    path('weather/', views.weather_info, name='weather_info'),
    path('integrations/weather/ingest/', views.ingest_weather, name='ingest_weather'),
    path('integrations/market/ingest/', views.ingest_market_prices, name='ingest_market_prices'),
    path('integrations/satellite/ingest/', views.ingest_satellite_observation, name='ingest_satellite_observation'),
    path('soil/recommend/', views.soil_recommendation, name='soil_recommendation'),
    path('irrigation/recommend/', views.irrigation_recommendation, name='irrigation_recommendation'),
    path('yield/predict/', views.yield_prediction, name='yield_prediction'),
    path('digital-twin/simulate/', views.digital_twin_simulation, name='digital_twin_simulation'),
    path('dashboard/summary/', views.smart_dashboard, name='smart_dashboard'),
    path('', include(router.urls)),
]
