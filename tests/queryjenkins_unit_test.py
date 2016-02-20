import unittest
import mock
from app.queryjenkins import connectToJenkins


class QueryJenkinsTestCase(unittest.TestCase):

    @mock.patch("app.queryjenkins.Jenkins")
    def testConnectToJenkins(self, mock_Jenkins):
        connectToJenkins("http://any_server")
        mock_Jenkins.assert_called_with("http://any_server")
