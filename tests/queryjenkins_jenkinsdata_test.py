from pytest_bdd import scenario, given, when
# from app import qj

JENKINS_TEST_SERVER = "http://builds.apache.org"
JENKINS_TEST_JOB = "Phoenix-4.4-HBase-1.0"


# def setUp(self):
#     pass


# @scenario('qr_jenkinsdata.feature', 'Find all 10 last successful builds')
# def test_jenkinsdata():
#     pass


# @given('A Jenkins connection is established')
# def test_jenkins_connection():
#     qjinstance = qj.QueryJenkins()
#     assert qjinstance.connectToJenkins(JENKINS_TEST_SERVER)


# @when('We can get a list of builds of a specific job')
# def test_get_list_of_builds():
#     qjinstance = qj.QueryJenkins()
#     qjinstance.connectToJenkins(JENKINS_TEST_SERVER)
#     buildlist = qjinstance.getListOfBuilds(JENKINS_TEST_JOB)
#     assert buildlist == [0]
