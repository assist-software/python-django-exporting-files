from django.contrib import admin
from .models import Town, Weather


class TownAdmin(admin.ModelAdmin):
    list_display = ('name', 'county')
    ordering = ['county', 'name']


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('town', 'date')
    ordering = ['town', 'date']

admin.site.register(Town, TownAdmin)
admin.site.register(Weather, WeatherAdmin)
