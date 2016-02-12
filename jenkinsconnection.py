import re
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

class JenkinsConnection(object):

	def  __init__(self, server, job):
		self.jenkins_server = server
		self.jenkins_job = job
		self.jenkins_ref = Jenkins(server)		
		
	#def getLastTenBuilds(self):
	#	return