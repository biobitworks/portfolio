from django.shortcuts import render
from django.template import RequestContext
from labapp.models import KVP
from django.utils.timezone import datetime

def my_context_preprocessor(request):
    last_updated = KVP.objects.get(key='Last Updated').value

    return {'labname' : 'Lab Name',
        'time':datetime.now(),
        'last_updated': last_updated}
