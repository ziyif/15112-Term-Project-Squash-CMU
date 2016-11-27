# from django.template.defaulttages import register
from django import template

register = template.Library()

@register.filter
def time_in_week(s):
    times = {'MM':'Monday Morning',
        'MA': 'Monday Afternoon',
        'ME': 'Monday Evening',

        'TM': 'Tuesday Morning',
        'TA': 'Tuesday Afternoon',
        'TE': 'Tuesday Evening',
        'WM': 'Wednesday Morning',
        'WA': 'Wednesday Afternoon',
        'WE': 'Wednesday Evening',
        'TrM': 'Thursday Morning',
        'TrA': 'Thursday Afternoon',
        'TrE': 'Thursday Evening',
        'FM': 'Friday Morning',
        'FA': 'Friday Afternoon',
        'FE': 'Friday Evening',
        'SM': 'Saturday Morning',
        'SA': 'Saturday Afternoon',
        'SE': 'Saturday Evening',
        'SuM': 'Sunday Morning',
        'SuA': 'Sunday Afternoon',
        'SuE': 'Sunday Evening'
        }

    return times[s]

@register.filter
def times_in_week(times):
    result = []
    for time in times:
        result.append(time_in_week(time))
    return result