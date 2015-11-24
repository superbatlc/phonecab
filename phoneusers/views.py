import json
from urllib import urlencode
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from phoneusers.models import PhoneUser, Whitelist, Credit
#from acls.models import Acl

from cdrs.models import Detail
from audits.models import Audit
from helper.Helper import Helper
from helper import http
from acls.models import Acl
from prefs.models import Pref
from archives.models import ArchivedPhoneUser


@login_required
def phoneuser_home(request):
    """Phoneusers page"""
    import time
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['phoneusers'] = phoneuser_items(request)
    variables['d'] = d

    return render_to_response(
        'phoneusers/home.html', RequestContext(request, variables))

def phoneuser_items(request):
    """Phoneuser Items List"""
    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)

    items_per_page = settings.ITEMS_PER_PAGE

    keyword = request.GET.get("keyword", "")
    enabled = request.GET.get("enabled", "")
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

    items_list = PhoneUser.objects.filter(q_obj).order_by('last_name')
    if enabled != "":
        items_list = items_list.filter(enabled=enabled)

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
            'phoneusers/table.html', RequestContext(request, variables))

    return render_to_string(
        'phoneusers/table.html', RequestContext(request, variables))

@login_required
def phoneuser_view(request, phoneuser_id="0"):
    """Visualizza la pagina di anagrafica"""
    phoneuser_id = int(phoneuser_id)
    if not phoneuser_id:
        raise Http404

    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    phoneuser = phoneuser_data(request, phoneuser_id)
    whitelists = whitelist_items(request, phoneuser_id)
    credits = credit_items(request, phoneuser_id)
   
    variables['phoneuser'] = phoneuser
    variables['whitelists'] = whitelists
    variables['credits'] = credits
    return render_to_response('phoneusers/page.html',
        RequestContext(request,variables))

@login_required
def phoneuser_data(request, phoneuser_id="0"):
    """Recupera e visualizza le informazioni sul phoneuser - pannello anagrafica"""
    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff) #TODO solo priv_anagrafica
    if int(phoneuser_id):
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        except:
            raise Http404
    variables['phoneuser'] = phoneuser
    if request.is_ajax():
        return render_to_response(
            'phoneusers/phoneuser_data.html', RequestContext(request, variables))
    return render_to_string(
        'phoneusers/phoneuser_data.html', RequestContext(request, variables))

@login_required
def phoneuser_edit(request):
    """Gestisce sia il new che l'edit"""
    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    phoneuser_id = request.POST.get("id", "0")
    if int(phoneuser_id):
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        except:
            raise Http404
    else:
        phoneuser = PhoneUser
        phoneuser.id = 0

    variables['phoneuser'] = phoneuser
    return render_to_response('phoneusers/phoneuser.html',
        RequestContext(request,variables))

@login_required
def phoneuser_save(request):
    """Save or update user"""
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    enabled = int(request.POST.get("data[enabled]", "0"))
    first_name = request.POST.get("data[first_name]", "")
    last_name = request.POST.get("data[last_name]", "")
    serial_no = request.POST.get("data[serial_no]", "")
    pincode = request.POST.get("data[pincode]", "")
    four_bis_limited = int(request.POST.get("data[four_bis_limited]", "0"))
    listening_enabled = int(request.POST.get("data[listening_enabled]", "0"))
    recording_enabled = int(request.POST.get("data[recording_enabled]", "0"))
    language = request.POST.get("data[language]", "")
    vipaccount = int(request.POST.get("data[vipaccount]", "0"))

    variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    is_new = False
    action = "Creazione"
    try:
        if phoneuser_id:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            action = "Modifica"
        else:
            phoneuser = PhoneUser()
            is_new = True

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

        # log azione
        audit = Audit()
        audit.log(user=request.user,
            what="%s anagrafica: %s" % (action, phoneuser))
        
        if is_new:
            return phoneuser_items(request)
        variables['phoneuser'] = phoneuser
        return render_to_response(
            'phoneusers/phoneuser_data.html', RequestContext(request, variables))
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')

@login_required
def phoneuser_check_pincode(request):
    """Verifica che il pincode sia univoco"""
    pincode = request.POST.get("pincode", "")
    check = PhoneUser.objects.filter(pincode=pincode).count()

    return HttpResponse(str(check))
    
