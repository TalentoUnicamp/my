from django.conf import settings
from django.shortcuts import reverse
from urllib.parse import urlencode, quote
from django.contrib.auth import login
from django.contrib import messages
from ..models import Social
import requests
import json


def get_credentials():
    app_id = settings.GOOGLE_KEY
    app_secret = settings.GOOGLE_SECRET
    return (app_id, app_secret)


def canv_url(request):
    """Return Canvas URL.

    Generates the canvas_url used by facebook to redirect after auth
    """
    # Check whether the last call was secure and use its protocol
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('social:login_response', kwargs={'provider': 'google'})
    else:
        return 'http://' + request.get_host() + reverse('social:login_response', kwargs={'provider': 'google'})


def auth_url(request):
    """Auth URL.

    Returns the facebook auth url using the current app's domain
    """
    canvas_url = canv_url(request)
    app_id, app_secret = get_credentials()

    # Permissions set by user. Default is none
    perms = settings.GOOGLE_PERMISSIONS

    url = "https://accounts.google.com/o/oauth2/v2/auth?"

    # Payload
    kvps = {
        'access_type': 'online',
        'client_id': app_id,
        'redirect_uri': canvas_url,
        'include_granted_scopes': 'true',
        'response_type': 'code'
    }

    # Add 'next' as state if provided
    next_param = f"next_url={quote(request.GET.get('next', ''))}"
    # Add 'redirected' as state if provided
    redirected_param = f"redirected={request.GET.get('redirected', '')}"
    if request.GET.get('next', False):
        kvps['state'] = next_param
        redirected_param = f',{redirected_param}'
    if request.GET.get('redirected', False):
        kvps['state'] = kvps.get('state', '') + redirected_param

    # Format permissions if needed
    if perms:
        kvps['scope'] = " ".join(perms)

    # Return the url
    return url + urlencode(kvps)


def get_access_token_from_code(code, redirect_uri):
    app_id, app_secret = get_credentials()
    url = 'https://www.googleapis.com/oauth2/v4/token'
    payload = {
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, headers={'Accept': 'application/json'}, data=payload)
    response.raise_for_status()
    return response.json()


def debug_token(token):
    url = 'https://www.googleapis.com/userinfo/v2/me'
    response = requests.get(url, headers={'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(token)})
    return response.json()


def login_successful(code, request):
    """Login Successful.

    Process successful login by creating or updating an user using Facebook's response
    """
    canvas_url = canv_url(request)
    app_id, app_secret = get_credentials()

    # Get token info from user
    try:
        token_info = get_access_token_from_code(code, canvas_url)
    except requests.exceptions.HTTPError:
        # For some reason, the auth code has already been used, redirect to login again
        return 'auth code used'

    try:
        # Extract token from token info
        access_token = token_info['access_token']
    except KeyError:
        return 'token missing'

    # Debug the token, as per documentation
    debug = debug_token(access_token)

    # Get the user's scope ID from debug data
    social_id = debug['id']
    # Github tokens dont expire
    expires = token_info['expires_in']
    scopes = token_info.get('scope', "profile email") or "profile email"
    scopes = scopes.split(' ')

    # Get some user info like name and url
    names = debug.get('name', ' ').split(' ')
    first_name = names[0]
    last_name = ' '.join(names[1:]) if len(names) > 1 else ''
    email = debug.get('email', None)

    # User if not anonymous
    user = request.user if request.user.is_authenticated else None

    kwargs = {
        'provider': 'google',
        'user': user,
        'request': request,
        'social_id': social_id,
        'access_token': access_token,
        'expires': expires,
        'first_name': first_name,
        'last_name': last_name,
        'scopes': json.dumps(scopes),
        'email': email
    }
    new, u_created, s_created, request = Social.create_or_update(**kwargs)

    if not u_created and s_created:
        messages.add_message(request, messages.SUCCESS, 'Google vinculado!')

    if new is None:
        return request

    # Try to login the user
    if new.profile.user.is_active:
        login(request, new.profile.user)
    else:
        messages.add_message(request, messages.ERROR, 'Essa conta foi desativada!')

    return request


def code_already_used_url(next_url, redirected):
    state = {}
    if next_url:
        state['next'] = next_url
    state['redirected'] = int(redirected) + 1 if redirected else 0
    return reverse('social:login', kwargs={'provider': 'google'}) + '?' + urlencode(state)
