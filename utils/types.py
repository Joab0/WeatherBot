from typing import Dict, Any, List

from datetime import datetime


class Location:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.name: str = data['name']
        self.region: str = data['region']
        self.country: str = data['country']
        self.lat: float = data['lat']
        self.lon: float = data['lon']
        self.tz_id: str = data['tz_id']
        self.localtime: datetime = datetime.fromtimestamp(data['localtime_epoch'])


class CurrentWeather:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.last_updated: datetime = datetime.fromtimestamp(data['last_updated_epoch'])
        self.temp_c: float = data['temp_c']
        self.temp_f: float = data['temp_f']
        self.is_day: bool = True if data['is_day'] else False
        self.condition_icon: str = data['condition']['icon']
        self.condition_code: int = data['condition']['code']
        self.wind_mph: float = data['wind_mph']
        self.wind_kph: float = data['wind_kph']
        self.wind_degree: int = data['wind_degree']
        self.wind_dir: str = data['wind_dir']
        self.pressure_mb: float = data['pressure_mb']
        self.pressure_in: float = data['pressure_in']
        self.precip_mm: float = data['precip_mm']
        self.precip_in: float = data['precip_in']
        self.humidity: int = data['humidity']
        self.cloud: int = data['cloud']
        self.feelslike_c: float = data['feelslike_c']
        self.feelslike_f: float = data['feelslike_f']
        self.vis_km: float = data['vis_km']
        self.vis_miles: float = data['vis_miles']
        self.uv: float = data['uv']
        self.gust_mph: float = data['gust_mph']
        self.gust_kph: float = data['gust_kph']


class ForecastDay:
    def __init__(self, data: Dict[str, Any]):
        self.date: datetime = datetime.fromtimestamp(data['date_epoch'])
        self.maxtemp_c: float = data['day']['maxtemp_c']
        self.maxtemp_f: float = data['day']['maxtemp_f']
        self.mintemp_c: float = data['day']['mintemp_c']
        self.mintemp_f: float = data['day']['mintemp_f']
        self.avgtemp_c: float = data['day']['avgtemp_c']
        self.avgtemp_f: float = data['day']['avgtemp_f']
        self.maxwind_mph: float = data['day']['maxwind_mph']
        self.maxwind_kph: float = data['day']['maxwind_kph']
        self.totalprecip_mm: float = data['day']['totalprecip_mm']
        self.totalprecip_in: float = data['day']['totalprecip_in']
        self.totalsnow_cm: float = data['day']['totalsnow_cm']
        self.avgvis_km: float = data['day']['avgvis_km']
        self.avgvis_miles: float = data['day']['avgvis_miles']
        self.avghumidity: float = data['day']['avghumidity']
        self.daily_will_it_rain: int = data['day']['daily_will_it_rain']
        self.daily_chance_of_rain: int = data['day']['daily_chance_of_rain']
        self.daily_will_it_snow: int = data['day']['daily_will_it_snow']
        self.daily_chance_of_snow: int = data['day']['daily_chance_of_snow']
        self.condition_icon: str = data['day']['condition']['icon']
        self.condition_code: int = data['day']['condition']['code']
        self.uv: int = data['day']['uv']


class WeatherAlert:
    def __init__(self, data: Dict[str, Any]):
        self.headline: str = data['headline']
        self.msgtype: str = data['msgtype']
        self.severity: str = data['severity']
        self.urgency: str = data['urgency']
        self.areas: str = data['areas']
        self.category: str = data['category']
        self.certainty: str = data['certainty']
        self.event: str = data['event']
        self.note: str = data['note']
        self.effective: datetime = datetime.fromisoformat(data['effective'])
        self.expires: datetime = datetime.fromisoformat(data['expires'])
        self.desc: str = data['desc']
        self.instruction: str = data['instruction']


class WeatherData:
    def __init__(self, data: Dict[str, Any]):
        self.location: Location = Location(data['location'])
        self.current: CurrentWeather = CurrentWeather(data['current'])
        self.forecast: List[ForecastDay] = [
            ForecastDay(day) for day in data['forecast']['forecastday']
        ]
        self.alerts: List[WeatherAlert] = [
            WeatherAlert(alert) for alert in data['alerts']['alert']
        ]
