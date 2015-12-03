from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from acls.models import Acl


@login_required
def tools_home(request):
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    try:
        variables['diskusage'] = _tool_get_disk_usage()
    except:
        pass
    
    return render_to_response(
        'tools/home.html', RequestContext(request, variables))


def _tool_get_disk_usage():
    import os
    percent = os.popen("df -hl | grep '%s' | awk 'BEGIN{}{percent=$5} END{print percent}'" % settings.FILESYSTEM).read()
    return percent.replace("%", "")
