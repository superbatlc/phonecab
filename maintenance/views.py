from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings


@login_required
def manitenance_home(request):
    # import time
    # d = request.GET.dict()
    # user = request.user
    # variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    # variables['audits'] = audit_items(request)
    # variables['d'] = d

    # data_inizio_cal = time.strftime("%d-%m-%Y")
    # if 'start_date' in d.keys():
    #     data_inizio_cal = d['start_date']
    # data_fine_cal = time.strftime("%d-%m-%Y")
    # if 'end_date' in d.keys():
    #     data_fine_cal = d['end_date']

    # variables['data_inizio_cal'] = data_inizio_cal
    # variables['data_fine_cal'] = data_fine_cal

    return render_to_response(
        'maintenance/home.html', RequestContext(request, {}))
