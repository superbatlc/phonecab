import json
from urllib import urlencode
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings

#from cdrs.models import Detail
#from phoneusers.models import PhoneUser, Whitelist
from audits.models import Audit
from acls.models import Acl
#from prefs.models import Pref
from helper.Helper import Helper


@login_required
def audit_home(request):
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['audits'] = audit_items(request)
    variables['d'] = d

    data_inizio_cal = time.strftime("%d-%m-%Y")
    if 'start_date' in d.keys():
        data_inizio_cal = d['start_date']
    data_fine_cal = time.strftime("%d-%m-%Y")
    if 'end_date' in d.keys():
        data_fine_cal = d['end_date']

    variables['data_inizio_cal'] = data_inizio_cal
    variables['data_fine_cal'] = data_fine_cal

    return render_to_response(
        'audits/home.html', RequestContext(request, variables))


def audit_items(request):
    """CDR Items"""
    variables = {}

    items_per_page = 10 #settings.ITEMS_PER_PAGE

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    keyword = request.GET.get("keyword", "")

    page = int(request.GET.get("page", "1"))

    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

    q_obj = Q(user__username__icontains=keyword) | Q(user__last_name__icontains=keyword)

    if start_date != '':
        start_date = Helper.convert_datestring_format(
            start_date, "%d-%m-%Y", "%Y-%m-%d")
        if start_time:
            start_time = "%s:00" % start_time
        else:
            start_time = "00:00:00"
        start_date = "%s %s" % (start_date, start_time)
        q_obj.add(Q(when__gte=start_date), Q.AND)

    if end_date != '':
        end_date = Helper.convert_datestring_format(
            end_date, "%d-%m-%Y", "%Y-%m-%d")
        if end_time:
            end_time = "%s:59" % end_time
        else:
            end_time = "23:59:59"
        end_date = "%s %s" % (end_date, end_time)
        q_obj.add(Q(when__lte=end_date), Q.AND)

    items_list = Audit.objects.filter(q_obj).order_by('-when')
    total_items = items_list.count()

    items, items_range, items_next_page = Helper.make_pagination(
        items_list, page, items_per_page)

    prev_page = page - 1
    prev_page_disabled = ''
    if prev_page < 1:
        prev_page = 1
        prev_page_disabled = 'disabled'

    next_page = 1
    next_page_disabled = ''
    if items:
        next_page = page + 1
        if next_page > items.paginator.num_pages:
            next_page = items.paginator.num_pages
            next_page_disabled = 'disabled'

    # print "range: %s - next: %s" % (items_range, next_page)

    start_item = 1
    if page > 0:
        start_item = (page - 1) * items_per_page + 1
    end_item = start_item + items_per_page - 1
    if end_item > total_items:
        end_item = total_items

    variables['items'] = items
    variables['total_items'] = total_items
    variables['prev_page'] = prev_page
    variables['next_page'] = next_page
    variables['prev_page_disabled'] = prev_page_disabled
    variables['next_page_disabled'] = next_page_disabled
    variables['current_page'] = page
    variables['start_item'] = start_item
    variables['end_item'] = end_item
    variables['query_string'] = urlencode(d)
    variables['d'] = d

    if request.is_ajax():
        return render_to_response(
            'audits/table.html', RequestContext(request, variables))

    return render_to_string(
        'audits/table.html', RequestContext(request, variables))