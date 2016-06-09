import json
import datetime
from django.http import HttpResponse
from django.core import serializers
from .models import Log



# Create your views here.
def get_last_logs(request, pk=None):

    if pk:
        logs = Log.objects.filter(pk__gt=pk).order_by('when')
    else:
        today = datetime.datetime.today()
        midnight = today.replace(hour=0, minute=0, second=0)

        logs = Log.objects.filter(when__gte=midnight).order_by('when')

    for log in logs:
        log.kind_str = log.get_kind_display()

    return HttpResponse(status=200,
                        content=serializers.serialize('json', logs),
                        content_type="application/json")
