import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from phoneusers.models import PhoneUser, Whitelist, Credit
#from acls.models import Acl

from cdrs.models import Detail
from audits.models import Audit
from helper.Helper import Helper
from helper import http
from acls.models import Acl
from archives.models import ArchivedPhoneUser


@login_required
def phoneuser_view(request, phoneuser_id):
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)

    if int(phoneuser_id):
        # richiesta di modifica di un'anagrafica esistente
        try:
            variables['phoneuser'] = PhoneUser.objects.get(pk=phoneuser_id)
            variables['whitelists'] = Whitelist.objects.filter(
                phoneuser_id=phoneuser_id).order_by('label')
            # Credit.objects.filter(phoneuser_id=phoneuser_id).order_by('-recharge_date')
            variables['credits'] = credit_list(request, phoneuser_id)

            return render_to_response(
                'phoneusers/home.html', RequestContext(request, variables))

        except Exception as e:  # ObjectDoesNotExist:
            print '%s (%s)' % (e.message, type(e))
            # print "No phoneuser associated with id: %s" % phoneuser_id
            raise Http404
    else:
        raise Http404


@login_required
def phoneuser_edit(request, phoneuser_id="0"):
    """Gestisce sia il new che l'edit"""
    if int(phoneuser_id):
        # richiesta di modifica di un'anagrafica esistente
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            variables = {
                'phoneuser': phoneuser,
            }
            return render_to_response(
                'phoneusers/anagrafica_modal.html',
                RequestContext(
                    request,
                    variables))

        except ObjectDoesNotExist:
            print "No phoneuser associated with id: %s" % phoneuser_id
            raise Http404
    else:
        phoneuser = PhoneUser
        phoneuser.id = 0
        variables = {
                'phoneuser': phoneuser,
            }

        return render_to_response(
            'phoneusers/anagrafica_modal.html', RequestContext(request, {}))


@login_required
def phoneuser_save(request):
    """Save or update user"""
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    enabled = int(request.POST.get("data[enabled]", "0"))
    first_name = request.POST.get('data[first_name]', '')
    last_name = request.POST.get("data[last_name]", "")
    serial_no = request.POST.get('data[serial_no]', '')
    pincode = request.POST.get("data[pincode]", "")
    four_bis_limited = int(request.POST.get("data[four_bis_limited]", "0"))
    listening_enabled = int(request.POST.get("data[listening_enabled]", "0"))
    recording_enabled = int(request.POST.get("data[recording_enabled]", "0"))
    language = request.POST.get("data[language]", "")
    vipaccount = int(request.POST.get("data[vipaccount]", "0"))

    try:
        if phoneuser_id:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        else:
            phoneuser = PhoneUser()

        phoneuser.enabled = enabled
        phoneuser.first_name = first_name.title()
        phoneuser.last_name = last_name.title()
        phoneuser.serial_no = serial_no
        phoneuser.pincode = pincode
        phoneuser.four_bis_limited = four_bis_limited
        phoneuser.listening_enabled = listening_enabled
        phoneuser.recording_enabled = recording_enabled
        phoneuser.language = language
        phoneuser.vipaccount = vipaccount

        phoneuser.save()
        ret = phoneuser.id
    except:
        ret = "0"

    return HttpResponse(ret, mimetype='text/plain')


@login_required
def phoneuser_check_pincode(request):
    """Verifica che il pincode sia univoco"""
    pincode = request.POST.get("pincode", "")
    check = PhoneUser.objects.filter(pincode=pincode).count()

    if(check > 0):
        return HttpResponse('1')
    return HttpResponse('0')


@login_required
def phoneuser_enable(request, phoneuser_id):
    ret = "1"
    try:
        phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        phoneuser.enabled = 1
        phoneuser.save()
    except:
        ret = "0"
    return HttpResponse(ret, mimetype='text/plain')


@login_required
def phoneuser_disable(request, phoneuser_id):
    ret = "1"
    try:
        phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        phoneuser.enabled = 0
        phoneuser.save()
    except:
        ret = "0"
    return HttpResponse(ret, mimetype='text/plain')


