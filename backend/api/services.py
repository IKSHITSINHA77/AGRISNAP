from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from django.conf import settings


@dataclass
class ServiceResult:
    ok: bool
    data: Dict[str, Any]
    error: str = ""


def _safe_get(url: str, params: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> ServiceResult:
    try:
        response = requests.get(url, params=params, headers=headers or {}, timeout=settings.ML_INFERENCE_TIMEOUT_SECONDS)
        response.raise_for_status()
        return ServiceResult(ok=True, data=response.json())
    except requests.RequestException as exc:
        return ServiceResult(ok=False, data={}, error=str(exc))


def fetch_weather_forecast(lat: float, lon: float) -> ServiceResult:
    if not settings.OPENWEATHER_API_KEY:
        return ServiceResult(
            ok=False,
            data={},
            error="OPENWEATHER_API_KEY is missing",
        )

    url = f"{settings.OPENWEATHER_BASE_URL}/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
    }
    result = _safe_get(url, params=params)
    if not result.ok:
        return result

    first = (result.data.get("list") or [{}])[0]
    main = first.get("main") or {}
    rain = first.get("rain") or {}
    wind = first.get("wind") or {}
    weather_list = first.get("weather") or [{}]
    weather_item = weather_list[0] if weather_list else {}
    city = result.data.get("city") or {}

    parsed = {
        "source": "openweather",
        "temperature": main.get("temp", 0),
        "humidity": main.get("humidity", 0),
        "rainfall_mm": rain.get("3h", 0.0),
        "wind_speed_kmph": round(float(wind.get("speed", 0)) * 3.6, 2),
        "condition": weather_item.get("description", "Unknown"),
        "location": city.get("name", "Unknown"),
        "forecast_for": first.get("dt_txt"),
    }
    return ServiceResult(ok=True, data=parsed)


def fetch_market_prices(crop_name: str, location: str = "") -> ServiceResult:
    if not settings.MARKET_API_BASE_URL:
        return ServiceResult(
            ok=False,
            data={},
            error="MARKET_API_BASE_URL is missing",
        )

    params = {"crop": crop_name}
    if location:
        params["location"] = location
    headers = {"Authorization": f"Bearer {settings.MARKET_API_KEY}"} if settings.MARKET_API_KEY else {}
    result = _safe_get(settings.MARKET_API_BASE_URL, params=params, headers=headers)
    if not result.ok:
        return result

    entries = result.data.get("data") if isinstance(result.data, dict) else result.data
    if not entries:
        return ServiceResult(ok=False, data={}, error="No market entries returned")
    return ServiceResult(ok=True, data={"entries": entries})


def run_disease_inference(image_url: str) -> ServiceResult:
    if not settings.ML_INFERENCE_URL:
        return ServiceResult(
            ok=False,
            data={},
            error="ML_INFERENCE_URL is missing",
        )

    try:
        response = requests.post(
            settings.ML_INFERENCE_URL,
            json={"image_url": image_url},
            timeout=settings.ML_INFERENCE_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        return ServiceResult(ok=True, data=payload)
    except requests.RequestException as exc:
        return ServiceResult(ok=False, data={}, error=str(exc))
