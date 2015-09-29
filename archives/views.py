from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from acls.models import Acl
from archives.models import ArchivedPhoneUser, ArchivedWhitelist, ArchivedCredit
from helper.Helper import Helper


@login_required
def archived_phoneuser_view(request, archived_phoneuser_id):
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)

    if int(archived_phoneuser_id):
        try:
            archived_phoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
            variables['archived_phoneuser'] = archived_phoneuser
            variables['archived_whitelists'] = archived_phoneuser.archivedwhitelist_set.order_by('label')
            # Credit.objects.filter(phoneuser_id=phoneuser_id).order_by('-recharge_date')
            variables['archived_credits'] = archivedcredit_list(request, archived_phoneuser.id)

            return render_to_response(
                'archives/home.html', RequestContext(request, variables))

        except Exception as e:  # ObjectDoesNotExist:
            print '%s (%s)' % (e.message, type(e))
            # print "No archivedphoneuser associated with id: %s" % archived_phoneuser_id
            raise Http404
    else:
        raise Http404
    
@login_required
def archivedcredit_list(request, archived_phoneuser_id):

    items_per_page = 10

    d = request.GET.dict()
    try:
        archived_phoneuser = ArchivedPhoneUser.objects.get(pk=archived_phoneuser_id)
    except ObjectDoesNotExist:
        # print "No archivedphoneuser associated with id: %s" % archivedphoneuser_id
        raise Http404
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    items_list = archived_phoneuser.archivedcredit_set.order_by('-recharge_date')
    total_items = items_list.count()

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
    variables['balance'] = archived_phoneuser.balance

    if request.is_ajax():
        return render_to_response(
            'archives/credits_list.html', RequestContext(request, variables))
    return render_to_string(
        'archives/credits_list.html', RequestContext(request, variables))