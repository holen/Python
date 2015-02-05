from django.shortcuts import render_to_response, render
from contact.forms import ContactForm
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['823772686@qq.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})
    #return render_to_response('contact_form.html', {'form': form})
    return render(request, 'contact_form.html', {'form': form})

def thanks(request):
    return render_to_response('contact_thanks.html')
