from urllib import urlencode
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from acls.models import Acl
from archives.models import *
from helper.Helper import Helper


@login_required
def archive_phoneuser_home(request):
    """Phoneusers page"""
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['phoneusers'] = archive_phoneuser_items(request)
    variables['d'] = d

    return render_to_response(
        'archives/phoneusers/home.html', RequestContext(request, variables))

def archive_phoneuser_items(request):
    """Archived Phoneuser Items List"""
    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)

    items_per_page = settings.ITEMS_PER_PAGE

    keyword = request.GET.get("keyword", "")
    page = int(request.GET.get("page", "1"))

    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

    q_obj = Q(last_name__icontains=keyword)
    q_obj.add(Q(pincode__icontains=keyword), Q.OR)
    q_obj.add(Q(serial_no__icontains=keyword), Q.OR)

    items_list = ArchivedPhoneUser.objects.filter(q_obj).order_by('last_name')
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
            'archives/phoneusers/table.html', RequestContext(request, variables))

    return render_to_string(
        'archives/phoneusers/table.html', RequestContext(request, variables))

@login_required
def archive_phoneuser_view(request, archived_phoneuser_id):
    """Visualizza la pagina di anagrafica"""
    archived_phoneuser_id = int(archived_phoneuser_id)
    if not archived_phoneuser_id:
        raise Http404

    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    phoneuser = archive_phoneuser_data(request, archived_phoneuser_id)
    whitelists = archive_whitelist_items(request, archived_phoneuser_id)
    credits = archive_credit_items(request, archived_phoneuser_id)
   
    variables['phoneuser'] = phoneuser
    variables['whitelists'] = whitelists
    variables['credits'] = credits
    return render_to_response('archives/phoneusers/page.html',
        RequestContext(request,variables))

@login_required
def archive_phoneuser_data(request, archived_phoneuser_id):
    """Recupera e visualizza le informazioni sul phoneuser archiviato"""
    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    if int(archived_phoneuser_id):
        try:
            phoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
        except:
            raise Http404
    variables['phoneuser'] = phoneuser
    if request.is_ajax():
        return render_to_response(
            'archives/phoneusers/phoneuser.html', RequestContext(request, variables))
    return render_to_string(
        'archives/phoneusers/phoneuser.html', RequestContext(request, variables))

@login_required
def archive_whitelist_items(request, archived_phoneuser_id):
    archived_phoneuser_id = int(archived_phoneuser_id)
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    whitelists = ArchivedWhitelist.objects.filter(
        archived_phoneuser_id=archived_phoneuser_id).order_by('label')

    for wl in whitelists:
        if wl.frequency == 0 or wl.frequency == 3:
            wl.times = '-'

    variables['whitelists'] = whitelists

    if request.is_ajax():
        return render_to_response(
            'archives/phoneusers/whitelists/table.html', RequestContext(request, variables))

    return render_to_string(
        'archives/phoneusers/whitelists/table.html', RequestContext(request, variables))

@login_required
def archive_credit_items(request, archived_phoneuser_id):
    archived_phoneuser_id = int(archived_phoneuser_id)
    archivedphoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    credits = ArchivedCredit.objects.filter(
        archived_phoneuser_id=archived_phoneuser_id).order_by('-recharge_date')

    variables['items'] = credits
    variables['balance'] = archivedphoneuser.balance

    if request.is_ajax():
        return render_to_response(
            'archives/phoneusers/credits/table.html', RequestContext(request, variables))

    return render_to_string(
        'archives/phoneusers/credits/table.html', RequestContext(request, variables))

@login_required
def archive_cdrs_home(request):
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['cdr'] = archive_cdrs_items(request)
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
        'archives/cdrs/home.html', RequestContext(request, variables))

