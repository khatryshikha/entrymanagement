import json
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.mail import send_mail
from .exceptions import SMSNotSent

def sendMail(receiver, subject, message):
    from_email = settings.EMAIL_HOST_USER
    print(receiver, message)
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[receiver])
    return

def sendSMSTL(receiver, message):
    apikey = settings.TEXTLIVE_APIKEY
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': receiver, 'message' : message, 'sender': ''})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return json.loads(fr.decode('utf-8'))

def visitorCheckinNotification(hostDetails, visitorDetails):
    # Email to host
    message =  'Dear ' + hostDetails['first_name'] + ' ' + hostDetails['last_name'] + ',\n\nGuest has come to visit you.'+"\n\nName - " + visitorDetails['first_name'] + ' ' + visitorDetails['last_name'] + '\nEmail - ' + str(
        visitorDetails['Email_ID']) + '\nPhone - ' + str(visitorDetails['Phone_No']) 

    sendMail(
        hostDetails['Email_ID'],
        "Welcome your arrived Guest | Guest Details",
        message)

    # Email to visitor
    message_visitor = 'Hello '+visitorDetails['first_name'] + ' ' + visitorDetails['last_name'] +',\nA warm welcome to our company! Hope you will have a great time. We request our visitor to complete the enquiry on the provides below on Checkout. http://127.0.0.1:8000/visitor_checkout/' + \
        str(visitorDetails['id'])
    sendMail(visitorDetails['Email_ID'],
     "Successfully registered", message_visitor)

    ## SMS to host
    ret = sendSMSTL(hostDetails['Phone_No'], message)
    if ret['status'].lower() == 'failure':
        raise SMSNotSent(str(ret['errors']))

    ##  SMS to visitor
    ret_visitor = sendSMSTL(visitorDetails['Phone_No'], message_visitor)
    if ret_visitor['status'].lower() == 'failure':
        raise SMSNotSent(str(ret_visitor['errors']))
    return




def visitorCheckoutNotification(hostDetails, visitorDetails):
    message = 'Dear ' + visitorDetails['first_name'] + ' ' + visitorDetails['last_name'] + ',\n\nThank for visiting us. Hope you had a great time here.\nFollowing are your visiting details:\n' + '\nName : ' + visitorDetails['first_name'] + ' ' + visitorDetails['last_name'] + '\nPhone : ' + str(
        visitorDetails['Phone_No']) + '\nCheck-in time : ' + str(visitorDetails['Check_in']) + '\nCheck-out time : ' + str(visitorDetails['Check_out']) + '\nHost name : ' + str(hostDetails['first_name']) + ' ' + hostDetails['last_name'] + '\nAddres visited : Innovaccer Office, Noida-201309'
    sendMail(
        visitorDetails['Email_ID'],
        "Thank for Visiting us | Visting Details",
        message)
    return