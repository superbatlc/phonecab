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
from cdrs.models import SuperbaCDR
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
    dst = request.GET.get("dst", "")
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

    # se filtriamo per destinazione dobbiamo visualizzare solo
    # i record associati a una chiamata
    if dst != '':
        filtered_item_list = []
        for item in items_list:
            try:
                detail = SuperbaCDR.objects.get(uniqueid=item.uniqueid)
                if dst == detail.dst:
                    filtered_item_list.append(item)
            except:
                pass
        items_list = filtered_item_list

    total_items = len(items_list)

    items, items_range, items_next_page = Helper.make_pagination(
        items_list, page, items_per_page)

    for item in items:
        item.phoneuser = PhoneUser.get_from_pincode(item.pincode)
        try:
            details = SuperbaCDR.objects.filter(uniqueid=item.uniqueid)
            if not details:
                item.detail = SuperbaCDR
                item.detail.dst = ''
            else:
                item.detail = details[0]
                item.detail.src = Extension.get_extension_name(item.detail.src)
            item.whitelist = Whitelist.objects.get(
                phoneuser=item.phoneuser, phonenumber=item.detail.dst)
        except Exception as e:
            return redirect("/records/?err=1&err_msg=Impossibile caricare la lista dei record")

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

def _multi_record_export_as_zip_file(request): #TODO VERIFICARE
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
            
            detail = SuperbaCDR.objects.get(uniqueid=item.uniqueid) 
            if detail.valid:
                file_counter += 1
                path = os.path.join(settings.RECORDS_ROOT, item.filename)
                myzip.write(path, arcname = item.filename)
        
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

def record_show_warning(request):
    return render_to_response('records/show_warning.html',
        RequestContext(request,{}))


def _single_record_remove(request, record_id):
    """Rimozione fisica singolo record"""
    try:
        Record.objects.get(pk=record_id).delete_all(True)
        ret = "1"
    except Exception as e:
        # print '%s (%s)' % (e.message, type(e)) # TODO gestire errore
        ret = "0"

    return HttpResponse(ret)

def _multi_record_remove(request):
    
    import os
    d = request.POST.dict()
    start_date = request.POST.get("data[start_date]", "")
    end_date = request.POST.get("data[end_date]", "")
    start_time = request.POST.get("data[start_time]", "00:00")
    end_time = request.POST.get("data[end_time]", "23:59")
    dst = request.POST.get("data[dst]", "")
    pincode = request.POST.get("data[pincode]", "")

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

    if dst != '':
        filtered_item_list = []
        for item in items_list:
            try:
                detail = SuperbaCDR.objects.get(uniqueid=item.uniqueid)
                if dst in detail.dst:
                    filtered_item_list.append(item)
            except:
                pass
        items_list = filtered_item_list

    for item in items_list:
        path = os.path.join(settings.RECORDS_ROOT, item.filename)
        
        try:
            os.remove(path)
            item.delete()
            # logghiamo azione
            audit = Audit()
            audit.user_id = request.user.id
            detail = Helper.get_filter_detail(d)
            if detail == '':
                detail = 'Tutte le registrazioni'
            audit.what = "Eliminazione registrazioni corrispondenti ai seguenti criteri: %s" \
                                    % (detail)
            audit.save()

        except Exception as e:
            return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')

    return HttpResponse(status=200)

