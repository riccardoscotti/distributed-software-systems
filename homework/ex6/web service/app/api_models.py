from flask_restx import fields 

from .extensions import api 

loc_model = api.model('Location', {
    'lat': fields.Float,
    'lon': fields.Float
})

days_loc_model = api.model('Daily forecast request', {
    'numDays': fields.Integer,
    'loc': fields.Nested(loc_model)
})

current_weather_model = api.model('Weather data', {
    'datetime': fields.String,
    'minTemperature': fields.Float,
    'maxTemperature': fields.Float,
    'temperature': fields.Float,
    'windSpeed': fields.Float,
    'windDirection': fields.Float,
    'humidity': fields.Float,
    'precipitation': fields.Float
})

hour_data_model = api.model('Hour data model', {
    'temperature': fields.Float,
    'windSpeed': fields.Float,
    'windDirection': fields.Float,
    'humidity': fields.Float,
    'precipitation': fields.Float
})

hourly_forecast_model = api.model('Hourly forecast', {
    'date': fields.String,
    'minTemperature': fields.Float,
    'maxTemperature': fields.Float,
    'hours': fields.List(fields.Nested(hour_data_model))
})

daily_forecast_model = api.model('Daily forecast', {
    'date': fields.String,
    'minTemperature': fields.Float,
    'maxTemperature': fields.Float,
    'sunrise': fields.String,
    'sunset': fields.String,
    'precipitation': fields.String
})