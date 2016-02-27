"""This module handles access to Atlassian Confluence"""

from urllib.parse import urljoin
import requests
from requests_oauthlib import OAuth1Session


class QueryConfluence(object):
    """Access to Confluence to change the content of a page"""

    _request_token_url = "/plugins/servlet/oauth/request-token"
    _authorization_url = "/plugins/servlet/oauth/authorize"
    _access_token_url = "/plugins/servlet/oauth/access-token"

    @classmethod
    def oauth(cls, base_url, token, secret, key):
        """Authenticate to confluence using OAuth 1.0"""
        token_url = urljoin(
            base_url, cls._authorization_url + "?oauth_token=" + token
        )
        client = OAuth1Session(
            key,
            client_secret=secret,
            resource_owner_key="",
            resource_owner_secret="")
        client.get(token_url)

    @classmethod
    def pack_content(cls, page_id, content):
        """Wrap a Confluence page id and a page content into a data structure
           for the request to Confluence"""
        return {
            "type": "page",
            "id": page_id,
            "body": {
                "storage": {
                    "value": content
                }
            }
        }

    @classmethod
    def check_page_exists(cls, server_url, page_id):
        """Check if a Confluence page exists"""
        response = requests.get(
            urljoin(server_url, str(page_id))
        )
        return response.status_code == 200

    @classmethod
    def replace_page_content(cls, server_url, page_id, content):
        """Replaces the content of a Confluence page"""
        if cls.check_page_exists(server_url, page_id):
            requests.post(
                urljoin(server_url, str(page_id)),
                cls.pack_content(page_id, content),
                auth=('admin', 'admin'),
                headers=({'Content-Type': 'application/json'})
            )