@login_required
def phoneuser_change_status(request):
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    newstatus = request.POST.get("data[newstatus]", "")
    ret = newstatus

    action = "Disattivazione"
    if int(newstatus):
        action = "Attivazione"

    try:
        phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        phoneuser.enabled = int(newstatus)
        phoneuser.save()

        # log azione
        audit = Audit()
        audit.log(user=request.user,
            what="%s scheda anagrafica: %s" % (action, phoneuser))
        return phoneuser_data(request, phoneuser_id)
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')
    
@login_required
def phoneuser_archive(request):
    """Archiviazione anagrafica"""
    phoneuser_id = int(request.POST.get("phoneuser_id", "0"))
    try:
        if phoneuser_id:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            archived_phoneuser = ArchivedPhoneUser()
            archived_phoneuser.phoneuser = phoneuser
            archived_phoneuser.archive()
            #phoneuser.enabled = 0
            #phoneuser.save()
            return HttpResponse(status=200)
        else:
            raise Http404
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')
    
@login_required
def phoneuser_name(request, accountcode):
    """Get phoneuser name for realtime displaying"""
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
def phoneuser_realtime_info(request):
    """Get call info for realtime displaying"""
    pincode = request.POST.get("data[pincode]", "")
    dst = request.POST.get("data[dst]", "")

    values = {
              'data': {},
              'err': 0,
              'err_msg': '',
              }

    values['data']['name'] = 'Non disponibile'
    values['data']['dst'] = 'Non disponibile'
    values['data']['recording'] = 'show'
    try:
        if accountcode:
                phoneuser = PhoneUser.get_from_pincode(pincode)
                if phoneuser:
                    values['data']['name'] = phoneuser.get_full_name()
                    if phoneuser.recording_enabled:
                        values['data']['recording'] = 'progress'
                    if dst:
                        whitelist = Whitelist.objects.get(phonenumber=dst, phoneuser_id=phoneuser.id)
                        values['data']['dst'] = "%s %s" % (dst, whitelist.label)
                        if whitelist.frequency == 1:
                            values['data']['recording'] = 'hidden'


        return HttpResponse(json.dumps(values), content_type="application/json")

    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')

    




@login_required
def whitelist_items(request, phoneuser_id):
    phoneuser_id = int(phoneuser_id)
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    whitelists = Whitelist.objects.filter(
        phoneuser_id=phoneuser_id).order_by('label')

    for wl in whitelists:
        if wl.frequency == 0 or wl.frequency == 3:
            wl.times = '-'

    variables['whitelists'] = whitelists

    if request.is_ajax():
        return render_to_response(
            'phoneusers/whitelists/table.html', RequestContext(request, variables))

    return render_to_string(
        'phoneusers/whitelists/table.html', RequestContext(request, variables))


@login_required
def whitelist_edit(request):
    variables = {}
    whitelist_id = int(request.POST.get("data[id]", "0"))
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))

    if whitelist_id:
        try:
            whitelist = Whitelist.objects.get(pk=whitelist_id)
            whitelist.duration = int(whitelist.duration / 60)
            whitelist.frequency = int(whitelist.frequency)
        except:
            raise Http404
    else:
        whitelist = Whitelist()
        whitelist.duration = int(Pref.get("threshold")) / 60
        if phoneuser_id:
            try:
                whitelist.phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            except:
                raise Http404

    variables['whitelist'] = whitelist
    variables['enable_first_in'] = Pref.get("enable_first_in")
    variables['change_threshold'] = Pref.get("change_threshold")

    return render_to_response('phoneusers/whitelists/whitelist.html', variables)


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
    action = "Creazione"
    try:
        if whitelist_id:
            whitelist = Whitelist.objects.get(pk=whitelist_id)
            action = "Modifica"
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

        # log azione
        audit = Audit()
        audit.log(user=request.user,
            what="%s autorizzazione: %s" % (action, whitelist.phoneuser))
        return whitelist_items(request, phoneuser_id)
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')

    
@login_required
def whitelist_remove(request):
    whitelist_id = int(request.POST.get("data[whitelist_id]", "0"))
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))

    if(whitelist_id):
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            Whitelist.objects.get(pk=whitelist_id).delete()
            # log azione
            audit = Audit()
            audit.log(user=request.user,
                what="Rimozione autorizzazione: %s" % phoneuser)
            return whitelist_items(request, phoneuser_id)
            
        except Exception as e:
            return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')
    else:
        raise Http404

