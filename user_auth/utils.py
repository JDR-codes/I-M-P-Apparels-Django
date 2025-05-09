from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def send_verification_email(user, request, subject, message, url_name):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = request.build_absolute_uri(reverse(url_name, kwargs={'uidb64': uid, 'token': token}))
    
    subject = subject
    message = f'{message}{link}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
