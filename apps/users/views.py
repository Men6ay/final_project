from apps.posts.permissions import OwnerPermission
from rest_framework import viewsets,permissions,authentication
from apps.users.serializers import UserSerializer
from apps.users.models import User
from django.shortcuts import redirect,render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import login
from rest_framework.response import Response
from django.utils.encoding import force_text
from django.http import HttpResponse
from apps.users.tokens import account_activation_token


class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Email verification'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = serializer.data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            data['response'] = "Successfully created a new user. Please check your email and verify your account."
            data['email'] = user.email
            data['token'] = user.token
        else:
            data = serializer.errors
        return Response(data)

def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('https://www.youtube.com')
    else:
        return HttpResponse('The link is inactive')
    
