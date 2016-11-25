# encoding: utf-8

import json
import logging
import uuid

from django.shortcuts import render
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import DateField, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt

from smtplib import SMTPServerDisconnected

from .helpers import CustomJsonEncoder, Settings
from .models import User

logger = logging.getLogger(__name__)


class BaseView(View):
    """
    Базовый класс для View
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)

    def redirect(self, reverse_name, args=None, **kwargs):
        return HttpResponseRedirect(reverse(reverse_name, args=args), **kwargs)

    def redirect_to_url(self, url, **kwargs):
        return HttpResponseRedirect(url, **kwargs)

    def json_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(
            json.dumps(context, cls=CustomJsonEncoder), **response_kwargs)


class JSONMixin(object):
    def render_to_response(self, context, **httpresponse_kwargs):
        return self.get_json_response(
            self.convert_context_to_json(context),
            **httpresponse_kwargs
        )

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        """ This method serialises a Django form and
        returns JSON object with its fields and errors
        """
        forms = {}
        for form_name, form in context.items():
            form = context.get('form')
            to_json = {}
            options = context.get('options', {})
            to_json.update(options=options)
            to_json.update(success=context.get('success', False))
            fields = {}
            for field_name, field in list(form.fields.items()):
                if isinstance(field, DateField) \
                    and isinstance(form[field_name].value(), datetime.date):
                    fields[field_name] = \
                        str(form[field_name].value().strftime('%d.%m.%Y'))
                else:
                    fields[field_name] = \
                        form[field_name].value() \
                        and str(form[field_name].value()) \
                        or form[field_name].value()
            to_json.update(fields=fields)
            if form.errors:
                errors = {
                    'non_field_errors': form.non_field_errors(),
                }
                fields = {}
                for field_name, text in list(form.errors.items()):
                    fields[field_name] = text
                errors.update(fields=fields)
                to_json.update(errors=errors)
            forms.update({form_name: to_json})
        return json.dumps(forms)


class BaseViewNoLogin(BaseView):
    """
    Базовый класс для View без аутентификации
    """
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class BaseTemplateView(TemplateView, BaseView):
    """
    Базовый класс для View для работ с template
    """
    pass


class HomeView(BaseTemplateView):
    """Главная страница dashboard"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class LoginView(BaseTemplateView):
    """
    Вход пользователя в систему
    """
    template_name = 'core/login.html'

    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.redirect_to_url("/")
        if "next" in request.GET:
            next_url = request.GET['next']
        else:
            next_url = None
        return self.render_to_response({'regUrl': '/registration', 'next': next_url})

    def post(self, request, *args, **kwargs):
        post = request.POST

        username = post['username']
        password = post['password']
        user = None

        if "next" in request.POST:
            next_url = request.POST['next']
        else:
            next_url = None

        # if email (костылим):
        if '@' in username:
            users = User.objects.filter(email=username)
            for us in users:
                if check_password(password, us.password):
                    user = authenticate(
                        username=us.username,
                        password=password
                    )
                    break
        else:
            user = authenticate(
                username=username,
                password=password
            )

        if user is not None:
            if user.is_active:
                login(request, user)
                if next_url:
                    return self.redirect_to_url(next_url)
                else:
                    return self.redirect("core:home")
            else:
                if not user.email:
                    return self.render_to_response({
                        'error': 'Пользователь не имеет почты!'
                    })

                host = Settings.get_host(request)
                code = uuid.uuid4().hex
                message = '{0}{2}?uuid={1}'.format(host, code, reverse('core:activate_user'))

                user.verify_email_uuid = code
                user.save()

                send_mail('Подтверждение!', message, settings.EMAIL_HOST_USER,
                          [user.email], fail_silently=False)

                return self.render_to_response({
                    'error': 'Пользователь заблокирован! Проверьте свою почту!'
                })

        return self.render_to_response({
            'error': 'Неправильный логин или пароль!',
            'next': next_url
        })


class LogoutView(BaseView):
    """
    Выход пользователя
    """

    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return self.redirect('login')


class RegistrationView(BaseView):
    """
    Регистрация нового пользователя в системе
    """
    # у предка dispatch перекрыт login_required
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        post = request.POST

        host = Settings.get_host(request)
        code = uuid.uuid4().hex
        message = '{0}{2}?uuid={1}'.format(host, code, reverse('core:activate_user'))

        user_login = post.get('login', '')
        user_email = post.get('email', '')

        try:
            if len(user_login) == 0 or len(user_email) == 0:
                raise ValueError("Логин или пароль не могут быть пустыми")

            current_user = User.objects.filter(Q(username=user_login) | Q(email=user_email))

            if len(current_user) > 0:
                raise ValueError("Такой пользователь уже существует")
            user = User(
                username=user_login,
                email=user_email,
                is_active=False,
                is_staff=True,
                verify_email_uuid=code
            )
            user.set_password(post.get('password'))
            user.save()

            # тут сделать очередь на письма
            send_mail('Подтверждение регистрации!', message, settings.EMAIL_HOST_USER,
                      [user.email], fail_silently=False)

            return self.json_response(
                {'status': 'ok',
                 'message': 'Регистрация прошла успешно! На почту была отправлена инструкция по активации аккаунта.'})
        except ValueError as e:
            return self.json_response(
                {'status': 'error', 'message': e.message}
            )
        except SMTPServerDisconnected as e:
            logger.exception(e.message)
            return self.json_response(
                {'status': 'error', 'message': "Ошибка при отправке почты %s" % e.message}
            )
        except:
            logger.exception("Произошла системная ошибка")
            return self.json_response(
                {'status': 'error', 'message': 'Произошла системная ошибка. Мы уже работаем над ней'}
            )
