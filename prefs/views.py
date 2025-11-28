from django.http import HttpResponse
#from django.http import Http404
from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from acls.models import Acl
from prefs.models import Fare, Pref


@login_required
def prefs_edit(request):
    # recuperiamo le preferenze e le tariffe
    # min_duration = Pref.get('min_duration')
    min_duration_with_credit = Pref.get('min_duration_with_credit')
    alert_before_end = Pref.get('alert_before_end')
    enable_first_in = Pref.get('enable_first_in')
    ordinary_lawyer = Pref.get('ordinary_lawyer')
    change_threshold = Pref.get('change_threshold')
    threshold = int(Pref.get('threshold') or 0) / 60
    change_additional_calls = Pref.get('change_additional_calls')
    default_additional_calls = Pref.get('default_additional_calls')
    max_calls_per_day = Pref.get('max_calls_per_day')
    lawyer_call_limit = Pref.get('lawyer_call_limit')
    limit_additional_calls_per_day = Pref.get('limit_additional_calls_per_day')
    covid_general = Pref.get('covid_general')
    limit_duration = Pref.get('limit_duration')
    header = Pref.get('header')
    fares = Fare.objects.filter(position__gt=0).order_by('position')

    variables = {
        # 'min_duration': min_duration,
        'min_duration_with_credit': min_duration_with_credit,
        'alert_before_end': alert_before_end,
        'enable_first_in': enable_first_in,
        'ordinary_lawyer': ordinary_lawyer,
        'change_threshold': change_threshold,
        'change_additional_calls': change_additional_calls,
        'default_additional_calls': default_additional_calls,
        'max_calls_per_day': max_calls_per_day,
        'lawyer_call_limit': lawyer_call_limit,
        'limit_additional_calls_per_day': limit_additional_calls_per_day,
        'covid_general': covid_general,
        'limit_duration': limit_duration,
        'threshold': threshold,
        'fares': fares,
        'header': header,
    }

    variables.update(Acl.get_permissions_for_user(request.user.id, request.user.is_staff))
    return render(request, 'prefs.html', variables)


@login_required
def prefs_save(request):
    import time

    try:

        # TARIFFE E PREFISSI --------------------------------------------------

        fare_id_list = request.POST.getlist('fare_id[]')
        fare_connection_charge_list = request.POST.getlist('fare_connection_charge[]')
        fare_fee_per_second_list = request.POST.getlist('fare_fee_per_second[]')
        fare_prefix_list_list = request.POST.getlist('fare_prefix_list[]')

        for index, id in enumerate(fare_id_list):
            f = Fare.objects.get(pk=id)
            f.connection_charge = get_fee(fare_connection_charge_list[index])
            f.fee_per_second = get_fee(fare_fee_per_second_list[index]) / 60
            f.prefix_list = fare_prefix_list_list[index]
            f.save(request.user)

        # ALTRE PREFERENZE CHIAMATA -------------------------------------------
        # min_duration = request.POST.get("min_duration", "0")
        min_duration_with_credit = request.POST.get("min_duration_with_credit", "0")
        alert_before_end = request.POST.get("alert_before_end", "0")
        enable_first_in = request.POST.get("enable_first_in", "0")
        ordinary_lawyer = request.POST.get("ordinary_lawyer", "0")
        change_threshold = request.POST.get("change_threshold", "0")
        threshold = to_int(request.POST.get("threshold", 10), 10) * 60
        change_additional_calls = request.POST.get("change_additional_calls", "0")
        default_additional_calls = to_int(request.POST.get("default_additional_calls", "0"))
        max_calls_per_day = to_int(request.POST.get("max_calls_per_day", "0"))
        lawyer_call_limit = to_int(request.POST.get("lawyer_call_limit", "0"))
        limit_additional_calls_per_day = to_int(request.POST.get("limit_additional_calls_per_day", "0"))
        header = request.POST.get("header", "0")
        limit_duration = request.POST.get("limit_duration", "0")
        covid_general = request.POST.get("covid_general", "0")

        # p = Pref.objects.get(key='min_duration')
        # p.value = min_duration
        # p.save(request.user)

        set_pref('min_duration_with_credit', min_duration_with_credit, request.user)
        set_pref('alert_before_end', alert_before_end, request.user)
        set_pref('enable_first_in', enable_first_in, request.user)
        set_pref('ordinary_lawyer', ordinary_lawyer, request.user)
        set_pref('change_threshold', change_threshold, request.user)
        set_pref('threshold', threshold, request.user)
        set_pref('change_additional_calls', change_additional_calls, request.user)
        set_pref('default_additional_calls', default_additional_calls, request.user)

        # p = Pref.objects.get(key='max_calls_per_day')
        # p.value = max_calls_per_day
        # p.save(request.user)

        set_pref('lawyer_call_limit', lawyer_call_limit, request.user)
        set_pref('limit_additional_calls_per_day', limit_additional_calls_per_day, request.user)
        set_pref('limit_duration', limit_duration, request.user)
        set_pref('covid_general', covid_general, request.user)
        set_pref('header', header, request.user)

    except Exception as e:
        print('%s (%s)' % (e, type(e))) # TODO gestire errore

    return redirect('/prefs/edit/')


def get_fee(value):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def set_pref(key, value, user):
    """
    Aggiorna o crea la preferenza evitando errori in caso di duplicati o chiavi mancanti.
    """
    pref = Pref.objects.filter(key=key).first()
    if pref is None:
        pref = Pref(key=key)
    pref.value = value
    pref.save(user)
