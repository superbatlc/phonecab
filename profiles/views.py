import json
from django.http import Http404
from urllib import urlencode
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from helper.Helper import Helper
from acls.models import Acl


@login_required
def profile_home(request):
    d = request.GET.dict()
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['profiles'] = profile_items(request)
    variables['d'] = d

    return render_to_response(
        'profiles/home.html', RequestContext(request, variables))

def profile_items(request):
    """Phoneuser Items Table"""
    #variables = Acl.get_permissions_for_user(request.user.id, request.user.is_staff)
    variables = {}
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
    q_obj.add(Q(username__icontains=keyword), Q.OR)

    items_list = User.objects.filter(q_obj).order_by('last_name').exclude(is_superuser=True)
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
            'profiles/table.html', RequestContext(request, variables))

    return render_to_string(
        'profiles/table.html', RequestContext(request, variables))

@login_required
def profile_edit(request):
    variables = {}
    profile_id = int(request.POST.get("id", "0"))

    if profile_id:
        try:
            profile = User.objects.get(pk=profile_id)
            variables = Acl.get_permissions_for_user(profile.id, profile.is_staff)
            variables['profile'] = profile
        except ObjectDoesNotExist:
            raise Http404

    return render_to_response('profiles/profile.html', variables)

@login_required
def profile_save(request):
    """Save or update user"""
    user_id = int(request.POST.get("data[profile_id]", "0"))
    first_name = request.POST.get("data[first_name]", "")
    last_name = request.POST.get("data[last_name]", "")
    username = request.POST.get("data[username]", "")
    password = request.POST.get("data[password]", "")
    is_admin = request.POST.get("data[is_admin]", "0") == "1"

    priv_anagrafica = int(request.POST.get("data[priv_anagrafica]", "1"))
    priv_whitelist = int(request.POST.get("data[priv_whitelist]", "0"))
    priv_credit = int(request.POST.get("data[priv_credit]", "0"))
    priv_cdr = int(request.POST.get("data[priv_cdr]", "0"))
    priv_record = int(request.POST.get("data[priv_record]", "0"))

    action = "Creazione"
    try:
        if user_id:
            user = User.objects.get(pk=user_id)
            print user
            user.first_name = first_name.title()
            user.last_name = last_name.title()
            user.username = username
            if password:
                user.set_password(password)
            action = "Modifica"
        else:
            user = User.objects.create_user(username=username,
                first_name=first_name,
                last_name=last_name,
                password=password)

        user.is_staff = is_admin
        user.save()
        # log azione
        audit = Audit()
        audit.log(user=request.user,
            what="%s utente: %s" % (action, user.get_full_name()))

        if not user.is_staff:
            # cancelliamo tutte le acl utente e
            # (ri)creiamo le acl corrispondenti
            Acl.objects.filter(user_id=user.id).delete()
            # userid function permission
            Acl.objects.create(
                user_id=user.id, function=0, permission=priv_anagrafica)
            if priv_whitelist:
                Acl.objects.create(
                    user_id=user.id, function=1, permission=priv_whitelist)
            if priv_credit:
                Acl.objects.create(
                    user_id=user.id, function=2, permission=priv_credit)
            if priv_cdr:
                Acl.objects.create(
                    user_id=user.id, function=3, permission=priv_cdr)
            if priv_record:
                Acl.objects.create(
                    user_id=user.id, function=4, permission=priv_record)

        return profile_items(request)
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')


@login_required
def profile_check_username(request):
    """Verifica che lo username sia univoco"""
    username_to_check = request.POST.get("username", "")
    check = User.objects.filter(username=username_to_check).count()

    return HttpResponse(str(check))


def profile_change_status(request):
    """Disabilita utente"""
    user_id = int(request.POST.get("data[id]", "0"))
    is_active = int(request.POST.get("data[is_active]", "0"))

    action = "Disabilitazione"
    if is_active:
        action = "Abilitazione"
    try:
        if user_id:        
            user = User.objects.get(pk=user_id)
            user.is_active = is_active
            user.save()
            print user
            # log azione
            #audit = Audit()
            #audit.log(user=request.user,
            #    what="%s utente: %s" % (action, user))
            return profile_items(request)
        else:
            raise Http404
    except Exception as e:
        return HttpResponse(status=400, content=json.dumps({'err_msg': format(e)}), content_type='application/json')