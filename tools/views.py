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
    if request.GET.get("err") != '1':
        try:
            variables['diskusage'] = _tool_get_disk_usage()
            variables['peers_status'] = _get_peers_status()
        except Exception as e:
            return redirect("/tools/?err=1&err_msg=%s" % format(e))
            #return redirect("/tools/?err=1&err_msg=Impossibile recuperare il valore di occupazione disco")
    
    return render_to_response(
        'tools/home.html', RequestContext(request, variables))


def _tool_get_disk_usage():
    import os
    percent = os.popen("df -hl | grep '%s' | awk 'BEGIN{}{percent=$5} END{print percent}'" % settings.FILESYSTEM).read()
    return float(percent.replace("%", ""))

def _get_peers_status():

    extensions = Extension.objects.all().order_by('extension')
    stati = []
    print extensions
    
    for extension in extensions:
        stato = 'OFF'
        status = os.popen('sudo /usr/sbin/asterisk -rx "sip show peer %s" | grep "Status"' % extension.extension).read()
	print status
        if "OK" in status:
            stato = 'ON'
        stati.append({'extension': extension, 'status': stato})

    return stati
