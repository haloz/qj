import unittest
import mock
import re
from jenkinsapi.jenkins import Jenkins
from app.queryjenkins import QueryJenkins


class RegexTest(unittest.TestCase):
    def testTicketRegex(self):
        expressions = [
            "LV-246 [Logging] Adding locations to user properties",
            "removed the exception when event type is unknown LV-2470",
            "Etc etc PHPBAC-342 Etc Etc",
            "LV-2731 [News] Changed from using the app ID to the advert ID for",
            "LV-2731 [News] Fix using combination of both IDs",
            "LV-2796 [Tests] Fixed multiple instantiation of user object",
            "LV-2779 [Misc] Remove config from ai",
            "LV-2522 [Web][Match]Add prevenDefault to match vote to avoid constant"
        ]
        alltickets_regex = re.compile(r"([A-Z]+-\d+)")
        for exp in expressions:
            match = alltickets_regex.search(exp)
            assert match.group(1) is not None

        web_regex = re.compile(r"([A-Z]+-\d+).+?\[W[eE][bB]\]")
        for i, exp in enumerate(expressions):
            print("i", i)
            match = web_regex.search(exp)
            if i in [0,1,2,3,4,5,6]:
                assert match is None
            else:
                assert match.group(1) is not None




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
