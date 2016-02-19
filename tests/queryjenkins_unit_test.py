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

    # @mock.patch.object(Jenkins, '_poll')
    # @mock.patch.object(QueryJenkins, 'getListOfBuilds')
    # def testGetListOfBuilds(self, _poll, getListOfBuilds):
    # 	getListOfBuilds.return_value = [ 1, 2, 3]
    # 	self.qj.connectToJenkins("http://127.0.0.1")
    # 	assert self.qj.getListOfBuilds("jobname") == [ 1, 2, 3]
