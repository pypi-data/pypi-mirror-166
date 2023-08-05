from __future__ import print_function
from __future__ import unicode_literals
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import http.client
import requests
from urllib.parse import quote
from urllib.parse import parse_qs
from urllib.parse import urlparse
import webbrowser
import json
import pyotp
from data_mig.utils.logging import bcolors

from data_mig.utils.exceptions import *

HTTP_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

"""
Portions of this class borrowed from CCI: 
https://github.com/SalesforceFoundation/CumulusCI/blob/master/cumulusci/oauth/salesforce.py

    Copyright (c) 2015, Salesforce.org
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Salesforce.org nor the names of
      its contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
    COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
    POSSIBILITY OF SUCH DAMAGE.

"""


class SalesforceOAuth2(object):

    def __init__(self, client_id, client_secret, callback_url, auth_site=None):
        if auth_site == None:
            auth_site = 'https://login.salesforce.com'
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        self.auth_site = auth_site

    def _request_token(self, request_data):
        url = self.auth_site + '/services/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        data.update(request_data)
        response = requests.post(url, headers=HTTP_HEADERS, data=data)
        if response.status_code >= http.client.BAD_REQUEST:
            message = '{}: {}'.format(response.status_code, response.content)
            raise RequestOauthTokenError(message, response)
        return response

    def get_authorize_url(self, scope, prompt=None):
        url = self.auth_site + '/services/oauth2/authorize'
        url += '?response_type=code'
        url += '&client_id={}'.format(self.client_id)
        url += '&redirect_uri={}'.format(self.callback_url)
        url += '&scope={}'.format(quote(scope))
        if prompt:
            url += '&prompt={}'.format(quote(prompt))
        return url

    def get_token(self, code):
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': self.callback_url,
            'code': code,
        }
        return self._request_token(data)

    def refresh_token(self, refresh_token):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        return self._request_token(data)

    def revoke_token(self, current_token):
        url = self.auth_site + '/services/oauth2/revoke'
        data = {'token': quote(current_token)}
        response = requests.post(url, headers=HTTP_HEADERS, data=data)
        response.raise_for_status()
        return response


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    parent = None

    def do_GET(self):
        args = parse_qs(urlparse(self.path).query, keep_blank_values=True)
        if 'error' in args:
            http_status = http.client.BAD_REQUEST
            http_body = 'error: {}\nerror description: {}'.format(
                args['error'], args['error_description'])
        else:
            http_status = http.client.OK
            http_body = """<html><body><h1>Authentication Succeeded</h1><p>You may now close this window and return to Arroyo.</p></body></html>"""
            code = args['code']
            self.parent.response = self.parent.oauth_api.get_token(code)
            try:
                self.parent._check_response(self.parent.response)
            except SalesforceOAuthError as e:
                http_status = self.parent.response.status_code
                http_body = str(e)
        self.send_response(http_status)
        self.end_headers()
        self.wfile.write(http_body.encode('ascii'))


