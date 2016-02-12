import unittest
import jenkinsapi
from jenkinsconnection import JenkinsConnection
from jenkinsapi.jenkins import Jenkins

class TddInPythonExample(unittest.TestCase):

	JENKINS_TEST_SERVER = "http://builds.apache.org"
	JENKINS_TEST_JOB = "Phoenix-4.4-HBase-1.0"


	def setUp(self):
		self.jenkins = JenkinsConnection(self.JENKINS_TEST_SERVER, self.JENKINS_TEST_JOB)

	def test_jenkins_connection(self):		
		self.assertEqual(self.jenkins.jserver, self.JENKINS_TEST_SERVER)
		self.assertEqual(self.jenkins.jjob_name, self.JENKINS_TEST_JOB)
		self.assertIsInstance(self.jenkins.jref, Jenkins)

	def test_get_latest_build_id(self):
		jenkins = JenkinsConnection(self.JENKINS_TEST_SERVER, self.JENKINS_TEST_JOB)
		self.assertEqual(self.jenkins.getLatestBuildId(), 50)


	#def test_get_last_ten_builds(self):	
	#	jenkins = JenkinsConnection(JENKINS_TEST_SERVER, JENKINS_TEST_JOB)
	#	builds = jenkins.getLastTenBuilds()
	#	assertEqual(len(builds), 10)


