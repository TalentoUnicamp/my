import facebook
from django.conf import settings
from django.shortcuts import reverse
from urllib.parse import urlencode, quote
from django.contrib.auth import login
from django.contrib import messages
from ..models import Social
import json


def get_credentials():
    app_id = settings.FACEBOOK_KEY
    app_secret = settings.FACEBOOK_SECRET
    return (app_id, app_secret)


def get_graph():
    """Get App Graph Object.

    returns a graph object containing an app token from the registered facebook app
    """
    app_id, app_secret = get_credentials()
    graph = facebook.GraphAPI(version='2.7')
    graph.access_token = graph.get_app_access_token(app_id, app_secret)
    return graph


def canv_url(request):
    """Return Canvas URL.

    Generates the canvas_url used by facebook to redirect after auth
    """
    # Check whether the last call was secure and use its protocol
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('social:login_response', kwargs={'provider': 'facebook'})
    else:
        return 'https://' + request.get_host() + reverse('social:login_response', kwargs={'provider': 'facebook'})


def auth_url(request):
    """Auth URL.

    Returns the facebook auth url using the current app's domain
    """
    canvas_url = canv_url(request)
    app_id, app_secret = get_credentials()

    # Permissions set by user. Default is none
    perms = settings.FACEBOOK_PERMISSIONS

    url = "https://www.facebook.com/dialog/oauth?"

    # Payload
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url}

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
        kvps['scope'] = ",".join(perms)

    # Return the url
    return url + urlencode(kvps)


def debug_token(token):
    """Debug Token.

    Returns debug string from token
    """
    app_id, app_secret = get_credentials()
    return get_graph().debug_access_token(token, app_id, app_secret)


def login_successful(code, request):
    """Login Successful.

    Process successful login by creating or updating an user using Facebook's response
    """
    canvas_url = canv_url(request)
    graph = get_graph()
    app_id, app_secret = get_credentials()

    # Get token info from user
    try:
        token_info = graph.get_access_token_from_code(code, canvas_url, app_id, app_secret)
    except facebook.GraphAPIError:
        # For some reason, the auth code has already been used, redirect to login again
        return 'auth code used'

    # Extract token from token info
    access_token = token_info['access_token']

    # Debug the token, as per documentation
    debug = debug_token(access_token)['data']

    # Get the user's scope ID from debug data
    social_id = debug['user_id']
    expires = debug.get('expires_at') - debug.get('issued_at')
    if debug.get('expires_at') == 0:
        expires = 99999999
    scopes = debug.get('scopes', [])

    # Get some user info like name and url
    extra_data = graph.get_object(str(social_id) + '/?fields=first_name,last_name,email')
    first_name = extra_data['first_name']
    last_name = extra_data['last_name']
    email = extra_data.get('email', None)

    # User if not anonymous
    user = request.user if request.user.is_authenticated else None

    kwargs = {
        'provider': 'facebook',
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
        messages.add_message(request, messages.SUCCESS, 'Facebook vinculado!')

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
    return reverse('social:login', kwargs={'provider': 'facebook'}) + '?' + urlencode(state)
