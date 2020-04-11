from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection

class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Nombre')
    email = forms.EmailField(required=False,label='e-mail')
    subject = forms.CharField(required=False,max_length=100,label='Tema')
    message = forms.CharField(widget=forms.Textarea,label='Comentario')

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False

            con = get_connection('django.core.mail.backends.console.EmailBackend')
            body = 'De: ' + cd['message'] + '\nEmail: ' + cd['email'] + '\nMensaje: ' + cd['message']
            send_mail('Email from COVID WEBSITE'+cd['subject'], body, cd.get('email', 'noreply@example.com'), ['cesar.f.soriano@gmail.com'],
                connection=con)
            return HttpResponseRedirect('contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'contact.html', {'form': form, 'submitted': submitted})