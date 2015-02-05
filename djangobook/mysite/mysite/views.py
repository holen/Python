from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
import datetime

def display_meta(request):
    #metas = request.META.items()
    #print request.META
    #print metas
    #metas.sort()
    #html = [] 
    #for k, v in metas:
    #    html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    #return HttpResponse('<table>%s</table>' % '\n'.join(html))
    return render(request, 'display_meta.html', {'metas': request.META, 'path': request.path})
    #for k, v in request.META.items():
#	return render(request, 'display_meta.html', {'key': k,'value': v})

#def hello(request):
#    return HttpResponse("Hello world")

#def current_datetime(request):
#    now = datetime.datetime.now()
#    t = get_template('current_datetime.html')
#    html = t.render(Context({'current_date': now}))
#    return HttpResponse(html)

def current_datetime(request):
    current_date = datetime.datetime.now()
    #return render_to_response('current_datetime.html', {'current_date': current_date})
    #return render(request, 'current_datetime.html', {'current_date': current_date})
    return render(request, 'current_datetime.html', locals())

def hours_ahead(request, offset):
    try:
        hour_offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    #return HttpResponse(html)
    return render(request, 'hours_ahead.html', {'hour_offset': hour_offset, 'next_time': dt})

#def search_form(request):
#    return render_to_response('search_form.html')

#def search(request):
#    if 'q' in request.GET:
#        message = 'You searched for: %r' % request.GET['q']
#    else:
#        message = 'You submitted an empty form.'
#    return HttpResponse(message)
