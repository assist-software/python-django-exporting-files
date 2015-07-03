#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Town, Weather


def WriteToExcel(weather_data, town=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Summary")

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    # write title
    if town:
        town_text = town.name
    else:
        town_text = ugettext("all recorded towns")
    title_text = u"{0} {1}".format(ugettext("Weather History for"), town_text)
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext("No"), header)
    worksheet_s.write(4, 1, ugettext("Town"), header)
    worksheet_s.write(4, 2, ugettext("Date"), header)
    worksheet_s.write(4, 3, ugettext("Description"), header)
    worksheet_s.write(4, 4, ugettext(u"Max T. (℃)"), header)
    worksheet_s.write(4, 5, ugettext(u"Min T. (℃)"), header)
    worksheet_s.write(4, 6, ugettext("Wind (km/h)"), header)
    worksheet_s.write(4, 7, ugettext("Precip. (mm)"), header)
    worksheet_s.write(4, 8, ugettext("Precip. (%)"), header)
    worksheet_s.write(4, 9, ugettext("Observations"), header)

    # column widths
    town_col_width = 10
    description_col_width = 10
    observations_col_width = 25

    # add data to the table
    for idx, data in enumerate(weather_data):
        row = 5 + idx
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        worksheet_s.write_string(row, 1, data.town.name, cell)
        if len(data.town.name) > town_col_width:
            town_col_width = len(data.town.name)

        worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)
        worksheet_s.write_string(row, 3, data.description, cell)
        if len(data.description) > description_col_width:
            description_col_width = len(data.description)

        worksheet_s.write_number(row, 4, data.max_temperature, cell_center)
        worksheet_s.write_number(row, 5, data.min_temperature, cell_center)
        worksheet_s.write_number(row, 6, data.wind_speed, cell_center)
        worksheet_s.write_number(row, 7, data.precipitation, cell_center)
        worksheet_s.write_number(row, 8,
                                 data.precipitation_probability, cell_center)

        observations = data.observations.replace('\r', '')
        worksheet_s.write_string(row, 9, observations, cell)
        observations_rows = compute_rows(observations, observations_col_width)
        worksheet_s.set_row(row, 15 * observations_rows)

    # change column widths
    worksheet_s.set_column('B:B', town_col_width)  # Town column
    worksheet_s.set_column('C:C', 11)  # Date column
    worksheet_s.set_column('D:D', description_col_width)  # Description column
    worksheet_s.set_column('E:E', 10)  # Max Temp column
    worksheet_s.set_column('F:F', 10)  # Min Temp column
    worksheet_s.set_column('G:G', 10)  # Wind Speed column
    worksheet_s.set_column('H:H', 11)  # Precipitation column
    worksheet_s.set_column('I:I', 11)  # Precipitation % column
    worksheet_s.set_column('J:J', observations_col_width)  # Observations column

    row = row + 1
    # Adding some functions for the data
    max_temp_avg = Weather.objects.all().aggregate(Avg('max_temperature'))
    worksheet_s.write_formula(row, 4,
                              '=average({0}{1}:{0}{2})'.format('E', 6, row),
                              cell_center,
                              max_temp_avg['max_temperature__avg'])
    min_temp_avg = Weather.objects.all().aggregate(Avg('min_temperature'))
    worksheet_s.write_formula(row, 5,
                              '=average({0}{1}:{0}{2})'.format('F', 6, row),
                              cell_center,
                              min_temp_avg['min_temperature__avg'])
    wind_avg = Weather.objects.all().aggregate(Avg('wind_speed'))
    worksheet_s.write_formula(row, 6,
                              '=average({0}{1}:{0}{2})'.format('G', 6, row),
                              cell_center,
                              wind_avg['wind_speed__avg'])
    precip_sum = Weather.objects.all().aggregate(Sum('precipitation'))
    worksheet_s.write_formula(row, 7,
                              '=sum({0}{1}:{0}{2})'.format('H', 6, row),
                              cell_center,
                              precip_sum['precipitation__sum'])
    precip_prob_avg = Weather.objects.all() \
        .aggregate(Avg('precipitation_probability'))
    worksheet_s.write_formula(row, 8,
                              '=average({0}{1}:{0}{2})'.format('I', 6, row),
                              cell_center,
                              precip_prob_avg['precipitation_probability__avg'])

    # add more Sheets
    worksheet_c = workbook.add_worksheet("Charts")
    worksheet_d = workbook.add_worksheet("Chart Data")

    if town:
        towns = [town]
    else:
        towns = Town.objects.all()

    # Creating the Line Chart
    line_chart = workbook.add_chart({'type': 'line'})
    # adding dates for the values
    dates = Weather.objects.order_by('date').filter(
        town=Town.objects.first()).values_list('date', flat=True)
    str_dates = []
    for d in dates:
        str_dates.append(d.strftime('%d/%m/%Y'))
    worksheet_d.write_column('A1', str_dates)
    worksheet_d.set_column('A:A', 10)

    # add data for the line chart
    for idx, t in enumerate(towns):
        data = Weather.objects.order_by('date').filter(town=t)
        letter_max_t = chr(ord('B') + idx)
        letter_min_t = chr(ord('B') + idx + len(towns))
        worksheet_d.write_column(
            "{0}1".format(letter_max_t),
            data.values_list('max_temperature', flat=True))
        worksheet_d.write_column(
            "{0}1".format(letter_min_t),
            data.values_list('min_temperature', flat=True))

        # add data to line chart series
        line_chart.add_series({
            'categories': '=Chart Data!$A1:$A${0}'.format(len(dates)),
            'values': '=Chart Data!${0}${1}:${0}${2}'
            .format(letter_max_t, 1, len(data)),
            'marker': {'type': 'square'},
            'name': u"{0} {1}".format(ugettext("Max T."), t.name)
        })
        line_chart.add_series({
            'categories': '=Chart Data!$A1:$A${0}'.format(len(dates)),
            'values': '=Chart Data!${0}${1}:${0}${2}'
            .format(letter_min_t, 1, len(data)),
            'marker': {'type': 'circle'},
            'name': u"{0} {1}".format(ugettext("Min T."), t.name)
        })
    # adding other options
    line_chart.set_title({'name': ugettext("Maximum and Minimum Temperatures")})
    line_chart.set_x_axis({
        'text_axis': True,
        'date_axis': False
    })
    line_chart.set_y_axis({
        'num_format': u'## ℃'
    })
    # Insert Chart to "Charts" Sheet
    worksheet_c.insert_chart('B2', line_chart, {'x_scale': 2, 'y_scale': 1})

    # Creating the column chart
    bar_chart = workbook.add_chart({'type': 'column'})

    # creating data for column chart
    cell_index = len(towns) * 2 + 2
    for idx, t in enumerate(towns):
        max_wind = Weather.objects.filter(town=t).aggregate(Max('wind_speed'))
        min_wind = Weather.objects.filter(town=t).aggregate(Min('wind_speed'))
        worksheet_d.write_string(idx, cell_index, t.name)
        worksheet_d.write_number(
            idx, cell_index + 1, max_wind['wind_speed__max'])
        worksheet_d.write_number(
            idx, cell_index + 2, min_wind['wind_speed__min'])

    # add series
    bar_chart.add_series({
        'name': 'Max Speed',
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 1), 1, len(towns)),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, len(towns)),
        'data_labels': {'value': True, 'num_format': u'#0 "km/h"'}
    })
    bar_chart.add_series({
        'name': 'Min Speed',
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 2), 1, len(towns)),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, len(towns)),
        'data_labels': {'value': True, 'num_format': u'#0 "km/h"'}
    })
    # adding other options
    bar_chart.set_title({'name': ugettext("Maximum and minimum wind speeds")})

    worksheet_c.insert_chart('B20', bar_chart, {'x_scale': 1, 'y_scale': 1})

    # Creating the pie chart
    pie_chart = workbook.add_chart({'type': 'pie'})

    # creating data for pie chart
    pie_values = []
    pie_values.append(Weather.objects.filter(max_temperature__gt=20).count())
    pie_values.append(Weather.objects.filter(max_temperature__lte=20,
                                             max_temperature__gte=10).count())
    pie_values.append(Weather.objects.filter(max_temperature__lt=10).count())
    pie_categories = ["T >18", "10 < T < 18", "T < 10"]

    # adding the data to "Chart Data" Sheet
    cell_index = cell_index + 4
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index)),
                             pie_values)
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
                             pie_categories)

    # adding the data to the chart
    pie_chart.add_series({
        'name': ugettext('Temperature statistics'),
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, 3),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 1), 1, 3),
        'data_labels': {'percentage': True}
    })

    # insert the chart on "Charts" Sheet
    worksheet_c.insert_chart('J20', pie_chart)

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')

    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows = rows + 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1
    return rows
