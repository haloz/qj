import re
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

class JenkinsConnection(object):

	def  __init__(self, server, job_name):
		self.jserver = server
		self.jjob_name = job_name
		self.jref = Jenkins(server)		
		self.jjobref = self.jref[self.jjob_name]
		
	def getLatestBuildId(self):
		latest_build = self.jjobref.get_last_good_build()
		return latest_build.get_number()
