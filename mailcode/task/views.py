# Create your views here.
import common.mdb as mdb
from datetime import datetime, time, timedelta, date
from django.http import HttpResponse
from django.template import loader, Context
from annoying.decorators import render_to
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@render_to('task/search1.html')

def search(request):
    return locals()

def task(request):
    return locals()

if __name__ == '__main__':
    task();