@login_required
def whitelist_change_status(request):
    whitelist_id = int(request.POST.get("data[whitelist_id]", "0"))
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    newstatus = int(request.POST.get("data[newstatus]", "0"))

    ret = newstatus

    action = "Disattivazione"
    if int(newstatus):
        action = "Attivazione"

    if(whitelist_id):
        try:
            whitelist = Whitelist.objects.get(pk=whitelist_id)
            whitelist.enabled = newstatus
            whitelist.save()
            audit = Audit()
            audit.log(user=request.user,
                what="%s autorizzazione: %s" % (action, whitelist.phoneuser))
            return whitelist_items(request, phoneuser_id)
        except Exception as e:
            return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')
    else:
        raise Http404

@login_required
def whitelist_change_ordinary(request):
    whitelist_id = int(request.POST.get("data[whitelist_id]", "0"))
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))
    newstatus = int(request.POST.get("data[newstatus]", "0"))

    ret = newstatus

    action = "Abilitazione ordinaria"
    if int(newstatus):
        action = "Abilitazione straordinaria"

    if(whitelist_id):
        try:
            whitelist = Whitelist.objects.get(pk=whitelist_id)
            whitelist.extraordinary = newstatus
            whitelist.save()
            audit = Audit()
            audit.log(user=request.user,
                what="%s autorizzazione: %s" % (action, whitelist.phoneuser))
            return whitelist_items(request, phoneuser_id)
        except Exception as e:
            return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')
    else:
        raise Http404
    

@login_required
def whitelist_check_extra(request): # TODO verificare i valori ritornati

    whitelist_id = int(request.POST.get("data[whitelist_id]", "0"))
    phoneuser_id = int(request.POST.get("data[phoneuser_id]", "0"))

    values = {
              'data': {},
              'err': 0,
              'err_msg': '',
              }

    if(whitelist_id):
        try:
            wl = Whitelist.objects.get(pk=whitelist_id)
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)

            weekcalls, monthcalls = _get_extra_call(phoneuser.pincode,
                                                     wl.phonenumber)

            values['data']['weekcalls'] = weekcalls
            values['data']['monthcalls'] = monthcalls

        except Exception as e:
            values['err'] = 1
            values['err_msg'] = e.message
    else:
        raise Http404
    #return http.JSONResponse(request, values)
    return HttpResponse(json.dumps(values), content_type="application/json")

def _get_extra_call(accountcode, dst):
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
def whitelist_check_prefix(request): # TODO verificare
    from prefs.models import Fare
    phonenumber = request.POST.get("phonenumber", "0")
    ret = 0
    if(phonenumber):
        ret = Fare.check_prefix_existance(phonenumber)

    return HttpResponse(ret, content_tyep='text/plain')


@login_required
def credit_items(request, phoneuser_id):

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
    variables['phoneuser_id'] = phoneuser_id

    if request.is_ajax():
        return render_to_response(
            'phoneusers/credits/table.html', RequestContext(request, variables))
    return render_to_string(
        'phoneusers/credits/table.html', RequestContext(request, variables))


@login_required
def credit_new(request):
    variables = {'phoneuser_id': request.POST.get("phoneuser_id", "0")}
    return render_to_response('phoneusers/credits/credit.html', variables)


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
        audit = Audit()
        audit.log(user=request.user,
            what="Effettuata ricarica di importo %s a favore di %s" % (credit.recharge, 
                credit.phoneuser))
        return credit_items(request, phoneuser_id)
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')


def credit_export(request, phoneuser_id=0):
    """Stampa bilancio"""
    import datetime
    phoneuser_id = int(phoneuser_id)
    if phoneuser_id:
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
        except:
            raise Http404

        recharges = Credit.objects.filter(phoneuser_id=phoneuser_id)
        tot_recharges = Credit.get_total(phoneuser_id)
        tot_cost = Detail.get_cost(phoneuser_id)

        variables = {
            'header': Pref.header(),
            'phoneuser': phoneuser,
            'today': datetime.date.today().strftime("%d-%m-%Y"),
            'recharges': recharges,
            'tot_recharges': tot_recharges,
            'tot_cost': tot_cost,
        }

        return render_to_response('phoneusers/credits/report.html', variables)
    else:
        raise Http404

def credit_print_recharge(request, credit_id):
    """Stampa Singola Ricarica"""
    import datetime
    credit_id = int(credit_id)
    if credit_id:
        try:
            credit = Credit.objects.get(pk=credit_id)
            phoneuser = PhoneUser.objects.get(pk=credit.phoneuser_id)
        except:
            raise Http404

        variables = {
            'header': Pref.header(),
            'phoneuser': phoneuser,
            'today': datetime.date.today().strftime("%d-%m-%Y"),
            'credit': credit,
        }

        return render_to_response('phoneusers/credits/print_receipt.html', variables)
    else:
        raise Http404