# -*- coding: utf-8 -*-

import asyncio

from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.asgi import ASGIRequest
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.decorators import sync_and_async_middleware


@sync_and_async_middleware
class WebsocketOhjain:
  '''
  Ohjain, joka asettaa pyynnölle URI-määritteen `websocket` siten,
  että siihen tehdyt pyynnöt ohjataan ajossa olevaan ASGI-käsittelijään.

  Mikäli HTTP-yhteys on salattu (HTTPS),
  käytetään salattua Websocket-yhteyttä (WSS).

  Mikäli pyyntö ei ole ASGI-pohjainen, ei `websocket`-yhteys ole
  käytettävissä eikä em. määritettä aseteta.
  '''
  def __init__(self, get_response):
    self.get_response = get_response
    # Asetetaan tämä ohjain näyttämään ulospäin asynkroniselta silloin,
    # kun signaalitien seuraava ohjain on sellainen.
    if asyncio.iscoroutinefunction(self.get_response):
      self._is_coroutine = asyncio.coroutines._is_coroutine

  def __call__(self, request):
    # Huomaa, että funktiokutsu palauttaa joko synkronisen tuloksen
    # tai asynkronisen alirutiinin sen mukaan, mitä signaalitien
    # seuraava ohjain palauttaa.
    if isinstance(request, ASGIRequest):
      request.websocket = (
        f'{"wss" if request.is_secure() else "ws"}://{request.get_host()}'
      )
    return self.get_response(request)
    # def __call__

  # class WebsocketOhjain


class OhitaPaluusanoma:
  ''' Saateluokka, joka ohittaa paluusanoman käsittelyn. '''
  def process_response(self, request, response):
    return response


class CsrfOhjain(OhitaPaluusanoma, CsrfViewMiddleware):
  def process_view(self, request, callback, callback_args, callback_kwargs):
    '''
    Ohitetaan tavanomainen CSRF-tarkistus POST-datasta.
    '''
  # class CsrfOhjain


class IstuntoOhjain(OhitaPaluusanoma, SessionMiddleware):
  pass


# Muunnostaulu Websocket-pyyntöihin sovellettavista
# Middleware-ohjaimista.
# Muiden kuin tässä mainittujen ohjaimien lataus ohitetaan.
WEBSOCKET_MIDDLEWARE = {
  # Ohitetaan.
  'corsheaders.middleware.CorsMiddleware': False,
  'debug_toolbar.middleware.DebugToolbarMiddleware': False,
  'django.middleware.gzip.GZipMiddleware': False,
  'django.middleware.security.SecurityMiddleware' : False,
  'django.middleware.common.CommonMiddleware': False,
  'django.middleware.clickjacking.XFrameOptionsMiddleware': False,
  'django_hosts.middleware.HostsResponseMiddleware': False,

  # Suoritetaan.
  'django_hosts.middleware.HostsRequestMiddleware': True,
  'django.middleware.csrf.CsrfViewMiddleware': 'pistoke.ohjain.CsrfOhjain',
  'django.contrib.sessions.middleware.SessionMiddleware': \
    'pistoke.ohjain.IstuntoOhjain',
  'django.contrib.auth.middleware.AuthenticationMiddleware': True,
  'django.contrib.messages.middleware.MessageMiddleware': True,
  'impersonate.middleware.ImpersonateMiddleware': True,
  'silk.middleware.SilkyMiddleware': True,
  'pistoke.ohjain.WebsocketOhjain': True,
}
