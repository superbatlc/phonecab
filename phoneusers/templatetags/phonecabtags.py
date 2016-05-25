from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def privacymode(value, digits):
    if len(value) == 0:
        return ''
    if len(value) > digits:
        # return value.replace(' ','----')
        return value[:-digits] + '*' * digits
    return value


@register.filter
@stringfilter
def calltype(value):
    """ Assigns label based on calltype value"""
    if value == '0':
        return '<span class="label label-success">ORD</span>'
    elif value == '1':
        return '<span class="label label-warning">SUP</span>'
    elif value == '2':
        return '<span class="label label-danger">STR</span>'
    elif value == '3':
        return '<span class="label label-default">SPE</span>'


@register.filter
@stringfilter
def format_time(value):
    value = int(value)

    minutes = value / 60
    seconds = value % 60

    ret = ''

    if minutes:
        ret = "%sm " % minutes
    if seconds:
        ret += "%ss" % seconds

    return ret


@register.filter
@stringfilter
def print_timestamp(timestamp):
    import time
    return time.strftime("%H:%M:%S", time.gmtime(float(timestamp)))


@register.filter
@stringfilter
def per_minute(value):
    """Converts value per second in value per minute"""
    return float(value) * 60
