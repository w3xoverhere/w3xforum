from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from .forms import UserRegistrationForm, CodeForm, UserAuthenticationForm, PasswordRecoveryMailForm, PasswordRecoveryPasswordForm
from django.utils.html import strip_tags
from .tokens import generate_code
from .models import User
from django.core.signing import dumps, loads


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'auth/user_login.html'
    success_url = '/'

def user_registration(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.clean_password2()
            user.set_password(password)
            user.save()
            user_name = user.username
            token = dumps(user_name)
            response = HttpResponseRedirect(reverse('auth:activation', kwargs={ 'user_name': user_name}))
            response.set_cookie(key="token", value=token, max_age=600)
            return response
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/user_reg.html', context={'form': form})


def send_email_with_code(request, user):
    code = generate_code()
    dump_code = dumps(code)
    request.session['cde'] = dump_code
    subject = 'Активация аккаунта'
    html_message = render_to_string('auth/mail_message.html',
                                    context={'user': user.username, 'code': code})
    plain_message = strip_tags(html_message)
    send_mail(subject=subject, message=plain_message, from_email=None,
              recipient_list=[user.email], html_message=html_message)
def user_activation(request, user_name):
    try:
        token_cookie = request.COOKIES['token']
    except KeyError:
        return HttpResponseForbidden()

    token = loads(token_cookie)

    if token != user_name or request.user.is_authenticated:
        return HttpResponseForbidden()

    user = User.objects.get(username=user_name)

    if request.method == 'POST':
        form = CodeForm(request.POST)

        if form.is_valid():
            code_from_form = form.cleaned_data['code']
            code = loads(request.session['cde'])
            if code_from_form == code:
                user.is_active = True
                user.save()
                return render(request, 'auth/user_reg_complete.html')
            else:
                raise ValidationError("Код из письма не верен!")
    else:
        send_email_with_code(request, user=user)
        form = CodeForm()
    context = {'form': form}
    return render(request, 'auth/user_reg_activation.html', context=context)


def password_recovery(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method=='POST':
        form = PasswordRecoveryMailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except:
                raise ValidationError('Ошибка восстановления')
            cur_session = dumps(user.username)
            response = HttpResponseRedirect(
                reverse('auth:pswrdrec_code', kwargs={'user_name': user.username})
            )
            response.set_cookie('cur_session', cur_session, max_age=1200)
            return response
    else:
        form = PasswordRecoveryMailForm()
    return render(request, 'auth/user_pswrd_recovery_mail.html', context={'form': form})

def password_recovery_code(request, user_name):
    try:
        cur_session = request.COOKIES['cur_session']
    except:
        return HttpResponseForbidden()
    cur_session = loads(cur_session)
    if cur_session != user_name:
        return HttpResponseForbidden()
    user = User.objects.get(username=user_name)
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code_from_form = form.cleaned_data['code']
            code = loads(request.session['cde'])
            if code_from_form == code:
                response = HttpResponseRedirect(reverse('auth:pswrdrec_complete', kwargs={'user_name': user.username}))
                return response
    else:
        send_email_with_code(request, user=user)
        form = CodeForm()
    return render(request, 'auth/user_pswrd_recovery_code.html', context={'form': form})

def password_recovery_complete(request, user_name):
    try:
        cur_session = request.COOKIES['cur_session']
    except:
        return HttpResponseForbidden()
    cur_session = loads(cur_session)
    if cur_session != user_name:
        return HttpResponseForbidden()
    user = User.objects.get(username=user_name)
    if request.method=='POST':
        form = PasswordRecoveryPasswordForm(request.POST)
        if form.is_valid():
            password = form.clean_password2()
            user.set_password(password)
            user.save()
            response = HttpResponseRedirect('/')
            response.delete_cookie('cur_session')
            return response
        else:
            raise ValidationError('Ошибка проверки формы')
    else:
        form = PasswordRecoveryPasswordForm()
    return render(request, 'auth/user_pswrd_recovery_complete.html', context={'form': form})
