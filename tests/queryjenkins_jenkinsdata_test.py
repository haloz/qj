import unittest
from unittest import mock
from pytest_bdd import scenario, given, when, then
from app.queryjenkins import QueryJenkins

@scenario('queryjenkins_jenkinsdata.feature', 'Find all 10 last successful builds')
class QueryJenkinsTestCase(unittest.TestCase):

    JENKINS_TEST_JOB = "testjob"
    JENKINS_TEST_SERVER = "http://127.1.1.1"

    @given('A Jenkins connection is established')
    @mock.patch("app.queryjenkins.Jenkins")
    def test_jenkins_connection(self, mock_jenkins):
        qjinstance = QueryJenkins()
        qjinstance.connectToJenkins(self.JENKINS_TEST_SERVER)
        mock_jenkins.assert_called_with(self.JENKINS_TEST_SERVER)

    @when('We can get a list of builds of a specific job')
    @mock.patch("app.queryjenkins.Jenkins")
    def test_get_builds(self, mock_jenkins):
        qjinstance = QueryJenkins()
        qjinstance.connectToJenkins(self.JENKINS_TEST_SERVER)
        buildlist = qjinstance.getBuilds(self.JENKINS_TEST_JOB, 10)
        assert len(buildlist) == 10

    @then('We get these 10 builds, but only green ones')
    @mock.patch("app.queryjenkins.Jenkins")
    def test_get_only_green_builds(self, mock_jenkins):
        qjinstance = QueryJenkins()
        qjinstance.connectToJenkins(self.JENKINS_TEST_SERVER)
        buildlist = qjinstance.getBuilds(self.JENKINS_TEST_JOB, 10)
        greenbuilds = qjinstance.getGreenBuilds(buildlist)
        for b in greenbuilds:
            assert b.is_good()

