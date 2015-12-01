from urllib import urlencode
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings

from records.models import Record
from acls.models import Acl
from helper.Helper import Helper
from phoneusers.models import PhoneUser, Whitelist
from cdrs.models import Detail
from audits.models import Audit
from prefs.models import Pref, Extension
from helper.Helper import Helper
from helper.http import Http403


@login_required
def record_home(request):
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['records'] = record_items(request)
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
        'records/home.html', RequestContext(request, variables))

@login_required
def record_items(request):
    """Record Items"""
    from urllib import urlencode
    variables = {}

    items_per_page = settings.ITEMS_PER_PAGE

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", "00:00")
    end_time = request.GET.get("end_time", "23:59")
    pincode = request.GET.get("pincode", "")
    page = int(request.GET.get("page", "1"))
    d = request.GET.dict()

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

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

    items_list = Record.objects.filter(q_obj).order_by('-calldate')
    total_items = items_list.count()

    items, items_range, items_next_page = Helper.make_pagination(
        items_list, page, items_per_page)

    for item in items:
        item.phoneuser = PhoneUser.get_from_pincode(item.pincode)
        try:
            details = Detail.objects.filter(uniqueid=item.uniqueid)
            if not details:
                item.detail = Detail
                item.detail.custom_dst = ''
            else:
                item.detail = details[0]
                src_name = Extension.get_extension_name(item.detail.custom_src)
                if src_name:
                    item.detail.custom_src = "%s (%s)" % (src_name, item.detail.custom_src)
                    print item.detail.custom_src
            item.whitelist = Whitelist.objects.get(
                phoneuser_id=item.phoneuser.id, phonenumber=item.detail.custom_dst)
        except Exception as e:
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
            'records/table.html', RequestContext(request, variables))

    return render_to_string(
        'records/table.html', RequestContext(request, variables))

@login_required
def record_action(request, action, item, record_id=0):
    """Unica funzione per gestire azioni diverse"""
    # verifichiamo che l'utente possieda i privilegi
    # e che non abbia digitato la url direttamente
    if Acl.get_permission_for_function(
            request.user.id, Acl.FUNCTION_RECORD) or request.user.is_staff:
        if action == 'remove':
            if item == 'single':
                return _single_record_remove(request, record_id)
            else:
                return _multi_record_remove(request)
        elif action == 'download':
            if item == 'single':
                return _single_record_export(request, record_id)
            else:
                return _multi_record_export_as_zip_file(request)
        else:
            raise Http404
    else:
        raise Http403

def _single_record_export(request, record_id="0"):
    """Esportazione singolo file"""
    import os

    record_id = int(record_id)
    try:
        record = Record.objects.get(pk=record_id)
    except ObjectDoesNotExist:
        pass

    path = os.path.join(settings.RECORDS_ROOT, record.filename)
    response = Helper.file_export(path)

    # logghiamo azione
    audit = Audit()
    audit.user = request.user
    audit.what = "L'utente %s ha scaricato il seguente file: %s" \
        % (request.user.username, record.filename)
    audit.save()

    return response

def _multi_record_export_as_zip_file(request):
    "Esportazione multifile in formato zip"""
    import os
    import contextlib
    import zipfile

    d = request.GET.dict()
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    start_time = request.GET.get("start_time", "00:00")
    end_time = request.GET.get("end_time", "23:59")
    pincode = request.GET.get("pincode", "")

    q_obj = Q(pincode__icontains=pincode)

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

    items_list = Record.objects.filter(q_obj).order_by('-calldate')
    
    filename = 'registrazioni'
    if pincode != '':
        phoneuser = PhoneUser.get_from_pincode(pincode)
        filename = 'registrazioni %s' % phoneuser
    zipname = "%s.zip" % filename
    tmpzippath = os.path.join(settings.TMP_ZIP_ROOT, zipname)
    file_counter = 0
    with contextlib.closing(zipfile.ZipFile(tmpzippath, 'w')) as myzip:
        for item in items_list:
            
            detail = Detail.objects.get(uniqueid=item.uniqueid) 
            if detail.custom_valid and (detail.dcontext == 'cabs-dial-number' or detail.dcontext == 'outgoing-operator-dial-number' or detail.dcontext == 'incoming-operator-dial-number'):
                file_counter += 1
                path = os.path.join(settings.RECORDS_ROOT, item.filename)
                myzip.write(path, arcname = item.filename) #TODO: verificare effettiva esportazione
        
    if not file_counter:
        return redirect("/records/?err=1&err_msg=Nessuno dei file soddisfa i criteri per l'esportazione&%s" % urlencode(d))

    response = Helper.file_export(tmpzippath)

    # logghiamo azione
    audit = Audit()
    audit.user_id = request.user.id
    detail = Helper.get_filter_detail(d)
    audit.what = "Esportazione registrazioni corrispondenti ai seguenti criteri: %s" \
                            % (detail)
    audit.save()

    return response

def _single_record_remove(request, record_id):
    """Rimozione fisica singolo record"""
    try:
        Record.objects.get(pk=record_id).delete_all(True)
        ret = "1"
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        ret = "0"

    return HttpResponse(ret)

def _multi_record_remove(request):
    """
    import os
    d = request.GET.dict()
    cursor = connection.cursor()
    query_raw = _create_q_raw_from_filters(d,'')
    record_list_raw = query_get_list(cursor, '*', 'records_record',
        query_raw, 'deleted=0','' )
    record_list = Record.fill_model_list(record_list_raw)
    """
    ret = "1"
    """
    for record in record_list:
        path = os.path.join(settings.RECORDS_ROOT,record.filename)
        print path
        query = "UPDATE records_record SET deleted='1'
                WHERE id='%s'" % record.id
        try:
            cursor.execute(query)
            #os.remove(path)
        except Exception as e:
            print "%s" % e
            ret = "0"
    """
    return HttpResponse(ret)
