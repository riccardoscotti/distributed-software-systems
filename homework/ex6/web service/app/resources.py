from flask import request, jsonify
from flask_restx import Resource, Namespace

import asyncio 
from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters

from datetime import datetime

from .api_models import *

ns = Namespace('api')

async def query_openmeteo(lat, long, daily_parameters, hourly_parameters):
    """Asyncronous function to query the OpenMeteo API."""
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=lat,
            longitude=long,
            daily=daily_parameters,
            hourly=hourly_parameters,
            timezone='CET'
        )

        return forecast


@ns.route('/check')
class Check(Resource):
    def get(self):
        """
        To use for checking if the webservice is up
        """
        return {
            'status': 'OK'
        }, 200

@ns.route('/current')
class Current(Resource):
    @ns.expect(loc_model)
    @ns.marshal_list_with(current_weather_model)
    def post(self):
        """
        Returns current weather data for a specific location.
        """
        try:
            # retrieving data from the request
            data = request.get_json()

            # retrieving coordinates 
            lat = data['lat']
            lon = data['lon']

            # running the query to OpenMeteo with selected parameters
            forecast = asyncio.run(query_openmeteo(
                lat, 
                lon, 
                [
                    DailyParameters.TEMPERATURE_2M_MIN,
                    DailyParameters.TEMPERATURE_2M_MAX,
                    DailyParameters.SUNRISE,
                    DailyParameters.SUNSET
                ], 
                [
                    HourlyParameters.TEMPERATURE_2M,
                    HourlyParameters.WIND_SPEED_10M,
                    HourlyParameters.WIND_DIRECTION_10M,
                    HourlyParameters.RELATIVE_HUMIDITY_2M,
                    HourlyParameters.PRECIPITATION
                ]
                ))
            
            # used to extract current data
            current_hour = datetime.now().hour
            hourly_data = forecast.hourly
            daily_data = forecast.daily
            return {
                'datetime': datetime.now().isoformat(),
                'minTemperature': daily_data.temperature_2m_min[0],
                'maxTemperature': daily_data.temperature_2m_max[0],
                'temperature': hourly_data.temperature_2m[current_hour],
                'windSpeed': hourly_data.wind_speed_10m[current_hour],
                'windDirection': hourly_data.wind_direction_10m[current_hour],
                'humidity': hourly_data.relative_humidity_2m[current_hour],
                'precipitation': hourly_data.precipitation[current_hour]
            }, 200
        
        except Exception as e:
            return {
                "error": str(e)
            }, 401


@ns.route('/hourly')
class Hourly(Resource):
    @ns.expect(loc_model)
    @ns.marshal_list_with(hourly_forecast_model)
    def post(self):
        """
        Returns weather data hour by hour in a given day.
        """
        try:
            # retrieving data from the request
            data = request.get_json()

            # retrieving coordinates 
            lat = data['lat']
            lon = data['lon']

            # running the query to OpenMeteo with selected parameters
            forecast = asyncio.run(query_openmeteo(
                lat, 
                lon, 
                [
                    DailyParameters.TEMPERATURE_2M_MIN,
                    DailyParameters.TEMPERATURE_2M_MAX,
                    DailyParameters.SUNRISE,
                    DailyParameters.SUNSET
                ], 
                [
                    HourlyParameters.TEMPERATURE_2M,
                    HourlyParameters.WIND_SPEED_10M,
                    HourlyParameters.WIND_DIRECTION_10M,
                    HourlyParameters.RELATIVE_HUMIDITY_2M,
                    HourlyParameters.PRECIPITATION
                ]
                ))
            
            hourly_data = forecast.hourly
            daily_data = forecast.daily

            hourly_forecast = []
            for index in range(24):
                hourly_forecast.append({
                    'temperature': hourly_data.temperature_2m[index],
                    'windSpeed': hourly_data.wind_speed_10m[index],
                    'windDirection': hourly_data.wind_direction_10m[index],
                    'humidity': hourly_data.relative_humidity_2m[index],
                    'precipitation': hourly_data.precipitation[index]
                })
            return {
                'date': datetime.now().isoformat(),
                'minTemperature': daily_data.temperature_2m_min[0],
                'maxTemperature': daily_data.temperature_2m_max[0],
                'hours': hourly_forecast
            }, 200
        except Exception as e:
            return {
                'Error': str(e)
            }, 401

@ns.route('/daily')
class Daily(Resource):
    @ns.expect(days_loc_model)
    @ns.marshal_list_with(daily_forecast_model)
    def post(self):
        """
        Returns weather data hour by hour in a given day.
        """
        try:
            # retrieving data from the request
            data = request.get_json()
            
            # retrieving number of days to get forecast of
            numDays = data['numDays']

            # if the days specified are outside the interval [1, 7], it is set to 
            # a default of 7, to replicate openmeteo API specification
            if numDays < 1 or numDays >=7:
                numDays = 7


            # retrieving coordinates 
            lat = data['loc']['lat']
            lon = data['loc']['lon']
            
            # running the query to OpenMeteo with selected parameters
            forecast = asyncio.run(query_openmeteo(
                lat, 
                lon, 
                [
                    DailyParameters.TEMPERATURE_2M_MIN,
                    DailyParameters.TEMPERATURE_2M_MAX,
                    DailyParameters.SUNRISE,
                    DailyParameters.SUNSET,
                    DailyParameters.PRECIPITATION_SUM
                ], 
                [
                    HourlyParameters.TEMPERATURE_2M,
                    HourlyParameters.WIND_SPEED_10M,
                    HourlyParameters.WIND_DIRECTION_10M,
                    HourlyParameters.RELATIVE_HUMIDITY_2M,
                    HourlyParameters.PRECIPITATION
                ]
                ))
            
            # hourly_data = forecast.hourly
            daily_data = forecast.daily

            daily_forecast = []
            print(daily_data.temperature_2m_max)
            for index in range(numDays):
                daily_forecast.append({
                    'date': daily_data.time[index].isoformat(),
                    'minTemperature': daily_data.temperature_2m_min[index],
                    'maxTemperature': daily_data.temperature_2m_max[index],
                    'sunrise': daily_data.sunrise[index].time().isoformat(),
                    'sunset': daily_data.sunset[index].time().isoformat(),
                    'precipitation': daily_data.precipitation_sum
                })
            return daily_forecast, 200
        
        except Exception as e:
            return {
                'Error': str(e)
            }, 401