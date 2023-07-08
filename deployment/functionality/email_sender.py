# qcuulpzhomapryck

import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(receiver,html,filename=None,extension=None):
    creds = open('functionality/login_credentials.txt','r')
    credentials = creds.read().split()

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = credentials[0]
    receiver_email = receiver
    password = credentials[1]

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Medical Analysis"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    part = MIMEText(html, 'html')
    msg.attach(part)

    if filename != None and extension!=None:
        attachment = open(filename, "rb")
        filepath = filename + extension
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filepath)
        msg.attach(p)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email,msg.as_string())

if __name__ == "__main__":
    send_email('aansh.basu@gmail.com','b','/home/dragon/medical_project/Medical_Suite/deployment/uploads/file2','.jpg')