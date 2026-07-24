from django.db import models
from django.contrib.auth.models import User


class WeatherRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_records')
    location = models.CharField(max_length=255)
    temperature = models.CharField(max_length=50)
    feels_like = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon_url = models.CharField(max_length=500)
    humidity = models.CharField(max_length=50)
    wind = models.CharField(max_length=50)
    date_recorded = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.location} - {self.date_recorded}"
