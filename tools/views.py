import os
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from acls.models import Acl
from prefs.models import Extension


@login_required
def tools_home(request):
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['diskusage'] = 0
    variables['extdiskusage'] = 0
    if request.GET.get("err") != '1':
        try:
            variables['diskusage'] = _tool_get_disk_usage(settings.FILESYSTEM)
            variables['extdiskusage'] = _tool_get_disk_usage(settings.EXT_FILESYSTEM)
            variables['peers_status'] = _get_peers_status()
        except Exception as e:
            return redirect("/tools/?err=1&err_msg=%s" % format(e))
            #return redirect("/tools/?err=1&err_msg=Impossibile recuperare il valore di occupazione disco"
    return render_to_response(
        'tools/home.html', RequestContext(request, variables))


def _tool_get_disk_usage(disk):
    import os
    percent = os.popen("df -hl | grep '%s' | awk 'BEGIN{}{percent=$5} END{print percent}'" % settings.FILESYSTEM).read()
    if percent:
        return float(percent.replace("%", ""))
    return 0


def _get_peers_status():

    extensions = Extension.objects.all().order_by('extension')
    stati = []

    for extension in extensions:
        stato = 'OFF'
        cmd = '/usr/sbin/asterisk -rx "sip show peer %s" | grep "Status"'
        if settings.USE_SUDO:
            cmd = "sudo %s" % cmd
        status = os.popen(cmd % extension.extension).read()

        if "OK" in status:
            stato = 'ON'
        stati.append({'extension': extension, 'status': stato})

    return stati
