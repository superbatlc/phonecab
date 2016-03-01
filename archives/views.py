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
from audits.models import Audit
from prefs.models import Pref
from cdrs.models import SuperbaCDR


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
            archived_phoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
        except:
            raise Http404
    variables['phoneuser'] = archived_phoneuser
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
    archived_phoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    credits = ArchivedCredit.objects.filter(
        archived_phoneuser=archived_phoneuser).order_by('-recharge_date')

    variables['items'] = credits
    variables['balance'] = archived_phoneuser.balance
    variables['archived_phoneuser_id'] = archived_phoneuser_id

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
    pincode = request.GET.get("pincode", "")
    archived_phoneuser_id = request.GET.get("archived_phoneuser_id", "")
    dst = request.GET.get("dst", "")
    calltype = request.GET.get("calltype", None)
    page = int(request.GET.get("page", "1"))

    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

    q_obj = Q(pincode__icontains=pincode)
    q_obj.add(Q(dst__icontains=dst), Q.AND)

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

    if calltype:
        q_obj.add(Q(calltype=calltype), Q.AND)

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
                archived_phoneuser_id=item.archived_phoneuser_id, phonenumber=item.dst)[0]
        except Exception as e:
            item.whitelist = '-'

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
    variables['archived_phoneuser_id'] = archived_phoneuser_id

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
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
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

    items_list = ArchivedRecord.objects.filter(q_obj).order_by('-calldate')
    total_items = items_list.count()

    items, items_range, items_next_page = Helper.make_pagination(
        items_list, page, items_per_page)

    for item in items:
        try:
            details = ArchivedDetail.objects.filter(uniqueid=item.uniqueid)
            if not details:
                item.detail = SuperbaCDR
                item.detail.dst = ''
            else:
                item.detail = details[0]
            item.whitelist = ArchivedWhitelist.objects.get(
                archived_phoneuser_id=item.archived_phoneuser_id, phonenumber=item.detail.dst)
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

@login_required
def archive_cdrs_export_excel(request):
    import time
    import xlwt
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('Esportazione')

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    pincode = request.GET.get("pincode", "")
    dst = request.GET.get("dst", "")

    q_obj = Q(pincode__icontains=pincode)
    q_obj.add(Q(dst__icontains=dst), Q.AND)
    q_obj.add(Q(valid=True), Q.AND) # esportiamo solo le chiamate ritenute valide

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

    details = ArchivedDetail.objects.filter(q_obj).order_by('-calldate')

    sheet.write(0, 0, "Data e ora", style=default_style)
    sheet.write(0, 1, "Codice", style=default_style)
    sheet.write(0, 2, "Matricola", style=default_style)
    sheet.write(0, 3, "Cognome e Nome", style=default_style)
    sheet.write(0, 4, "Sorgente", style=default_style)
    sheet.write(0, 5, "Destinazione", style=default_style)
    sheet.write(0, 6, "Numero Autorizzato", style=default_style)
    sheet.write(0, 7, "Durata", style=default_style)
    sheet.write(0, 8, "Costo", style=default_style)

    for row, rowdata in enumerate(details):
        try:
            archived_phoneuser = ArchivedPhoneUser.objects.get(id=rowdata.archived_phoneuser_id)
            print archived_phoneuser
            fullname = archived_phoneuser.get_full_name()
            matricola = archived_phoneuser.serial_no
            try:
                whitelist = ArchivedWhitelist.objects.get(phonenumber=rowdata.dst,
                    archived_phoneuser=archived_phoneuser)
                whitelist_label = whitelist.label
            except:
                whitelist_label = '-'
        except:
            fullname = '-'
            matricola = '-'

        calldate = time.strftime("%d-%m-%Y %H:%M:%S",
                                 time.strptime(str(rowdata.calldate),
                                               "%Y-%m-%d %H:%M:%S"))
        billsec = "%sm %ss" % (int(rowdata.billsec / 60), rowdata.billsec % 60)
        rowdata.price = rowdata.price > 0 and rowdata.price or 0
        sheet.write(row + 1, 0, calldate, style=datetime_style)
        sheet.write(row + 1, 1, rowdata.pincode, style=default_style)
        sheet.write(row + 1, 2, matricola, style=default_style)
        sheet.write(row + 1, 3, fullname, style=default_style)
        sheet.write(row + 1, 4, rowdata.src, style=default_style)
        sheet.write(row + 1, 5, rowdata.dst, style=default_style)
        sheet.write(row + 1, 6, whitelist_label, style=default_style)
        sheet.write(row + 1, 7, billsec, style=default_style)
        sheet.write(row + 1, 8, rowdata.price, style=default_style)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = 'Dettaglio_chiamate_archiviate.xls'
    response[
        'Content-Disposition'] = 'attachment; filename=%s' % filename
    book.save(response)

    # logghiamo azione
    audit = Audit()
    audit.user = request.user
    d = request.GET.dict()
    audit.what = "Esportazione lista chiamate archiviate corrispondenti ai seguenti criteri: %s" \
        % (urlencode(d))
    audit.save()

    return response

