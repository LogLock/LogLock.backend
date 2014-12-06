from random import choice
''' 
Checks if the current login attempt is a security threat or not.
Performs the required action in each case
'''
def is_safe(form, mandrill):
    ip      = form.get('ip', None)
    geo     = form.get('geo', None)
    os      = form.get('os', None)
    browser = form.get('browser', None)
    # check against our database
    safety_status = choice(range(-1, 2))
    return safety_status, ip, geo, os, browser # send SMS, mail...


def send_mail(mandrill, to):
    mandrill.send_email(
        from_email='someone@yourdomain.com',
        subject='Blocked suspicious login attempt @twitter',
        to=[{'email': to}],
        text='''An attack has been detected and blocked (LND=>NY login with 5h difference).
            Authorize this access by [...]'''
    )


