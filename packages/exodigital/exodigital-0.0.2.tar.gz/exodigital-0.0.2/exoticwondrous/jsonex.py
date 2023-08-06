from typing import List
from typing import Any
from dataclasses import dataclass

# ExoDigit from exoticwondrous
# Telgram: https//exoticwondrous
# Ahmed Mohammmed
# ahmdsmhmmd@gmail.com   

#History revs:
# 08/08/2022 first release
# 26/08/2022
# shifted to ver.2 json-format.
#-- fixed bugs

@dataclass
class AreaName:
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'AreaName':
        _value = str(obj.get("value"))
        return AreaName(_value)

@dataclass
class Astronomy:
    moon_illumination: str
    moon_phase: str
    moonrise: str
    moonset: str
    sunrise: str
    sunset: str

    @staticmethod
    def from_dict(obj: Any) -> 'Astronomy':
        _moon_illumination = str(obj.get("moon_illumination"))
        _moon_phase = str(obj.get("moon_phase"))
        _moonrise = str(obj.get("moonrise"))
        _moonset = str(obj.get("moonset"))
        _sunrise = str(obj.get("sunrise"))
        _sunset = str(obj.get("sunset"))
        return Astronomy(_moon_illumination, _moon_phase, _moonrise, _moonset, _sunrise, _sunset)

@dataclass
class Country:
    value: str
    @staticmethod
    def from_dict(obj: Any) -> 'Country':
        _value = str(obj.get("value"))
        return Country(_value)

@dataclass
class WeatherDesc:
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherDesc':
        _value = str(obj.get("value"))
        return WeatherDesc(_value)

@dataclass
class WeatherIconUrl:
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherIconUrl':
        _value = str(obj.get("value"))
        return WeatherIconUrl(_value)

@dataclass
class WeatherUrl:
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherUrl':
        _value = str(obj.get("value"))
        return WeatherUrl(_value)

@dataclass
class Region:
    value: str
    @staticmethod
    def from_dict(obj: Any) -> 'Region':
        _value = str(obj.get("value"))
        return Region(_value)

@dataclass
class CurrentCondition:
    FeelsLikeC: str
    FeelsLikeF: str
    cloudcover: str
    humidity: str
    localObsDateTime: str
    observation_time: str
    precipInches: str
    precipMM: str
    pressure: str
    pressureInches: str
    temp_C: str
    temp_F: str
    uvIndex: str
    visibility: str
    visibilityMiles: str
    weatherCode: str
    weatherDesc: WeatherDesc
    weatherIconUrl: WeatherIconUrl
    winddir16Point: str
    winddirDegree: str
    windspeedKmph: str
    windspeedMiles: str

    @staticmethod
    def from_dict(obj: Any) -> 'CurrentCondition':
        _FeelsLikeC = str(obj.get("FeelsLikeC"))
        _FeelsLikeF = str(obj.get("FeelsLikeF"))
        _cloudcover = str(obj.get("cloudcover"))
        _humidity = str(obj.get("humidity"))
        _localObsDateTime = str(obj.get("localObsDateTime"))
        _observation_time = str(obj.get("observation_time"))
        _precipInches = str(obj.get("precipInches"))
        _precipMM = str(obj.get("precipMM"))
        _pressure = str(obj.get("pressure"))
        _pressureInches = str(obj.get("pressureInches"))
        _temp_C = str(obj.get("temp_C"))
        _temp_F = str(obj.get("temp_F"))
        _uvIndex = str(obj.get("uvIndex"))
        _visibility = str(obj.get("visibility"))
        _visibilityMiles = str(obj.get("visibilityMiles"))
        _weatherCode = str(obj.get("weatherCode"))
        _weatherDesc = [WeatherDesc.from_dict(y) for y in obj.get("weatherDesc")]
        _weatherIconUrl = [WeatherIconUrl.from_dict(y) for y in obj.get("weatherIconUrl")]
        _winddir16Point = str(obj.get("winddir16Point"))
        _winddirDegree = str(obj.get("winddirDegree"))
        _windspeedKmph = str(obj.get("windspeedKmph"))
        _windspeedMiles = str(obj.get("windspeedMiles"))
        return CurrentCondition(_FeelsLikeC, _FeelsLikeF, _cloudcover, _humidity, _localObsDateTime, _observation_time, _precipInches, _precipMM, _pressure, _pressureInches, _temp_C, _temp_F, _uvIndex, _visibility, _visibilityMiles, _weatherCode, _weatherDesc[0], _weatherIconUrl[0], _winddir16Point, _winddirDegree, _windspeedKmph, _windspeedMiles)

@dataclass
class NearestArea:
    areaName: AreaName
    country: Country
    latitude: str
    longitude: str
    population: str
    region: Region
    weatherUrl: WeatherUrl

    @staticmethod
    def from_dict(obj: Any) -> 'NearestArea':
        _areaName = [AreaName.from_dict(y) for y in obj.get("areaName")]
        _country = [Country.from_dict(y) for y in obj.get("country")]
        _latitude = str(obj.get("latitude"))
        _longitude = str(obj.get("longitude"))
        _population = str(obj.get("population"))
        _region = [Region.from_dict(y) for y in obj.get("region")]
        _weatherUrl = [WeatherUrl.from_dict(y) for y in obj.get("weatherUrl")]
        return NearestArea(_areaName[0], _country[0], _latitude, _longitude, _population, _region[0], _weatherUrl[0])

@dataclass
class Request:
    query: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Request':
        _query = str(obj.get("query"))
        _type = str(obj.get("type"))
        return Request(_query, _type)

@dataclass
class Weather:
    astronomy: Astronomy
    avgtempC: str
    avgtempF: str
    date: str
    maxtempC: str
    maxtempF: str
    mintempC: str
    mintempF: str
    sunHour: str
    totalSnow_cm: str
    uvIndex: str

    @staticmethod
    def from_dict(obj: Any) -> 'Weather':
        _astronomy = [Astronomy.from_dict(y) for y in obj.get("astronomy")]
        _avgtempC = str(obj.get("avgtempC"))
        _avgtempF = str(obj.get("avgtempF"))
        _date = str(obj.get("date"))
        _maxtempC = str(obj.get("maxtempC"))
        _maxtempF = str(obj.get("maxtempF"))
        _mintempC = str(obj.get("mintempC"))
        _mintempF = str(obj.get("mintempF"))
        _sunHour = str(obj.get("sunHour"))
        _totalSnow_cm = str(obj.get("totalSnow_cm"))
        _uvIndex = str(obj.get("uvIndex"))
        return Weather(_astronomy[0], _avgtempC, _avgtempF, _date, _maxtempC, _maxtempF, _mintempC, _mintempF, _sunHour, _totalSnow_cm, _uvIndex)

@dataclass
class Root:
    current_condition: CurrentCondition
    nearest_area: NearestArea
    request: Request
    weather: Weather

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _current_condition = [CurrentCondition.from_dict(y) for y in obj.get("current_condition")]
        _nearest_area = [NearestArea.from_dict(y) for y in obj.get("nearest_area")]
        _request = [Request.from_dict(y) for y in obj.get("request")]
        _weather = [Weather.from_dict(y) for y in obj.get("weather")]
        return Root(_current_condition[0], _nearest_area[0], _request[0], _weather[0])
