from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UsernameField

from .models import User
from .validators import user_exist


class UserAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,'placeholder': 'Имя пользователя',
                                                           'style': 'border-radius: 5px;'
                                                                    'border-width: thin;'
                                                                    'padding: 5px;'}))
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          'placeholder': 'Имя пользователя',
                                          'style': 'border-radius:5px;'
                                                   'border-width: thin;'
                                                   'padding: 5px;'})
    )



class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', min_length=4, max_length=20, validators=[user_exist],
                               error_messages={
                                   'min_length': 'Имя меньше 8 символов',
                                   'max_length': 'Имя больше 20 символов',
                               },
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'style': 'border-radius: 5px;'
                                                                                                         'border-width: thin;'
                                                                                                         'padding: 5px;'})
                               )
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'style': 'border-radius: 5px;'
                                                                                                   'border-width: thin;'
                                                                                                   'padding: 5px;'}),
                               min_length=10)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль',
                                                                  'style': 'border-radius: 5px;'
                                                                           'border-width: thin;'
                                                                           'padding: 5px;'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Почта', 'style': 'border-radius: 5px;'
                                                                                             'border-width: thin;'
                                                                                             'padding: 5px;'}))
    avatar = forms.FileInput()
    description = forms.CharField(
        label=("О себе"),
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Текст', 'style': 'border-radius: 5px;'
                                                                                             'border-width: thin;'
                                                                                             'padding: 5px;'}),
        help_text=("Информация о себе"))

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class CodeForm(forms.Form):
    code = forms.CharField(max_length=5)


class PasswordRecoveryMailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Почта',
                                                            'style': 'border-radius: 5px;'
                                                                     'border-width: thin;'
                                                                     'padding: 5px;'}))

class PasswordRecoveryPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                  'style': 'border-radius: 5px;'
                                                                           'border-width: thin;'
                                                                           'padding: 5px;'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль',
                                                                  'style': 'border-radius: 5px;'
                                                                           'border-width: thin;'
                                                                           'padding: 5px;'}))
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']