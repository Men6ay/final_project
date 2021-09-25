from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.utils.encoding import force_text
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from rest_framework import viewsets
from rest_framework.response import Response

from apps.posts.models import PostImage, Post
from apps.users.forms import UserCreationForm, UserLoginForm, UserChangeForm
from apps.users.serializers import UserSerializer
from apps.users.models import User
from apps.users.tokens import account_activation_token


class UserAuthView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'user_create.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        user_id = user.id
        if user.is_anonymous:
            signup = UserCreationForm(request.POST)
            if signup.is_valid():
                user = signup.save(commit=False)
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
                to_email = signup.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Подьвердите имейл.')
        else:
            signup = UserCreationForm()
        return render(request, 'user_create.html',
                      {'signup': signup, 'user_id': user_id})


class UserLoginView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'form': UserLoginForm()
        }
        return render(request, 'user_login.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            user = authenticate(request, username=username, password=password)
            if user.is_authenticated:
                login(request, user)
                return redirect(reverse_lazy('posts:post_list'))
            else:
                return redirect(reverse_lazy('users:user_login'))
        return render(request, 'user_login.html')


class UserProfileTemplateView(TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileTemplateView, self).get_context_data()
        images = PostImage.objects.all()
        posts = Post.objects.filter(
            post_images__in=images, user_id=self.request.user.id
        ).distinct()
        images = PostImage.objects.filter(post__in=posts)
        objects = zip(posts, images)
        context['user'] = self.request.user
        context['objects'] = objects
        return context


class UserChangeView(UpdateView):
    model = get_user_model()
    fields = ('username', 'email', 'age', 'gender', )
    template_name = 'user_change.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('users:user_profile')

    def get_context_data(self, **kwargs):
        context = super(UserChangeView, self).get_context_data()
        context['user'] = self.request.user
        return context


class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Account activated successfully')
    else:
        return HttpResponse('The link is inactive')
