from django import forms
from django.contrib.auth import get_user_model

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'gender', 'age')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(u" Почта '%s' уже существует." % email)
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u" Имя пользователя '%s' уже существует." % username)
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            return username
        except User.DoesNotExist:
            pass
        raise forms.ValidationError('This username or password does not exist.')

    def clean_password(self):
        password = self.cleaned_data["password"]
        try:
            User.objects.get(password=password)
        except User.DoesNotExist:
            return password
        raise forms.ValidationError('Username or password does not exist.')


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'age', )
