import unittest
from unittest import mock
from app.queryjira import QueryJira


class QueryJiraTestCase(unittest.TestCase):

    JIRA_TEST_SERVER = "127.0.0.1"
    JIRA_TEST_TOKEN = "token"
    JIRA_TEST_SECRET = "secret"
    JIRA_TEST_KEY = "key"
    JIRA_TEST_CERTFILE = "file.cert"

    @mock.patch("app.queryjira.io")
    def testConnectToJira(self, mock_io):
        # mock_io.open.return_value = None
        # jira = QueryJira()
        # jira.connectToJira(
        #     self.JIRA_TEST_SERVER,
        #     self.JIRA_TEST_TOKEN,
        #     self.JIRA_TEST_SECRET,
        #     self.JIRA_TEST_KEY,
        #     self.JIRA_TEST_CERTFILE)
        pass

    def testFindTicketChapterValues(self):
        pass
