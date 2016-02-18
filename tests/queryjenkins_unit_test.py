import unittest
import mock
from jenkinsapi.jenkins import Jenkins
from app.queryjenkins import QueryJenkins


class QueryJenkinsTest(unittest.TestCase):
    def setUp(self):
        self.qj = QueryJenkins()

    @mock.patch.object(Jenkins, '_poll')
    def testConnectToJenkins(self, _poll):
        assert self.qj.connectToJenkins("http://127.0.0.1") == 1
