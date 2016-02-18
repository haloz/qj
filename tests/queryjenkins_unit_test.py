import unittest
import mock
from jenkinsapi.jenkins import Jenkins
from app.queryjenkins import QueryJenkins


class QueryJenkinsTest(unittest.TestCase):
    def setUp(self):
        self.qj = QueryJenkins()

    def testConnectToJenkins(self):
        pass
        # assert self.qj.connectToJenkins("http://127.0.0.1") == 1
