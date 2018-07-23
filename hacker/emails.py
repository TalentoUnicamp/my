from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse


def notify_admitted(hacker):
    hack_name = settings.EVENT_NAME
    context = {
        'title': 'Informações importantes',
        'subtitle': 'Leia tudo!',
        'description': f'Avaliamos sua aplicação e queremos você no {hack_name}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.',
        'actionUrl': settings.ROOT_URL + reverse('profile:token_login', args={hacker.profile.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/action/text.txt', context)
    msg_html = render_to_string('project/email/action/html.html', context)

    send_mail(
        f'[{hack_name}] Aplicação aceita!',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def nag_admitted(hacker):
    hack_name = settings.EVENT_NAME
    context = {
        'title': '[Lembrete] Informações importantes',
        'subtitle': 'Leia tudo!',
        'description': f'Avaliamos sua aplicação e queremos você no {hack_name}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.',
        'actionUrl': settings.ROOT_URL + reverse('profile:token_login', args={hacker.profile.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/action/text.txt', context)
    msg_html = render_to_string('project/email/action/html.html', context)

    send_mail(
        f'[{hack_name}] Ação necessária!',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_waitlist(hacker):
    hack_name = settings.EVENT_NAME
    context = {
        'title': 'Foi por pouco!',
        'subtitle': 'Leia tudo!',
        'description': f'Sua aplicação para o {hack_name} foi aceita, mas infelizmente nós já atingimos o máximo de participantes.<br><b>Não perca as esperanças!</b> Alguém ainda pode desistir até o dia da confirmação de interesse e a vaga abrir para você.<br>Você receberá um <b>email</b> no instante que isso acontecer, então fique de olhos abertos!',
        'actionUrl': settings.ROOT_URL + reverse('profile:token_login', args={hacker.profile.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/action/text.txt', context)
    msg_html = render_to_string('project/email/action/html.html', context)

    send_mail(
        f'[{hack_name}] Fila de Espera',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_unwaitlist(hacker):
    hack_name = settings.EVENT_NAME
    context = {
        'title': 'Abriu uma vaga!',
        'subtitle': 'Leia tudo!',
        'description': f'Alguém desistiu e uma vaga foi aberta para você no {hack_name}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.<br> Para fazer isso, clique no botão abaixo:',
        'actionUrl': settings.ROOT_URL + reverse('profile:token_login', args={hacker.profile.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/action/text.txt', context)
    msg_html = render_to_string('project/email/action/html.html', context)

    send_mail(
        f'[{hack_name}] Abriu uma vaga!',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_decline(hacker):
    hack_name = settings.EVENT_NAME
    context = {
        'title': 'Sentimos muito',
        'subtitle': '',
        'description': f'Avaliamos sua aplicação e infelizmente decidimos que você não poderá fazer parte dessa edição do {hack_name}.<br>Esperamos ver você em edições futuras!',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.profile.user.email
    fr = settings.DEFAULT_FROM_EMAIL
    msg_plain = render_to_string('project/email/basic/text.txt', context)
    msg_html = render_to_string('project/email/basic/html.html', context)

    send_mail(
        f'[{hack_name}] Sobre sua aplicação',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )
