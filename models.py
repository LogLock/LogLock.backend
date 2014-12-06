''' 
Checks if the current login attempt is a security threat or not.
Performs the required action in each case
'''
def is_safe(form_data, mandrill):
    return True # send SMS, mail...


def send_mail(mandrill, to):
    mandrill.send_email(
        from_email='someone@yourdomain.com',
        subject='Blocked suspicious login attempt @twitter',
        to=[{'email': to}],
        text='''An attack has been detected and blocked (LND=>NY login with 5h difference).
            Authorize this access by [...]'''
    )