@login_required
def archive_record_action(request, action, item, archived_record_id=0):
    """Unica funzione per gestire azioni diverse"""
    # verifichiamo che l'utente possieda i privilegi
    # e che non abbia digitato la url direttamente
    if Acl.get_permission_for_function(
            request.user.id, Acl.FUNCTION_RECORD) or request.user.is_staff:
        if action == 'remove':
            if item == 'single':
                return _single_record_remove(request, archive_record_id)
            else:
                return _multi_record_remove(request)
        elif action == 'download':
            if item == 'single':
                return _single_record_export(request, archive_record_id)
            else:
                return _multi_record_export_as_zip_file(request)
        else:
            raise Http404
    else:
        raise Http403

def _multi_record_export_as_zip_file(request):
    "Esportazione multifile in formato zip"""
    import os
    import contextlib
    import zipfile

    d = request.GET.dict()
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    pincode = request.GET.get("pincode", "")

    q_obj = Q(pincode__icontains=pincode)

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

    items_list = ArchivedRecord.objects.filter(q_obj).order_by('-calldate')

    filename = 'registrazioni'
    if pincode != '':
        try:
            phoneuser = ArchivedPhoneUser.objects.get(pincode=pincode)
            filename = 'registrazioni %s' % phoneuser
        except:
            pass
    zipname = "%s.zip" % filename
    tmpzippath = os.path.join(settings.TMP_ZIP_ROOT, zipname)
    file_counter = 0
    with contextlib.closing(zipfile.ZipFile(tmpzippath, 'w')) as myzip:
        for item in items_list:
            detail = ArchivedDetail.objects.get(uniqueid=item.uniqueid)
            if detail.valid:
                file_counter += 1
                path = os.path.join(settings.RECORDS_ROOT, item.filename)
                myzip.write(path, arcname = item.filename)

    if not file_counter:
        return redirect("/archives/records/?err=1&err_msg=Nessuno dei file soddisfa i criteri per l'esportazione&%s" % urlencode(d))

    response = Helper.file_export(tmpzippath)

    # logghiamo azione
    audit = Audit()
    audit.user_id = request.user.id
    detail = Helper.get_filter_detail(d)
    audit.what = "Esportazione registrazioni archiviate corrispondenti ai seguenti criteri: %s" \
                            % (detail)
    audit.save()

    return response

@login_required
def archive_credit_print_recharge(request, archived_credit_id):
    """Stampa Singola Ricarica"""
    import datetime
    archived_credit_id = int(archived_credit_id)
    if archived_credit_id:
        try:
            archived_credit = ArchivedCredit.objects.get(pk=archived_credit_id)
            archived_phoneuser = ArchivedPhoneUser.objects.get(pk=archived_credit.archived_phoneuser_id)
        except:
            raise Http404

        variables = {
            'header': Pref.header(),
            'phoneuser': archived_phoneuser,
            'today': datetime.date.today().strftime("%d-%m-%Y"),
            'credit': archived_credit,
        }

        return render_to_response('phoneusers/credits/print_receipt.html', variables)
    else:
        raise Http404

@login_required
def archive_credit_export(request, archived_phoneuser_id=0):
    """Stampa bilancio"""
    import datetime
    archived_phoneuser_id = int(archived_phoneuser_id)
    if archived_phoneuser_id:
        try:
            archived_phoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
        except:
            raise Http404

        recharges = ArchivedCredit.objects.filter(archived_phoneuser_id=archived_phoneuser_id)
        tot_recharges = ArchivedCredit.get_total(archived_phoneuser)
        tot_cost = ArchivedDetail.get_cost(archived_phoneuser)

        variables = {
            'header': Pref.header(),
            'phoneuser': archived_phoneuser,
            'today': datetime.date.today().strftime("%d-%m-%Y"),
            'recharges': recharges,
            'tot_recharges': tot_recharges,
            'tot_cost': tot_cost,
        }

        return render_to_response('phoneusers/credits/report.html', variables)
    else:
        raise Http404
