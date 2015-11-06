from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from acls.models import Acl
from cdrs.models import RealTimeCall
from phoneusers.models import PhoneUser
from archives.models import ArchivedPhoneUser
from prefs.models import Fare
from helper.Helper import Helper


def phonecab_login(request):
    if request.user.is_authenticated():
        return redirect('/phonecab/', RequestContext(request, {}))

    print "Entering phonecab_login..."
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/phonecab/', RequestContext(request, {}))
            else:
                return render_to_response(
                    'registration/login.html',
                    RequestContext(
                        request,
                        {
                            'error': True,
                            'err_msg': 'Utente non attivo'}))
        else:
            return render_to_response(
                'registration/login.html',
                RequestContext(
                    request,
                    {
                        'error': True,
                        'err_msg': 'Le credenziali inserite non sono corrette.'}))
    else:
        return render_to_response(
            'registration/login.html', RequestContext(request, {}))


def phonecab_logout(request):
    logout(request)
    return redirect('/')


@login_required
def phonecab_home(request):
    """Show main page"""
    archive = request.GET.get("archive", "")

    custom_msg = ""
    if archive == 'ok':
        custom_msg = """<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>
                    <h4>Ok!</h4>Anagrafica archiviata con successo.<br>"""
    if archive == 'error':
        custom_msg = """<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>
                    <h4>Attenzione</h4>Archiviazione Anagrafica non riuscita.<br>
                    Si prega di contattare il responsabile del software PhoneCab.</div>"""

    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['user'] = user
    variables['realtime_table'] = phonecab_realtime(request)
    variables['custom_msg'] = custom_msg

    return render_to_response('base.html', RequestContext(request, variables))


@login_required
def phonecab_search(request):
    from django.db.models import Q
    # recuperiamo i privilegi utente
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['user'] = user
    query = request.POST.get("search_query", "")
    if query != "":
        variables['search_query'] = query
        if query == "*":
            anagrafiche = PhoneUser.objects.all().order_by('last_name')
        else:
            q_obj = Q(last_name__icontains=query)
            q_obj.add(Q(serial_no__icontains=query), Q.OR)
            q_obj.add(Q(pincode__contains=query), Q.OR)
            anagrafiche = PhoneUser.objects.filter(q_obj).order_by('last_name')

        variables['anagrafiche'] = anagrafiche

        if user.is_staff:
            # Archives
            if query == "*":
                archives = ArchivedPhoneUser.objects.all().order_by('last_name')
            else:
                q_obj = Q(last_name__icontains=query)
                q_obj.add(Q(serial_no__icontains=query), Q.OR)
                q_obj.add(Q(pincode__contains=query), Q.OR)
                archives = ArchivedPhoneUser.objects.filter(q_obj).order_by('last_name')

            variables['archives'] = archives
            # Users
            q_obj = Q(last_name__icontains=query)
            q_obj.add(Q(username__icontains=query), Q.OR)
            utenti = User.objects.filter(q_obj)
            variables['utenti'] = utenti

    return render_to_response(
        'search_result.html', RequestContext(request, variables))


def phonecab_realtime(request):
    """Show current calls"""
    import time
    import datetime

    rt_calls = RealTimeCall.objects.all().order_by('src')

    calldate = datetime.datetime.today().strftime("%Y%m%d")
    calltime = datetime.datetime.today().strftime("%H%M%S")

    daynight_text, daynight_class = Helper.get_daynight()
    daynight_user_text = daynight_text == 'GIORNO' and 'Abilita le linee' or 'Disabilita le linee'

    for rt in rt_calls:
        rt.phoneuser = PhoneUser.get_from_pincode(rt.pincode)
        duration = int(time.time()) - rt.calldate
        rt.elapsed_time = duration
        cost = Fare.get_call_cost(rt.dst, duration)
        rt.balance = round(rt.balance - cost, 2)
        rt.file = "%s_%s_%s_%s" % (rt.pincode,
                                   calldate,
                                   calltime,
                                   rt.dst)

    variables = {
        'rt_calls': rt_calls,
        'daynight_text': daynight_text,
        'daynight_user_text': daynight_user_text,
        'daynight_class': daynight_class,
    }

    if request.is_ajax():
        return render_to_response(
            'realtime_table.html', RequestContext(request, variables))
    return render_to_string(
        'realtime_table.html', RequestContext(request, variables))


def phonecab_daynight(request, mode):
    """Modifica manualmente la modalita giorno notte"""
    import os

    cmd = "/etc/asterisk/notte.sh"

    if mode == 'GIORNO':
        cmd = "/etc/asterisk/giorno.sh"

    os.system(cmd)

    return HttpResponse("ok", mimetype="text/plain")

