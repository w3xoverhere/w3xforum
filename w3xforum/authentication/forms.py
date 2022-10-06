from django import forms
from .models import User
from .validators import user_exist


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя',min_length=4, max_length=20, validators=[user_exist],
                               error_messages={
                                   'min_length': 'Имя меньше 8 символов',
                                   'max_length': 'Имя больше 20 символов',
                               }
                               )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=10)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    avatar = forms.FileInput()
    description = forms.CharField(
        label=("О себе"),
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        help_text=("Информация о себе"),)

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