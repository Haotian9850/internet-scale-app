from django.core.mail import send_mail

def send(subject, msg, sender, recipient):
    send_mail(
        subject,
        msg,
        sender,
        [recipient],
        fail_silently=False
    )

def assemble_pwd_reset_link(authenticator, hostname, port, path):
    return "http://{}:{}/{}/{}".format(
        hostname,
        port,
        path,
        authenticator
    )