@login_required
def archive_cdrs_items(request):
    variables = {}

    items_per_page = settings.ITEMS_PER_PAGE

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    accountcode = request.GET.get("accountcode", "")
    archived_phoneuser_id = request.GET.get("archived_phoneuser_id", "")
    dst = request.GET.get("dst", "")
    custom_calltype = request.GET.get("custom_calltype", None)
    page = int(request.GET.get("page", "1"))

    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

    q_obj = Q(accountcode__icontains=accountcode)
    q_obj.add(Q(custom_dst__icontains=dst), Q.AND)

    if archived_phoneuser_id:
        q_obj.add(Q(archived_phoneuser_id=archived_phoneuser_id), Q.AND)

    if start_date != '':
        start_date = Helper.convert_datestring_format(
            start_date, "%d-%m-%Y", "%Y-%m-%d")
        if start_time:
            start_time = "%s:00" % start_time
        else:
            start_time = "00:00:00"
        start_date = "%s %s" % (start_date, start_time)
        q_obj.add(Q(calldate__gte=start_date), Q.AND)

    if end_date != '':
        end_date = Helper.convert_datestring_format(
            end_date, "%d-%m-%Y", "%Y-%m-%d")
        if end_time:
            end_time = "%s:59" % end_time
        else:
            end_time = "23:59:59"
        end_date = "%s %s" % (end_date, end_time)
        q_obj.add(Q(calldate__lte=end_date), Q.AND)
        
    if custom_calltype:
        q_obj.add(Q(custom_calltype=custom_calltype), Q.AND)

    items_list = ArchivedDetail.objects.filter(q_obj).order_by('-calldate')
    total_items = items_list.count()
    total_costs = 0.0

    # calcoliamo numero e costo complessivo
    for item in items_list:
        if float(item.price) > 0:
            total_costs += float(item.price)

    items, items_range, items_next_page = Helper.make_pagination(
        items_list, page, items_per_page)

    for item in items:
        if item.price < 0:
            item.price = "0.00"
        try:
            item.whitelist = ArchivedWhitelist.objects.filter(
                archived_phoneuser=item.archived_phoneuser_id, phonenumber=item.custom_dst)[0]
        except Exception as e:
            pass # TODO gestire errore

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
    variables['total_costs'] = total_costs
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
            'archives/cdrs/table.html', RequestContext(request, variables))

    return render_to_string(
        'archives/cdrs/table.html', RequestContext(request, variables))

@login_required
def archive_records_home(request):
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['records'] = archive_records_items(request)
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
        'archives/records/home.html', RequestContext(request, variables))

@login_required
def archive_records_items(request):
    """Record Items"""
    from urllib import urlencode
    variables = {}

    items_per_page = settings.ITEMS_PER_PAGE

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", "00:00")
    end_time = request.GET.get("end_time", "23:59")
    archived_phoneuser_id = request.GET.get("archived_phoneuser_id", "")
    pincode = request.GET.get("pincode", "")
    page = int(request.GET.get("page", "1"))
    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

    q_obj = Q(pincode__icontains=pincode)

    if archived_phoneuser_id:
        q_obj.add(Q(archived_phoneuser_id=archived_phoneuser_id), Q.AND)

    if start_date != '':
        start_date = Helper.convert_datestring_format(
            start_date, "%d-%m-%Y", "%Y-%m-%d")
        start_date = "%s %s:00" % (start_date, start_time)
        q_obj.add(Q(calldate__gte=start_date), Q.AND)

    if end_date != '':
        end_date = Helper.convert_datestring_format(
            end_date, "%d-%m-%Y", "%Y-%m-%d")
        end_date = "%s %s:59" % (end_date, end_time)
        q_obj.add(Q(calldate__lte=end_date), Q.AND)

    items_list = ArchivedRecord.objects.filter(q_obj).order_by('-calldate')
    total_items = items_list.count()

    items, items_range, items_next_page = Helper.make_pagination(
        items_list, page, items_per_page)

    for item in items:
        try:
            details = ArchivedDetail.objects.filter(uniqueid=item.uniqueid)
            if not details:
                item.detail = Detail
                item.detail.custom_dst = ''
            else:
                item.detail = details[0]
            item.whitelist = ArchivedWhitelist.objects.get(
                archived_phoneuser_id=item.archived_phoneuser_id, phonenumber=item.detail.custom_dst)
        except Exception as e:
            pass # TODO gestire
            print "Errore nel recupero delle informazioni sulla chiamata"

        if item.filename != '':
            item.filename = "/recordings/%s" % item.filename

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
    variables['d'] = d
    variables['query_string'] = urlencode(d)

    if request.is_ajax():
        return render_to_response(
            'archives/records/table.html', RequestContext(request, variables))

    return render_to_string(
        'archives/records/table.html', RequestContext(request, variables))


