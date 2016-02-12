import unittest
import jenkinsapi
from jenkinsconnection import JenkinsConnection
from jenkinsapi.jenkins import Jenkins

class TddInPythonExample(unittest.TestCase):

	JENKINS_TEST_SERVER = "http://builds.apache.org"
	JENKINS_TEST_JOB = "Phoenix-4.4-HBase-1.0"

	def test_jenkins_connection(self):
		jenkins = JenkinsConnection(self.JENKINS_TEST_SERVER, self.JENKINS_TEST_JOB)
		self.assertEqual(jenkins.jenkins_server, self.JENKINS_TEST_SERVER)
		self.assertEqual(jenkins.jenkins_job, self.JENKINS_TEST_JOB)
		self.assertIsInstance(jenkins.jenkins_ref, Jenkins)

	#def test_get_last_ten_builds(self):	
	#	jenkins = JenkinsConnection(JENKINS_TEST_SERVER, JENKINS_TEST_JOB)
	#	builds = jenkins.getLastTenBuilds()
	#	assertEqual(len(builds), 10)