@login_required
def phoneuser_archive(request, phoneuser_id):
    ret = "1"
    try:
        phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        archived_phoneuser = ArchivedPhoneUser(phoneuser=phoneuser)
        archived_phoneuser.archive()
        #phoneuser.enabled = 0
        #phoneuser.save()
    except Exception as e:
        print "Errore archiviazione %s" % format(e)
        ret = "0"
    return HttpResponse(ret, mimetype='text/plain')


@login_required
def phoneuser_export(request, accountcode="0"):
    """Esportazione contratto telefonico"""
    import time
    import xlwt

    #phoneuser_id = int(phoneuser_id)
    print "accountcode: %s" % accountcode
    if accountcode:
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('Estratto Conto Telefonico')

        default_style = xlwt.Style.default_style
        datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')

        details = Detail.objects.filter(
            accountcode=accountcode, disposition="ANSWERED").order_by('calldate')

        phoneuser = PhoneUser.objects.get(pincode=accountcode)

        sheet.write(0, 0, "Data e ora", style=default_style)
        sheet.write(0, 1, "Codice", style=default_style)
        sheet.write(0, 2, "Cognome e Nome", style=default_style)
        sheet.write(0, 3, "Sorgente", style=default_style)
        sheet.write(0, 4, "Destinazione", style=default_style)
        sheet.write(0, 5, "Durata", style=default_style)
        sheet.write(0, 6, "Costo", style=default_style)

        row = 0
        for row, rowdata in enumerate(details):
            #calldate = BeeFunction.convert_datetime_format(str(rowdata.calldate),"%Y-%m-%d %H:%i:%s", "%d-%m-%Y %H:%i:%s")
            calldate = time.strftime("%d-%m-%Y %H:%M:%S",
                                     time.strptime(str(rowdata.calldate),
                                                   "%Y-%m-%d %H:%M:%S"))
            billsec = "%sm %ss" % (int(rowdata.billsec / 60), rowdata.billsec % 60)
            rowdata.price = rowdata.price > 0 and rowdata.price or 0
            sheet.write(row + 1, 0, calldate, style=datetime_style)
            sheet.write(row + 1, 1, rowdata.accountcode, style=default_style)
            sheet.write(row + 1, 2, phoneuser.get_full_name(), style=default_style)
            sheet.write(row + 1, 3, rowdata.custom_src, style=default_style)
            sheet.write(row + 1, 4, rowdata.custom_dst, style=default_style)
            sheet.write(row + 1, 5, billsec, style=default_style)
            sheet.write(row + 1, 6, rowdata.price, style=default_style)

        try:
            phoneuser = PhoneUser.objects.get(pincode=accountcode)
            residuo = "%s" % phoneuser.balance
        except:
            residuo = "0.00"

        sheet.write(row + 2, 4, "Valore residuo:", style=default_style)
        sheet.write(row + 2, 5, residuo, style=default_style)

        response = HttpResponse(mimetype='application/vnd.ms-excel')
        filename = 'Estratto_conto_telefonico_%s.xls' % phoneuser.get_full_name().replace(" ","_")
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % filename
        book.save(response)

        # logghiamo azione
        audit = Audit()
        audit.user = request.user
        detail = "Codice: %s" % accountcode
        audit.what = "L'utente %s ha esportato in formato excel una lista chiamate corrispondenti ai seguenti criteri: %s" \
            % (request.user.username, detail)
        audit.save()

        return response


@login_required
def phoneuser_ajax_view(request, phoneuser_id="0"):
    phoneuser_id = int(phoneuser_id)
    if phoneuser_id:
        user = request.user
        variables = Acl.get_permissions_for_user(user.id, user.is_staff)
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            variables['phoneuser'] = phoneuser
        except ObjectDoesNotExist:
            # print "No phoneuser associated with id: %s" % phoneuser_id
            raise Http404

        return render_to_response(
            'phoneusers/anagrafica_ajax_view.html',
            RequestContext(
                request,
                variables))
    else:
        return HttpResponse("", mimetype='text/plain')


@login_required
def phoneuser_name(request, accountcode):
    values = {
              'data': {},
              'err': 0,
              'err_msg': '',
              }

    values['data']['name'] = 'Non disponibile'
    values['data']['recording'] = False
    if accountcode:
        phoneuser = PhoneUser.get_from_pincode(accountcode)
        if phoneuser:
            values['data']['name'] = phoneuser.get_full_name()
            values['data']['recording'] = phoneuser.recording_enabled
    else:
        values['err'] = 1
        values['err_msg'] = 'Errore phoneuser_name'

    return HttpResponse(json.dumps(values), content_type="application/json")


