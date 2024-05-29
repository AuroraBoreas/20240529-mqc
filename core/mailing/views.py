from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail

import after_response

from .models import MailingGroup

@after_response.enable
def send_email_to_mailing_group(subject: str, message: str, from_email: str, group_name: str) -> None:
    try:
        mailing_group = MailingGroup.objects.get(name=group_name)
        members = mailing_group.members.all()
        recipient_emails = [member.email for member in members]
        send_mail(
            subject,
            message,
            from_email,
            recipient_emails,
            fail_silently=False,
        )
    except MailingGroup.DoesNotExist:
        msg = 'there is no records of {0}'.format(group_name)
        raise ValueError(msg)

@transaction.non_atomic_requests
@login_required(redirect_field_name='mailing:send')
def send_email_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = settings.EMAIL_HOST_USER
        # recipient_list = ['recipient@example.com']
        # send_mail(subject, message, from_email, recipient_list)
        send_email_to_mailing_group.after_response(subject, message, from_email, 'Notification')
        messages.success(request, 'Email sent successfully')
        return render(request, 'core/mailing/sent.html')
    return render(request, 'core/mailing/send.html')