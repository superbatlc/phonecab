import json
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from acls.models import Acl
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
                # dobbiamo verificare se utente ha privilegi cdr
                privs = Acl.get_permissions_for_user(user.id, user.is_staff)
                if privs['priv_cdr'] > 0:
                    return redirect('/phonecab/', RequestContext(request, {}))
                return redirect('/phoneusers/', RequestContext(request, {}))
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


def phonecab_realtime(request):
    """Show current calls"""
    import time
    import datetime

    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    variables['actual_nightmode'] = Helper.get_nightmode()

    return render_to_response('realtime.html', RequestContext(request, variables))


def phonecab_get_nightmode(request):
    """Recupera la modalita giorno notte"""
    return HttpResponse(status=200,
                        content=("{ \"nightmode\" : %d }" % Helper.get_nightmode()), 
                        content_type="application/json")

def phonecab_set_nightmode(request, mode):
    """Modifica manualmente la modalita giorno notte"""
    import os

    cmd = "sudo /etc/asterisk/notte.sh"

    if mode == '0':
        cmd = "sudo /etc/asterisk/giorno.sh"
    try:
        ret = os.system(cmd)
        return HttpResponse(status=200,
                            content=json.dumps({'ret': ret}), 
                            content_type="application/json")
    except:
        redirect("/?err=1&err_msg=Impossibile accedere allo stato delle linee")