@login_required
def whitelist_list(request, phoneuser_id):
    phoneuser_id = int(phoneuser_id)
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    whitelists = Whitelist.objects.filter(
        phoneuser_id=phoneuser_id).order_by('label')

    for wl in whitelists:
        if wl.frequency == 0 or wl.frequency == 3:
            wl.times = '-'

    variables['whitelists'] = whitelists

    return render_to_response(
        'phoneusers/whitelists_list.html', RequestContext(request, variables))


@login_required
def whitelist_edit(request, whitelist_id="0"):
    variables = {}
    variables['phoneuser_id'] = request.POST.get("phoneuser_id", "0")

    if int(whitelist_id):
        # richiesta di modifica di una whitelist esistente
        try:
            whitelist = Whitelist.objects.get(pk=whitelist_id)
            whitelist.duration = int(whitelist.duration / 60)
            whitelist.frequency = int(whitelist.frequency)
        except ObjectDoesNotExist:
            # print "No whitelesit associated with id: %s" % whitelist_id
            raise Http404
    else:
        whitelist = Whitelist()
        whitelist.phoneuser = PhoneUser.objects.get(pk=variables['phoneuser_id'])

    variables['wl'] = whitelist

    return render_to_response('phoneusers/whitelist_modal.html', variables)


@login_required
def whitelist_save(request):
    """Save or update whitelist"""
    whitelist_id = int(request.POST.get("data[whitelist_id]", "0"))
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    label = request.POST.get("data[label]", "")
    phonenumber = request.POST.get("data[phonenumber]", "")
    duration = int(request.POST.get("data[duration]", "0"))
    frequency = int(request.POST.get("data[frequency]", "0"))
    real_mobile = int(request.POST.get("data[real_mobile]", "0"))

    # la maschera consente di inserire i minuti
    duration = duration * 60

    ret = "1"
    try:
        if whitelist_id:
            whitelist = Whitelist.objects.get(pk=whitelist_id)
        else:
            whitelist = Whitelist()
            if frequency == 0:
                whitelist.enabled = True

        whitelist.phoneuser_id = phoneuser_id
        whitelist.label = label
        whitelist.phonenumber = phonenumber
        whitelist.duration = duration
        whitelist.frequency = frequency
        whitelist.real_mobile = real_mobile

        whitelist.save()
    except:
        ret = "0"

    return HttpResponse(ret, mimetype='text/plain')


@login_required
def whitelist_remove(request):
    whitelist_id = int(request.POST.get("whitelist_id", "0"))
    ret = 0
    if(whitelist_id):
        try:
            Whitelist.objects.get(pk=whitelist_id).delete()
            ret = 1
        except:
            ret = 0

    return HttpResponse(ret, mimetype='text/plain')


@login_required
def whitelist_changestatus(request):
    whitelist_id = int(request.POST.get("whitelist_id", "0"))
    value = request.POST.get("value", "false") == 'true'

    ret = 0
    if(whitelist_id):
        try:
            wl = Whitelist.objects.get(pk=whitelist_id)
            wl.enabled = not value  # we change the actual state
            wl.save()
            ret = 1
        except:
            ret = 0

    return HttpResponse(ret, mimetype='text/plain')


@login_required
def whitelist_changeordinary(request):
    whitelist_id = int(request.POST.get("whitelist_id", "0"))
    value = request.POST.get("value", "false") == 'true'

    ret = 0
    if(whitelist_id):
        try:
            wl = Whitelist.objects.get(pk=whitelist_id)
            wl.extraordinary = not value  # we change the straordinary
            wl.save()
            ret = 1
        except:
            ret = 0

    return HttpResponse(ret, mimetype='text/plain')


@login_required
def whitelist_checkextra(request):


    whitelist_id = int(request.POST.get("whitelist_id", "0"))

    values = {
              'data': {},
              'err': 0,
              'err_msg': '',
              }

    if(whitelist_id):
        try:
            wl = Whitelist.objects.get(pk=whitelist_id)

            weekcalls, monthcalls = get_extra_call(wl.phoneuser.pincode,
                                                     wl.phonenumber)

            values['data']['weekcalls'] = weekcalls
            values['data']['monthcalls'] = monthcalls

        except Exception as e:
            values['err'] = 1
            values['err_msg'] = e.message

    #return http.JSONResponse(request, values)
    return HttpResponse(json.dumps(values), content_type="application/json")


