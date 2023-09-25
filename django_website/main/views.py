from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users.models import Contact
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

from users.models import SubscribedUsers
from django.contrib import messages
from django.core.mail import EmailMessage

import os
from uuid import uuid4

from main.decorators import user_is_superuser
from .forms import NewsletterForm
from users.models import SubscribedUsers


# from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def support(request):
    return render(request, "spport a cause.html")

def members(request):
    return render(request, "member.html")

@login_required
def service(request):
    return render(request, "service.html")

def ourteam(request):
    return render(request, "our team.html")

def about(request):
    return render(request, "about.html")


def partners(request):
    return render(request, "partners.html")

def joinus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        state = request.POST.get('state')
        transaction = request.POST.get('transaction')
        message = request.POST.get('message')
        joinus = Joinus(name=name,state=state, transaction=transaction, message=message, date= datetime.today())
        joinus.save()
    return render(request, "Join Us.html")


def contact(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(firstname=firstname,lastname=lastname, email=email, subject=subject, message=message, date= datetime.today())
        contact.save()

        send_mail(
            "Thankyou for Contacting me.",
            "Hello, my friend i will contact you very soon.",
            "mrsculture.offical@gmail.com",
            [email],
            fail_silently=False,
        )
    return render(request, "contact.html")


@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject')
            receivers = request.POST.get('receivers').split(',')
            email_message = request.POST.get('message')

            mail = EmailMessage(subject, email_message, f"Helping Hands <{request.user.email}>", bcc=receivers)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent succesfully")
            else:
                messages.error(request, "There was an error sending email")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('/')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='newsletter.html', context={'form': form})