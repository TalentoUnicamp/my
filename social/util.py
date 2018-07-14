from urllib.parse import unquote
from django.contrib import messages


def login_canceled(request):

    # If the user has canceled the login process, or something else happened, do nothing and display error message
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu :( Se isso se repetir, fale conosco!')

    return request


def decode_state_data(state):
    if not state:
        return {}
    parts = state.split(',')
    data = {}
    for part in parts:
        p = part.split('=')
        data[p[0]] = unquote(p[1])
    return data
