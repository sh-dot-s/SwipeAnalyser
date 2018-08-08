from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.middleware.csrf import get_token

def sendSMTPMail(request, selected_objects):
    try:
        subject, from_email, to = 'Swipe Clearance Mail', 'Imaging.Support@mrcooper.com', ['SankarsettyLokesh.SaiSriHarsha@mrcooper.com']
        csrf_token = get_token(request)
        c = {'csrfMiddlewareToken': csrf_token}
        html_content = get_template('email.html')
        html_content = html_content.render(c)
        text_content = strip_tags(html_content)
        with open('./swipe/core/templates/mail.txt','r') as fileRead:
            lines = fileRead.read()
        stringToAdd, i = "", 1
        for empids in selected_objects:
            tempLines = lines
            stringToAdd += tempLines.format(i=i,id=empids.employee_id,name=empids.employee_name,date=empids.attendence_date,time=empids.work_time)
            i += 1
        # print((stringToAdd))
        html_content = html_content.replace("tablebody",stringToAdd)
        # print(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Mail sent succesfully")
    except Exception as e:
        print(e)
        print("Failed")
    return
def sendCompleteMail(Files, user):
    try:
        print(user)
        subject, from_email, to = '(SPART) File/s Processing Complete', 'SankarsettyLokesh.SaiSriHarsha@mrcooper.com', user
        body = ''
        for files in Files:
            body += '<li>%s</li>'%files
        html_content = '''
            <html>
                <h3>Processing of the following files is complete</h3>
                <ul>%s</ul>
                <a href="swipedev.mrcooper.it">Click Here to go to SPART</button>
            </html>
        '''%body
        text_content = "File processing complete notification"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Notification sent succesfully")
    except Exception as e:
        print(e)
        print("Failed")
    return

def sendFailedMail(Files, user):
    try:
        subject, from_email, to = '(SPART) File/s Processing Stopped', 'SankarsettyLokesh.SaiSriHarsha@mrcooper.com', user
        body = ''
        for files in Files:
            body += '<li>%s</li>'%files
        html_content = '''
            <html>
                <h3>Processing has stopped due to incomplete Master data, the following ID's are missing, please update and reprocess</h3>
                <ul>%s</ul>
                <a href="swipedev.mrcooper.it">Click Here to go to SPART</button>
            </html>
        '''%body
        text_content = "File processing Stopped"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Failure Notification sent succesfully")
    except Exception as e:
        print(e)
        print("Failed")
    return
