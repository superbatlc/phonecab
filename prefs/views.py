from django.http import HttpResponse
#from django.http import Http404
from django.shortcuts import render_to_response, redirect
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from acls.models import Acl
from prefs.models import Fare, Pref


@login_required
def prefs_edit(request):
    # recuperiamo le preferenze
    dist = Fare.objects.get(direction='distrettuale')
    naz = Fare.objects.get(direction='nazionale')
    int1 = Fare.objects.get(direction='internazionale 1')
    int2 = Fare.objects.get(direction='internazionale 2')
    int3 = Fare.objects.get(direction='internazionale 3')
    int4 = Fare.objects.get(direction='internazionale 4')
    int5 = Fare.objects.get(direction='internazionale 5')
    int6 = Fare.objects.get(direction='internazionale 6')
    int7 = Fare.objects.get(direction='internazionale 7')
    int8 = Fare.objects.get(direction='internazionale 8')
    int9 = Fare.objects.get(direction='internazionale 9')
    mob = Fare.objects.get(direction='mobile')

    min_duration = Pref.get('min_duration')
    alert_before_end = Pref.get('alert_before_end')
    enable_first_in = Pref.get('enable_first_in')
    change_threshold = Pref.get('change_threshold')
    threshold = int(Pref.get('threshold')) / 60
    """
    variables = {
        'tooltip_text': 'Premi per mostrare/nascondere i prefissi di questa area geografica',
        'naz': naz,
        'dist': dist,
        'int1': int1,
        'int2': int2,
        'int3': int3,
        'int4': int4,
        'int5': int5,
        'int6': int6,
        'int7': int7,
        'int8': int8,
        'int9': int9,
        'mob': mob,
    """
    variables = {
        'min_duration': min_duration,
        'alert_before_end': alert_before_end,
        'enable_first_in': enable_first_in,
        'change_threshold': change_threshold,
        'threshold': threshold,
        'fares': Fare.objects.filter(visible=True)
    }

    variables.update(Acl.get_permissions_for_user(request.user.id, request.user.is_staff))

    return render_to_response(
        'prefs.html', RequestContext(request, variables))


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
        min_duration = request.POST.get("min_duration", "0")
        alert_before_end = request.POST.get("alert_before_end", "0")
        enable_first_in = request.POST.get("enable_first_in", "0")

        p = Pref.objects.get(key='min_duration')
        p.value = min_duration
        p.save(request.user)

        p = Pref.objects.get(key='alert_before_end')
        p.value = alert_before_end
        p.save(request.user)

        p = Pref.objects.get(key='enable_first_in')
        p.value = enable_first_in
        p.save(request.user)

        # return HttpResponse(ret, mimetype='text/plain')
        return prefs_edit(request)

    except Exception as e:
        print '%s (%s)' % (e.message, type(e))


def get_fee(value):
    return float(value.replace(",", "."))
