import doc_manager.settings as settings
import smtplib
from email.message import EmailMessage
from django.shortcuts import render, redirect
import sys
from django.http import HttpResponse
from twilio.rest import Client

def sendmail(sender, receiver, subject, messagebody, note, attachments=None):
    contacts = [receiver]
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = ', '.join(contacts)
    msg.set_content(messagebody)
    content = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Title</title>
        </head>
        <body>
        <h2>"""+note+"""</h2> <p></p>"""+"""
        <a href=\"http://"""+ messagebody+ "\""+ """>""" + messagebody + """</a>
        </body> 
        </html>"""
    msg.add_alternative(content,subtype='html')

    port = 465
    with smtplib.SMTP_SSL(settings.EMAIL_HOST,port) as smtp:
        # smtp.ehlo()
        # smtp.starttls()
        # smtp.ehlo()
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)

def sharelinkbyemail(request, user1, email, link, note=""):
    subject = "this link was shared by a user:" + user1.username
    body = link

    sender = user1.email

    try:
        sendmail(settings.EMAIL_HOST_USER, email, subject, body, note)
    except:
        e = sys.exc_info()[0]
        return render(request, 'users/error.html', {'errorstring': e})

    infostring = "email successfully sent"
    return render(request, 'users/info.html', {'infostring': infostring})


def sharelinkbysms(request, user1, recieverphone, link,note=""):
    subject = "link from  user:"+ user1.username
    message = subject + " " + note+"  " + link

    callerphone = user1.profile.phone

    sid = ""
    try:
        sid = sendsms(callerphone,recieverphone,  message)
    except:
        e = sys.exc_info()[0]


        return render(request, 'users/error.html', {'errorstring': e+str(sid)})

    infostring = "sms successfully sent:info("+str(sid)+")"
    return render(request, 'users/info.html', {'infostring': infostring})



def sendsms(callerphone,receiverphone,  message):

    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)


    message = client.messages.create(
        body= message,
        from_="+16503824369",
        to=receiverphone
    )

    return message.sid