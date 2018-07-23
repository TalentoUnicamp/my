from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse


def verify_email(profile):
    hack_name = settings.EVENT_NAME
    context = {
        'title': 'Verificação de Email',
        'subtitle': '',
        'description': 'Você está recebendo essa mensagem pois alterou seu email.<br><br>Use o botão abaixo para verificar seu email:',
        'actionUrl': settings.ROOT_URL + reverse('profile:verify_email', args={profile.verification_code}),
        'actionName': 'Verificar Email',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/action/text.txt', context)
    msg_html = render_to_string('project/email/action/html.html', context)
    send_mail(
        '[{}] Verificar email'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def recover_token_email(profile):
    hack_name = settings.EVENT_NAME
    context = {
        'title': 'Recuperar token',
        'subtitle': '',
        'description': f'Você está recebendo essa mensagem pois alguém pediu para que o seu token fosse recuperado.<br><br>Seu token atual é <b>{profile.token}</b> e você pode logar em sua conta usando o botão abaixo',
        'actionUrl': settings.ROOT_URL + reverse('profile:token_login', args={profile.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/action/text.txt', context)
    msg_html = render_to_string('project/email/action/html.html', context)

    send_mail(
        '[{}] Recuperar Token'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )
