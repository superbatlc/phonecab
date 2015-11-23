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
def __phonecab_home(request):
    """Show main page"""
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['user'] = user
    variables['realtime_table'] = phonecab_realtime(request)
    variables['custom_msg'] = custom_msg

    return render_to_response('base.html', RequestContext(request, variables))


def phonecab_realtime(request):
    """Show current calls"""
    import time
    import datetime

    daynight_actual_mode = Helper.get_daynight()
    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    variables['daynight_actual_mode'] = daynight_actual_mode

    return render_to_response('realtime.html', RequestContext(request, variables))


def phonecab_getdaynight(request):
    """Recupera la modalita giorno notte"""
    return HttpResponse(status=200,content=("{ \"daynight\" : %d }" % Helper.get_daynight()), content_type="application/json")

def phonecab_daynight(request, mode):
    """Modifica manualmente la modalita giorno notte"""
    import os

    cmd = "/etc/asterisk/notte.sh"

    if mode == 'GIORNO':
        cmd = "/etc/asterisk/giorno.sh"

    os.system(cmd)

    return HttpResponse("ok", mimetype="text/plain")
