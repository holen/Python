from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from books.models import Book

#def search(request):
#    error = False
#    if 'q' in request.GET and request.GET['q']:
#        q = request.GET['q']
#        books = Book.objects.filter(title__icontains=q)
#        return render_to_response('search_results.html',
#            {'books': books, 'query': q})
#    else:
#        #return HttpResponse('Please submit a search term.')
#        return render(request, 'search_form.html', {'error': True})
#def search_form(request):
#    return render_to_response('search_form.html')

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
	elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_results.html',{'books': books, 'query': q})
    #return render_to_response('search_form.html',{'error': error})
    return render(request, 'search_form.html', {'errors': errors})
