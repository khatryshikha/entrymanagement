import os
from datetime import datetime
from uuid import uuid4

from django.conf import settings
# from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from twilio.rest import Client
from django.contrib import messages

from twilio.base.exceptions import TwilioRestException

from .models import Host, Visitor
from .utils import visitorCheckinNotification, visitorCheckoutNotification
from .exceptions import SMSNotSent
# Homepage


def index(request):
    return render(request, 'index.html')


# Host's Details

def host_details(request):
    try:
        if(request.method == 'POST'):
            phone_no = int(request.POST['Phone'])
            host_object = Host()
            host_object.id = str(uuid4())
            host_object.first_name = request.POST['FirstName']
            host_object.last_name = request.POST['LastName']
            host_object.Email_ID = request.POST['EmailAddress']
            host_object.Phone_No = phone_no
            host_object.save()
            request.session['host_id'] = host_object.id

            return redirect('/visitor_details')
        else:
            return render(request, 'host_details.html')
    except ValueError as e:
        context = {
            'value': "Phone number should be integer. "
        }
        return render(request, '404.html', context=context)
    except Exception as e:
        print(e)
        context = {
            'value': "Sorry! Some error occured"
        }
        return render(request, '404.html', context=context)


# Visitor's details

def visitor_details(request):
    try:
        if(request.method == 'POST'):
            phone_no = int(request.POST['Phone'])
            visitor_object = Visitor()
            visitor_object.id = str(uuid4())
            visitor_object.host_id = Host.objects.get(
                id=request.session['host_id'])
            visitor_object.first_name = request.POST['FirstName']
            visitor_object.last_name = request.POST['LastName']
            visitor_object.Email_ID = request.POST['EmailAddress']
            visitor_object.Phone_No = phone_no
            visitor_object.save()
            request.session['visitor_id'] = visitor_object.id
            visitor_details = {
                'id': visitor_object.id,
                'first_name': visitor_object.first_name,
                'last_name': visitor_object.last_name,
                'Email_ID': visitor_object.Email_ID,
                'Phone_No': visitor_object.Phone_No}
            host_object_ref = Host.objects.get(id=request.session['host_id'])
            host_details = {
                'id': host_object_ref.id,
                'first_name': host_object_ref.first_name,
                'last_name': host_object_ref.last_name,
                'Email_ID': host_object_ref.Email_ID,
                'Phone_No': host_object_ref.Phone_No}
            visitorCheckinNotification(host_details, visitor_details)
            messages.success(request, 'Visitor successfully checked in! SMS and EMails send')
            return render(request, 'index.html')
            return render(request, 'success.html')
        else:
            return render(request, 'visitor_details.html')
    except ValueError as e:
        print(e)
        context = {
            'value': "Phone number should be integer. "
        }
        return render(request, '404.html', context=context)
    except SMSNotSent as smserr:
        print(smserr)
        messages.error(request, 'Visitor successfully checked in! Emails sent but SMS not delivered due to third party error')
        return render(request, 'index.html')
    except Exception as e:
        print(e)
        context = {
            'value': "Sorry! Some error occured"
        }
        return render(request, '404.html', context=context)

# Visitor checkout


def checkout(request, id):
    try:
        visit_object = Visitor.objects.get(id=str(id))
        visit_object.Check_out = datetime.now()
        visit_object.save()
        host_object_ref = visit_object.host_id
        visitor_details = {
            'id': visit_object.id,
            'first_name': visit_object.first_name,
            'last_name': visit_object.last_name,
            'Email_ID': visit_object.Email_ID,
            'Phone_No': visit_object.Phone_No,
            'Check_in': visit_object.Check_in,
            'Check_out': visit_object.Check_out
        }
        host_details = {'id': host_object_ref.id,
                        'first_name': host_object_ref.first_name,
                        'last_name': host_object_ref.last_name,
                        'Email_ID': host_object_ref.Email_ID,
                        'Phone_No': host_object_ref.Phone_No
                        }
        visitorCheckoutNotification(host_details, visitor_details)
        return render(request, 'goodbye.html')
    except SMSNotSent as smserr:
        print(smserr)
        messages.error(request, 'Visitor successfully checked out! Emails sent but SMS not delivered due to third party error')
        return render(request, 'index.html')
