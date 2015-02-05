from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Your favorite color is %s" % request.COOKIES["favorite_color"])
    else:
        return HttpResponse("You don't have a favorite color.")

def set_color(request):
    if "favorite_color" in request.GET:

        # Create an HttpResponse object...
        response = HttpResponse("Your favorite color is now %s" % request.GET["favorite_color"])

        # ... and set a cookie on the response
        response.set_cookie("favorite_color", request.GET["favorite_color"])

        return response

    else:
        return HttpResponse("You didn't give a favorite color.")
