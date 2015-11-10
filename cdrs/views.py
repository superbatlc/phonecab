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

from cdrs.models import Detail
from phoneusers.models import PhoneUser, Whitelist
from audits.models import Audit
from acls.models import Acl
from prefs.models import Pref
from helper.Helper import Helper


@login_required
def cdr_home(request):
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['cdr'] = cdr_items(request)
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
        'cdrs/home.html', RequestContext(request, variables))


def cdr_items(request):
    """CDR Items"""
    variables = {}

    items_per_page = settings.ITEMS_PER_PAGE

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    accountcode = request.GET.get("accountcode", "")
    dst = request.GET.get("dst", "")
    page = int(request.GET.get("page", "1"))

    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

    q_obj = Q(accountcode__icontains=accountcode)
    q_obj.add(Q(custom_dst__icontains=dst), Q.AND)
    q_obj.add(Q(dcontext='cabs-dial-number')|Q(dcontext='outgoing-operator-dial-number')|Q(dcontext='incoming-operator-dial-number'), Q.AND)

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

    items_list = Detail.objects.filter(q_obj).order_by('-calldate')
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
            # cerchiamo di recuperare informazioni sul phoneuser
        item.phoneuser = PhoneUser.get_from_pincode(item.accountcode)
        try:
            item.whitelist = Whitelist.objects.filter(
                phoneuser_id=item.phoneuser.id, phonenumber=item.custom_dst)[0]
        except Exception as e:
            pass

        #variables['callrange'] = call_range
        #variables['call_next_page'] = call_next_page
        #variables['query_string'] = urlencode(d)
        #variables['d'] = d

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
            'cdrs/table.html', RequestContext(request, variables))

    return render_to_string(
        'cdrs/table.html', RequestContext(request, variables))


@login_required
def cdr_valid(request):

    detail_id = int(request.POST.get("detail_id", "0"))
    valid = request.POST.get("valid", "False") == "True"

    values = {
              'data': {},
              'err': 0,
              'err_msg': '',
              }

    if detail_id:
        try:
            detail = Detail.objects.get(pk=detail_id)
            detail.custom_valid = not valid  # cambiamo il valore
            detail.save()

            values['data'] = not valid

        except:
            values['err'] = 1
            values['err_msg'] = 'Id chiamata sconosciuto'
    else:
        values['err'] = 1
        values['err_msg'] = 'Id chiamata non passato'

    return HttpResponse(json.dumps(values), content_type="application/json")


def cdr_export_excel(request):
    import xlwt
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('Esportazione')

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", "00:00")
    end_time = request.GET.get("end_time", "23:59")
    accountcode = request.GET.get("accountcode", "")
    dst = request.GET.get("dst", "")

    q_obj = Q(accountcode__icontains=accountcode)
    q_obj.add(Q(custom_dst__icontains=dst), Q.AND)
    q_obj.add(Q(dcontext='cabs-dial-number')|Q(dcontext='outgoing-operator-dial-number')|Q(dcontext='incoming-operator-dial-number'), Q.AND)
    q_obj.add(Q(custom_valid=1), Q.AND) # esportiamo solo le chiamate ritenute valide
    
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

    details = Detail.objects.filter(q_obj).order_by('-calldate')

    sheet.write(0, 0, "Data e ora", style=default_style)
    sheet.write(0, 1, "Codice", style=default_style)
    sheet.write(0, 2, "Cognome e Nome", style=default_style)
    sheet.write(0, 3, "Sorgente", style=default_style)
    sheet.write(0, 4, "Destinazione", style=default_style)
    sheet.write(0, 5, "Durata", style=default_style)
    sheet.write(0, 6, "Costo", style=default_style)

    for row, rowdata in enumerate(details):
        try:
            phoneuser = PhoneUser.objects.get(pincode=rowdata.accountcode)
            fullname = phoneuser.get_full_name()
        except:
            fullname = '-'

        calldate = time.strftime("%d-%m-%Y %H:%M:%S",
                                 time.strptime(str(rowdata.calldate),
                                               "%Y-%m-%d %H:%M:%S"))
        billsec = "%sm %ss" % (int(rowdata.billsec / 60), rowdata.billsec % 60)
        rowdata.price = rowdata.price > 0 and rowdata.price or 0
        sheet.write(row + 1, 0, calldate, style=datetime_style)
        sheet.write(row + 1, 1, rowdata.accountcode, style=default_style)
        sheet.write(row + 1, 2, fullname, style=default_style)
        sheet.write(row + 1, 3, rowdata.custom_src, style=default_style)
        sheet.write(row + 1, 4, rowdata.custom_dst, style=default_style)
        sheet.write(row + 1, 5, billsec, style=default_style)
        sheet.write(row + 1, 6, rowdata.price, style=default_style)

        response = HttpResponse(mimetype='application/vnd.ms-excel')
        filename = 'Dettaglio_chiamate.xls'
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % filename
        book.save(response)

    # logghiamo azione
    audit = Audit()
    audit.user = request.user
    d = request.GET.dict()
    audit.what = "L'utente %s ha esportato in formato excel una lista chiamate corrispondenti ai seguenti criteri: %s" \
        % (request.user.username, urlencode(d))
    audit.save()

    return response
