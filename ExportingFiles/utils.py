from random import choice
from reportlab.lib.colors import HexColor
from .models import Weather, Town


def get_temperatures(values):
    temperatures = []
    t_min, t_max = (), ()
    days = []
    for v in values:
        date2str = v.date.strftime("%Y-%m-%d")
        days.append(date2str+"\n"+v.town.name)
        t_min += (v.min_temperature,)
        t_max += (v.max_temperature,)
    temperatures.append(t_max)
    temperatures.append(t_min)
    return temperatures, days


def get_days():
    days = []
    distinct_days = Weather.objects.values('date').distinct().order_by()
    for dd in distinct_days:
        days.append(dd['date'])
    return days


def get_str_days():
    strdays = []
    days = get_days()
    for d in days:
        date2str = d.strftime("%Y-%m-%d")
        strdays.append(date2str)
    return strdays


def get_wind_speed(values):
    speed = []
    strtowns = []
    days = get_days()
    towns = values.all().values('town').distinct().order_by()
    for t in towns:
        strtowns.append(Town.objects.get(pk=t['town']).name.encode('utf-8'))
    for t in towns:
        ws = values.filter(town__id=t['town'])
        town_wind = []
        for d in days:
            try:
                town_wind.append(ws.get(date=d).wind_speed)
            except:
                town_wind.append(0)
        speed.append(town_wind)
    return speed, strtowns


def get_random_colors(no_colors):
    # generate random hexa
    colors_list = []
    for i in range(no_colors):
        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colors_list.append(HexColor('#'+color))
    return colors_list


def precip_prob_sum(values):
    pp20 = 0
    pp40 = 0
    pp60 = 0
    pp80 = 0
    pp100 = 0
    for v in values:
        if v.precipitation_probability <= 20:
            pp20 += 1
        elif v.precipitation_probability > 20 and v.precipitation_probability <= 40:
            pp40 += 1
        elif v.precipitation_probability > 40 and v.precipitation_probability <= 60:
            pp60 += 1
        elif v.precipitation_probability > 60 and v.precipitation_probability <= 80:
            pp80 += 1
        else:
            pp100 += 1
    return [pp20, pp40, pp60, pp80, pp100]


def get_percentage(values):
    total = sum(values)
    percentage = []
    for value in values:
        v = round(value*100.0/total, 2)
        percentage.append(str(v)+" %")
    return percentage
