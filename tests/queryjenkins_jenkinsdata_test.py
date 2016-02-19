from pytest_bdd import scenario, given, when, then
from app.queryjenkins import QueryJenkins

JENKINS_TEST_JOB = "Phoenix-4.4-HBase-1.0"
JENKINS_TEST_SERVER = "http://builds.apache.org"





def setUp(self):
    pass


@scenario('queryjenkins_jenkinsdata.feature', 'Find all 10 last successful builds')
def test_jenkinsdata():
    pass


@given('A Jenkins connection is established')
def test_jenkins_connection():
    qjinstance = QueryJenkins()
    assert qjinstance.connectToJenkins(JENKINS_TEST_SERVER)


@when('We can get a list of builds of a specific job')
def test_get_builds():
    qjinstance = QueryJenkins()
    qjinstance.connectToJenkins(JENKINS_TEST_SERVER)
    buildlist = qjinstance.getBuilds(JENKINS_TEST_JOB)
    assert len(buildlist) == 10


@then('We get these 10 builds, but only green ones')
def test_get_only_green_builds():
    qjinstance = QueryJenkins()
    qjinstance.connectToJenkins(JENKINS_TEST_SERVER)
    buildlist = qjinstance.getBuilds(JENKINS_TEST_JOB)
    greenbuilds = qjinstance.getGreenBuilds(buildlist)
    for b in greenbuilds:
        assert b.is_good


