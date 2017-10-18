from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django.shortcuts import render
from django.template import Context

def sendSMTPMail(selected_objects):
    try:
        subject, from_email, to = 'Swipe Clearance Mail', 'SankarsettyLokesh.SaiSriHarsha@mrcooper.com', 'SankarsettyLokesh.SaiSriHarsha@mrcooper.com'
        text_content = 'This is an important message.'
        params = ({'table': selected_objects})
        # html_content = get_template('email.html')
        html_content = render_to_string('email.html')
        html_content = (str(html_content))
        # print((html_content))
        stringToAdd, i = "", 1
        # html_content = html_content.render(params)
        for empids in selected_objects:
            stringToAdd += '<tr>\n\t<th scope="row">{}</th>\n\t<td>{}</td>\n\t<td>{}</td>\n\t<td><input type="text" class="form-control" id="clarifyComments" placeholder="Remarks.."></td>\n</tr>\n'.format(i,empids.employee_name,empids.attendence_date)
            i += 1
        # print((stringToAdd))
        html_content = html_content.replace("tablebody",stringToAdd)
        print(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Mail sent succesfully")
    except Exception as e:
        print(e)
        print("Failed")
    return


# from django.template import Context

# plaintext = get_template('email.txt')
# htmly     = get_template('email.html')
#
# # d = Context({ 'username': username })
#
# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# # text_content = plaintext.render(d)
# html_content = htmly.render(d)
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()