class CaptureSalesforceOAuth(object):

    def __init__(self, client_id, client_secret, callback_url, auth_site, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        self.auth_site = auth_site or 'https://login.salesforce.com'
        self.httpd = None
        self.oauth_api = self._get_oauth_api()
        self.response = None
        self.scope = scope
        self.httpd_timeout = 300

    def __call__(self):
        url = self._get_redirect_url()
        self._launch_browser(url)
        self._create_httpd()
        print(
            'Spawning HTTP server at {} '.format(self.callback_url) +
            'with timeout of {} seconds.\n'.format(self.httpd.timeout) +
            'If you are unable to log in to Salesforce you can ' +
            'press ctrl+c to kill the server and return to the command line.'
        )
        self.httpd.handle_request()
        self._check_response(self.response)
        return self.response.json()

    def _check_response(self, response):
        if response.status_code and response.status_code == http.client.OK:
            return
        raise SalesforceOAuthError('status_code:{} content:{}'.format(
            response.get('status_code', 'unknown'), response.get('content', response)))

    def _create_httpd(self):
        url_parts = urlparse(self.callback_url)
        server_address = (url_parts.hostname, url_parts.port)
        OAuthCallbackHandler.parent = self
        self.httpd = HTTPServer(server_address, OAuthCallbackHandler)
        self.httpd.timeout = self.httpd_timeout

    def _get_oauth_api(self):
        return SalesforceOAuth2(
            self.client_id,
            self.client_secret,
            self.callback_url,
            self.auth_site,
        )

    def _get_redirect_url(self):
        url = self.oauth_api.get_authorize_url(self.scope, prompt='login')
        response = requests.get(url)
        self._check_response(response)
        return url

    def _launch_browser(self, url):
        print('Launching web browser for URL {}'.format(url))
        webbrowser.open(url, new=1)


class SalesforceAuth(object):

    def __init__(self, config):
        self._config = config
        self._instance_url = config.SALESFORCE_CONFIG['instance_url']
        self._client_id = config.CONNECTED_APP.get('client_id')
        self._secret = config.CONNECTED_APP.get('client_secret')
        self._callback_url = 'http://localhost:8080/callback'
        self._scope = 'refresh_token web full'
        self._refresh_token = config.SALESFORCE_CONFIG.get('refresh_token')
        self._token = config.SALESFORCE_CONFIG.get('access_token')
        self.capture = CaptureSalesforceOAuth(self._client_id, self._secret, self._callback_url, self._instance_url,
                                              self._scope)

    def capture_token(self):
        auth = self.capture()
        self._config.SALESFORCE_CONFIG['refresh_token'] = auth.get('refresh_token')
        self._config.SALESFORCE_CONFIG['access_token'] = auth.get('access_token')
        self._config.SALESFORCE_CONFIG['instance_url'] = auth.get('instance_url')

    def refresh_token(self):

        if self._refresh_token:
            try:
                resp = self.capture.oauth_api.refresh_token(self._refresh_token).content
                self._token = (json.loads(resp)).get('access_token')
                self._config.SALESFORCE_CONFIG['access_token'] = self._token
            except RequestOauthTokenError as e:
                resp = json.loads(e.response.content)
                if resp.get('error') == 'invalid_grant':
                    self.capture_token()
        else:
            self.capture_token()

        self._config.update_config()

    def reset_tokens(self):
        self._refresh_token = None

        try:
            del self._config.SALESFORCE_CONFIG['access_token']
        except KeyError:
            pass

        try:
            del self._config.SALESFORCE_CONFIG['refresh_token']
        except KeyError:
            pass

    def switch_orgs(self, sandbox=False):
        sandbox_or_login = 'test' if sandbox else 'login'
        endpoint = 'https://{}.salesforce.com'.format(sandbox_or_login)
        self._instance_url = endpoint
        self._config.SALESFORCE_CONFIG['instance_url'] = endpoint

        self.reset_tokens();
        self.capture = CaptureSalesforceOAuth(self._client_id, self._secret, self._callback_url, self._instance_url,
                                              self._scope)
        self.refresh_token()

    def get_token(self):
        return self._token or self.refresh_token()

    def open_sf_url(self, url='', relative_url=None):
        sc = self._config.SALESFORCE_CONFIG
        totp_secret = sc.get('totp_secret')
        if totp_secret:
            totp = pyotp.TOTP(totp_secret).now()
            print(f'{bcolors.OKGREEN}TOTP: {totp}{bcolors.ENDC}')

        token = self._token

        if relative_url:
            destination_url = urlparse(self._instance_url, relative_url)
        elif not url:
            destination_url = ''
        else:
            destination_url = quote(url)

        URL_TEMPLATE = '{instance_url}/secur/frontdoor.jsp?sid={access_token}&retURL={destination}'
        url = URL_TEMPLATE.format(instance_url=self._instance_url, access_token=token, destination=destination_url)
        webbrowser.open(url, new=1)

