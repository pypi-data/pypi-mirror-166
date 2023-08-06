import jwt
import sys
import os
import logging
import requests
from http.client import responses
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from . import settings
from .. import __version__

logging.getLogger("azure.identity").setLevel(logging.ERROR)

class PurviewClient():
    def __init__(self):
        self.access_token = None
        self.account_name = None

    def set_account(self, app):
        if app == "management":
            self.account_name = None
        else:
            self.account_name = settings.PURVIEW_NAME if settings.PURVIEW_NAME != None else os.environ.get("PURVIEW_NAME")
            if self.account_name is None:
                print("""[ERROR] Environment variable PURVIEW_NAME is missing.

Please configure the PURVIEW_NAME environment variable. Setting environment variables can vary by environment, see examples below.
\tWindows (Command Prompt):\tset PURVIEW_NAME=value
\tmacOS (Terminal):\t\texport PURVIEW_NAME=value
\tPython:\t\t\t\tos.environ["PURVIEW_NAME"] = "value"
\tPowerShell:\t\t\t$env:PURVIEW_NAME = "value"
\tJupyter Notebook:\t\t%env PURVIEW_NAME=value

Alternatively, an Azure Purview account name can be provided by appending --purviewName=<val> at the end of your command.
""")
                sys.exit()

    def set_token(self, app):
        credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

        if app == "management":
            resource = "https://management.azure.com/.default"
        else:
            resource = "https://purview.azure.net/.default"

        try:
            token = credential.get_token(f'{resource}')
        except ClientAuthenticationError as e:
            print(e)
            print("For more information, check out: https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python")
            sys.exit()
        self.access_token = token.token

    def get_token(self):
        return self.access_token

    def http_get(self, app, method, endpoint, params, payload, files, headers):
        if app == 'management':
            uri = f"https://management.azure.com{endpoint}"
        elif app == 'catalog':
            uri = f"https://{self.account_name}.purview.azure.com/catalog{endpoint}"
        elif app == 'scan':
            uri = f"https://{self.account_name}.purview.azure.com/scan{endpoint}"
        elif app == 'account':
            uri = f"https://{self.account_name}.purview.azure.com/account{endpoint}"
        elif app == 'policystore':
            uri = f"https://{self.account_name}.purview.azure.com/policystore{endpoint}"
        elif app == 'share':
            uri = f"https://{self.account_name}.purview.azure.com/share{endpoint}"
        elif app == 'mapanddiscover':
            uri = f"https://{self.account_name}.purview.azure.com/mapanddiscover{endpoint}"
        elif app == 'guardian':
            uri = f"https://{self.account_name}.{app}.purview.azure.com{endpoint}"
        else:
            uri = f"https://{self.account_name}.{app}.purview.azure.com{endpoint}"

        auth = {"Authorization": "Bearer {0}".format(self.access_token)}
        useragent = {"User-Agent": "purviewcli/{0} {1}".format(__version__, requests.utils.default_headers().get("User-Agent"))}
        headers = dict(**headers, **auth, **useragent)

        try:
            response = requests.request(method, uri, params=params, json=payload, files=files, headers=headers)
            # DEBUG
            # print(f"Method:\t\t{method}")
            # print(f"Body:\t\t{payload}")
            # print(f"Headers:\t\t{headers}")
            # print(f"Endpoint:\t{response.url}")
        except requests.exceptions.HTTPError as errh:
            print ("[HTTP ERROR]",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("[CONNECTION ERROR]",errc)
            sys.exit()
        except requests.exceptions.Timeout as errt:
            print ("[TIMEOUT ERROR]",errt)
        except requests.exceptions.RequestException as err:
            print ("[REQUEST EXCEPTION]",err)

        status_code = response.status_code

        if status_code == 204:
            data = {
                'operation': '[%s] %s' % (method, response.url),
                'status': 'The server successfully processed the request'
            }
        elif status_code == 403:
            # Decode JWT
            print('[Error]')
            print('Access to the requested resource is forbidden (HTTP status code 403).')
            print('\r\n[Resource]')
            print(f'[{method}] {uri}')
            print('\r\n[Response]')
            print(response.json())
            claimset = jwt.decode(self.access_token, options={"verify_signature": False})
            print('\r\n[Credentials]')
            data = {
                'applicationId': claimset.get('appid', None),
                'objectId': claimset.get('oid', None),
                'tenantId': claimset.get('tid',None)
            }
        elif 'Content-Type' in response.headers:
            if response.headers['Content-Type'] == 'text/csv; charset=UTF-8':
                filepath = os.path.join(os.getcwd(),'export.csv')
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                data = {
                    'status_code': response.status_code,
                    'export': filepath
                }
            elif response.headers['Content-Type'] == 'application/octet-stream':
                filepath = os.path.join(os.getcwd(),'export.csv')
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                data = {
                    'status_code': response.status_code,
                    'export': filepath
                }
            else:
                try:
                    data = response.json()
                except ValueError:
                    data = {
                        'url': response.url,
                        'status_code': response.status_code,
                        'reason': response.reason
                    }
        else:
            status_code = response.status_code
            status_msg = responses[status_code]
            print(f"[INFO] HTTP Status Code: {status_code} ({status_msg})")

            try:
                data = response.json()
            except ValueError:
                data = response.content
        return data
