#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from .forms import WeatherForm
from .models import Town, Weather
from .excel_utils import WriteToExcel
from .pdf_utils import PdfPrint


def all_towns(request):
    towns = Town.objects.all()
    template_name = "exportingfiles/all_towns.html"
    context = {
        'towns': towns,
    }
    return render(request, template_name, context)


def today_weather(request):
    today = date.today()
    today_w = Weather.objects.filter(date=today)
    template_name = "exportingfiles/today_weather.html"
    context = {
        'today_weather': today_w
    }
    return render(request, template_name, context)


def weather_history(request):
    weather_period = Weather.objects.all()
    town = None
    if request.method == 'POST':
        form = WeatherForm(data=request.POST)
        if form.is_valid():
            town_id = form.data['town']
            town = Town.objects.get(pk=town_id)
            weather_period = Weather.objects.filter(town=town_id)
        if 'excel' in request.POST:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
            xlsx_data = WriteToExcel(weather_period, town)
            response.write(xlsx_data)
            return response
        if 'pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            today = date.today()
            filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
            response['Content-Disposition'] =\
                'attachement; filename={0}.pdf'.format(filename)
            buffer = BytesIO()
            report = PdfPrint(buffer, 'A4')
            pdf = report.report(weather_period, 'Weather statistics data')
            response.write(pdf)
            return response
    else:
        form = WeatherForm()

    template_name = "exportingfiles/weather_history.html"
    context = {
        'form': form,
        'town': town,
        'weather_period': weather_period,
    }
    return render(request, template_name, context)


def details(request, weather_id):
    weather = Weather.objects.get(pk=weather_id)
    template_name = "exportingfiles/details.html"
    context = {
        'weather': weather,
    }
    return render(request, template_name, context)