def get_extra_call(accountcode, dst):
    import datetime
    from django.db import connection

    cursor = connection.cursor()
    weekcalls = 0
    monthcalls = 0

    # cerchiamo quante chiamate sono state effettuate
    # da accountcode all dst indicata
    # nella settimana e nel mese
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # lunedi di questa settimana
    previous_monday = (today - datetime.timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    query = """SELECT COUNT(*) AS n FROM cdrs_detail
            WHERE accountcode='%s' AND DATE(calldate)>='%s'
            AND DATE(calldate) <= '%s' AND custom_calltype = 1
            AND lastapp='Dial' AND custom_valid=1
            AND (dcontext='cabs-dial-number'
            OR dcontext='outgoing-operator-dial-number'
            OR dcontext='incoming-operator-dial-number')""" % (accountcode,
                                     previous_monday,
                                     yesterday_str)

    cursor.execute(query)
    calls = cursor.fetchone()
    weekcalls = calls[0]

    # primo giorno del mese
    first_of_month = today.replace(day=1).strftime("%Y-%m-%d")
    query = """SELECT COUNT(*) AS n FROM cdrs_detail
            WHERE accountcode='%s' AND DATE(calldate)>='%s'
            AND DATE(calldate) <= '%s' AND custom_calltype = 1
            AND lastapp='Dial' AND custom_valid=1
            AND (dcontext='cabs-dial-number'
            OR dcontext='outgoing-operator-dial-number'
            OR dcontext='incoming-operator-dial-number')""" % (accountcode,
                                     first_of_month,
                                     yesterday_str)
    cursor.execute(query)
    calls = cursor.fetchone()
    monthcalls = calls[0]

    return (weekcalls, monthcalls)


@login_required
def whitelist_check_prefix(request):
    from prefs.models import Fare
    phonenumber = request.POST.get("phonenumber", "0")
    ret = 0
    if(phonenumber):
        ret = Fare.check_prefix_existance(phonenumber)

    return HttpResponse(ret, mimetype='text/plain')


@login_required
def credit_list(request, phoneuser_id):

    items_per_page = 10

    d = request.GET.dict()
    phoneuser_id = int(phoneuser_id)
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    items_list = Credit.objects.filter(
        phoneuser_id=phoneuser_id).order_by('-recharge_date')
    total_items = items_list.count()
    try:
        phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
    except ObjectDoesNotExist:
        # print "No phoneuser associated with id: %s" % phoneuser_id
        raise Http404

    page = 1
    if 'page' in d.keys():
        page = int(d['page'])
        # elimino la pagina dal dizionario
        del d['page']

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
    variables['d'] = d
    variables['balance'] = phoneuser.balance

    if request.is_ajax():
        return render_to_response(
            'phoneusers/credits_list.html', RequestContext(request, variables))
    return render_to_string(
        'phoneusers/credits_list.html', RequestContext(request, variables))


@login_required
def credit_new(request):
    variables = {'phoneuser_id': request.POST.get("phoneuser_id", "0")}
    return render_to_response('phoneusers/credit_modal.html', variables)


@login_required
def credit_save(request):
    """Save credit"""
    from decimal import Decimal
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    recharge = request.POST.get('data[recharge]', "0")
    reason = request.POST.get('data[reason]', "")

    recharge = recharge.replace(",", ".")

    credit = Credit()

    credit.phoneuser_id = phoneuser_id
    credit.recharge = Decimal(recharge)
    credit.reason = reason

    ret = "1"
    try:
        #credit.save(user_id=request.user.id, phoneuser_id=phoneuser_id)
        credit.save()
        phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        # eliminiamo eventuali valori residui negativi
        if phoneuser.balance > 0:
            phoneuser.balance += Decimal(recharge)
        else:
            phoneuser.balance = Decimal(recharge)
        phoneuser.save()
    except Exception as e:
        ret = "0"

    return HttpResponse(ret, mimetype='text/plain')
