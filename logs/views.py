from django.http import HttpResponse
from .models import Log
import json
from django.core import serializers

# Create your views here.
def get_last_logs(request,):
    max_logs_returned = 10
    logs = Log.objects.all().order_by('-when')[:max_logs_returned]

    return HttpResponse(status=200,
                        content=serializers.serialize('json', logs),
                        content_type="application/json")
