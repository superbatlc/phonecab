from django.http import HttpResponse
#from django.http import Http404
from django.shortcuts import render_to_response
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

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

    min_duration = Pref.objects.get(key='min_duration').value
    alert_before_end = Pref.objects.get(key='alert_before_end').value
    privacy_mode = Pref.objects.get(key='privacy_mode').value

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
        'min_duration': min_duration,
        'alert_before_end': alert_before_end,
        'privacy_mode': privacy_mode,
    }
    return render_to_response(
        'prefs_modal.html', RequestContext(request, variables))


@login_required
def prefs_save(request):
    try:
        ret = "1"
        # DISTRETTUALI -----------------------------------------------------------
        dist_connection_charge = get_fee(
            request.POST.get(
                "data[dist_connection_charge]",
                "0.00"))
        dist_fee_per_second = get_fee(
            request.POST.get(
                "data[dist_fee_per_second]",
                "0.00")) / 60

        f = Fare.objects.get(direction='distrettuale')
        f.connection_charge = dist_connection_charge
        f.fee_per_second = dist_fee_per_second
        f.save(request.user)
        # NAZIONALI -----------------------------------------------------------
        naz_connection_charge = get_fee(
            request.POST.get(
                "data[naz_connection_charge]",
                "0.00"))
        naz_fee_per_second = get_fee(
            request.POST.get(
                "data[naz_fee_per_second]",
                "0.00")) / 60

        f = Fare.objects.get(direction='nazionale')
        f.connection_charge = naz_connection_charge
        f.fee_per_second = naz_fee_per_second
        f.save(request.user)

        # INTERNAZIONALI 1 ----------------------------------------------------
        int1_connection_charge = get_fee(
            request.POST.get(
                "data[int1_connection_charge]",
                "0.00"))
        int1_fee_per_second = get_fee(
            request.POST.get(
                "data[int1_fee_per_second]",
                "0.00")) / 60
        int1_prefix_list = request.POST.get("data[int1_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 1')
        f.connection_charge = int1_connection_charge
        f.fee_per_second = int1_fee_per_second
        f.prefix_list = int1_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 2 ----------------------------------------------------
        int2_connection_charge = get_fee(
            request.POST.get(
                "data[int2_connection_charge]",
                "0.00"))
        int2_fee_per_second = get_fee(
            request.POST.get(
                "data[int2_fee_per_second]",
                "0.00")) / 60
        int2_prefix_list = request.POST.get("data[int2_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 2')
        f.connection_charge = int2_connection_charge
        f.fee_per_second = int2_fee_per_second
        f.prefix_list = int2_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 3 ----------------------------------------------------
        int3_connection_charge = get_fee(
            request.POST.get(
                "data[int3_connection_charge]",
                "0.00"))
        int3_fee_per_second = get_fee(
            request.POST.get(
                "data[int3_fee_per_second]",
                "0.00")) / 60
        int3_prefix_list = request.POST.get("data[int3_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 3')
        f.connection_charge = int3_connection_charge
        f.fee_per_second = int3_fee_per_second
        f.prefix_list = int3_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 4 ----------------------------------------------------
        int4_connection_charge = get_fee(
            request.POST.get(
                "data[int4_connection_charge]",
                "0.00"))
        int4_fee_per_second = get_fee(
            request.POST.get(
                "data[int4_fee_per_second]",
                "0.00")) / 60
        int4_prefix_list = request.POST.get("data[int4_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 4')
        f.connection_charge = int4_connection_charge
        f.fee_per_second = int4_fee_per_second
        f.prefix_list = int4_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 5 ----------------------------------------------------
        int5_connection_charge = get_fee(
            request.POST.get(
                "data[int5_connection_charge]",
                "0.00"))
        int5_fee_per_second = get_fee(
            request.POST.get(
                "data[int5_fee_per_second]",
                "0.00")) / 60
        int5_prefix_list = request.POST.get("data[int5_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 5')
        f.connection_charge = int5_connection_charge
        f.fee_per_second = int5_fee_per_second
        f.prefix_list = int5_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 6 ----------------------------------------------------
        int6_connection_charge = get_fee(
            request.POST.get(
                "data[int6_connection_charge]",
                "0.00"))
        int6_fee_per_second = get_fee(
            request.POST.get(
                "data[int6_fee_per_second]",
                "0.00")) / 60
        int6_prefix_list = request.POST.get("data[int6_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 6')
        f.connection_charge = int6_connection_charge
        f.fee_per_second = int6_fee_per_second
        f.prefix_list = int6_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 7 ----------------------------------------------------
        int7_connection_charge = get_fee(
            request.POST.get(
                "data[int7_connection_charge]",
                "0.00"))
        int7_fee_per_second = get_fee(
            request.POST.get(
                "data[int7_fee_per_second]",
                "0.00")) / 60
        int7_prefix_list = request.POST.get("data[int7_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 7')
        f.connection_charge = int7_connection_charge
        f.fee_per_second = int7_fee_per_second
        f.prefix_list = int7_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 8 ----------------------------------------------------
        int8_connection_charge = get_fee(
            request.POST.get(
                "data[int8_connection_charge]",
                "0.00"))
        int8_fee_per_second = get_fee(
            request.POST.get(
                "data[int8_fee_per_second]",
                "0.00")) / 60
        int8_prefix_list = request.POST.get("data[int8_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 8')
        f.connection_charge = int8_connection_charge
        f.fee_per_second = int8_fee_per_second
        f.prefix_list = int8_prefix_list
        f.save(request.user)

        # INTERNAZIONALI 9 ----------------------------------------------------
        int9_connection_charge = get_fee(
            request.POST.get(
                "data[int9_connection_charge]",
                "0.00"))
        int9_fee_per_second = get_fee(
            request.POST.get(
                "data[int9_fee_per_second]",
                "0.00")) / 60
        int9_prefix_list = request.POST.get("data[int9_prefix_list]", "")

        f = Fare.objects.get(direction='internazionale 9')
        f.connection_charge = int9_connection_charge
        f.fee_per_second = int9_fee_per_second
        f.prefix_list = int9_prefix_list
        f.save(request.user)

        # MOBILE --------------------------------------------------------------
        mob_connection_charge = get_fee(
            request.POST.get(
                "data[mob_connection_charge]",
                "0.00"))
        mob_fee_per_second = get_fee(
            request.POST.get(
                "data[mob_fee_per_second]",
                "0.00")) / 60

        f = Fare.objects.get(direction='mobile')
        f.connection_charge = mob_connection_charge
        f.fee_per_second = mob_fee_per_second
        f.save(request.user)

        # ALTRE PREFERENZE CHIAMATA -------------------------------------------
        min_duration = request.POST.get("data[min_duration]", "0")
        alert_before_end = request.POST.get("data[alert_before_end]", "0")
        privacy_mode = request.POST.get("data[privacy_mode]", "0")

        p = Pref.objects.get(key='min_duration')
        p.value = min_duration
        p.save(request.user)

        p = Pref.objects.get(key='alert_before_end')
        p.value = alert_before_end
        p.save(request.user)

        p = Pref.objects.get(key='privacy_mode')
        p.value = privacy_mode
        p.save(request.user)

        return HttpResponse(ret, mimetype='text/plain')

    except Exception as e:
        print '%s (%s)' % (e.message, type(e))


def get_fee(value):
    return float(value.replace(",", "."))
