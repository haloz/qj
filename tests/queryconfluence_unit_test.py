import unittest
from unittest import mock
from urllib.parse import urljoin
from app.queryconfluence import QueryConfluence


class MockOkResponse:
    status_code = 200

    def __init__(self, *args, **kwargs):
        pass


class MockNotFoundResponse:
    status_code = 404

    def __init__(self, *args, **kwargs):
        pass


class QueryConfluenceTestCase(unittest.TestCase):

    qc = None

    def setUp(self):
        self.qc = QueryConfluence()

    def testPackContent(self):
        data = self.qc.packContent(123, "<h1>Test</h1>")
        self.assertEqual(data["body"]["storage"]["value"], "<h1>Test</h1>")

    def testCheckPageExists(self):
        with mock.patch(
            "app.queryconfluence.requests.get",
            new=MockNotFoundResponse
        ):
            self.assertFalse(self.qc.checkPageExists(
                "http://localhost:8080/confluence/rest/api/content/",
                123
            ))

        with mock.patch(
            "app.queryconfluence.requests.get",
            new=MockOkResponse
        ):
            self.assertTrue(self.qc.checkPageExists(
                "http://localhost:8080/confluence/rest/api/content/",
                123
            ))

    @mock.patch("app.queryconfluence.requests.post")
    def testReplacePageContent(self, mock_post):
        url = "http://localhost:8080/confluence/rest/api/content/"
        data = "<h1>Test</h1>"
        with mock.patch(
            "app.queryconfluence.requests.get",
            new=MockOkResponse
        ):
            self.qc.replacePageContent(url, 11, data)
        mock_post.assert_called_once_with(
            "http://localhost:8080/confluence/rest/api/content/11",
            self.qc.packContent(11, data),
            auth=('admin', 'admin'),
            headers=({'Content-Type': 'application/json'})
        )
