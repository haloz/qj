"""This module unit tests the QueryConfluence class"""

import unittest
from unittest import mock
from app.queryconfluence import QueryConfluence


class MockOkResponse:
    """Mock response class for successful HTTP request"""
    status_code = 200

    def __init__(self, *args, **kwargs):
        pass


class MockNotFoundResponse:
    """Mock response class for failed HTTP request"""
    status_code = 404

    def __init__(self, *args, **kwargs):
        pass


class QueryConfluenceTestCase(unittest.TestCase):
    """Test case for QueryConfluence class"""
    _qc_instance = None

    def setUp(self):
        self._qc_instance = QueryConfluence()

    @mock.patch("app.queryconfluence.OAuth1Session.get")
    def test_oauth(self, mock_oauthget):
        """Setup a mock to test OAuth of QueryConfluence class"""
        self._qc_instance.oauth(
            "http://localhost:1234",
            "token",
            "secret",
            "key"
        )
        mock_oauthget.assert_called_once_with(
            "http://localhost:1234/plugins/servlet/oauth/authorize?oauth_token=token"
        )

    def test_pack_content(self):
        """Test if id and content are correctly wrapped in a data structure"""
        data = self._qc_instance.pack_content(123, "<h1>Test</h1>")
        self.assertEqual(data["body"]["storage"]["value"], "<h1>Test</h1>")

    def test_check_page_exists(self):
        """Mock-test to check whether a Confluence page exists"""
        with mock.patch(
            "app.queryconfluence.requests.get",
            new=MockNotFoundResponse
        ):
            self.assertFalse(self._qc_instance.check_page_exists(
                "http://localhost:8080/confluence/rest/api/content/",
                123
            ))

        with mock.patch(
            "app.queryconfluence.requests.get",
            new=MockOkResponse
        ):
            self.assertTrue(self._qc_instance.check_page_exists(
                "http://localhost:8080/confluence/rest/api/content/",
                123
            ))

    @mock.patch("app.queryconfluence.requests.post")
    def test_replace_page_content(self, mock_post):
        """Mock-test replacing a Confluence page content"""
        url = "http://localhost:8080/confluence/rest/api/content/"
        data = "<h1>Test</h1>"
        with mock.patch(
            "app.queryconfluence.requests.get",
            new=MockOkResponse
        ):
            self._qc_instance.replace_page_content(url, 11, data)
        mock_post.assert_called_once_with(
            "http://localhost:8080/confluence/rest/api/content/11",
            self._qc_instance.pack_content(11, data),
            auth=('admin', 'admin'),
            headers=({'Content-Type': 'application/json'})
        )
