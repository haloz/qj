from jenkinsapi.jenkins import Jenkins


class QueryJenkins(object):
    def connectToJenkins(self, server):
        self.jref = Jenkins(server)
        return 1

    def getListOfBuilds(self, jobname):
        self.jjobref = self.jref[jobname]
        return [0]
