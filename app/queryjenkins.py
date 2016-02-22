from jenkinsapi.jenkins import Jenkins


class QueryJenkins(object):

    def connectToJenkins(self, server):
        self._jenkins_libary = Jenkins(server)
        return 1

    def getBuilds(self, jobname, amount):
        self._jenkins_job = self._jenkins_libary[jobname]
        lastgoodbuild = self._jenkins_job.get_last_good_build()
        lastbuildid = lastgoodbuild.get_number()
        builds = []
        for build_id in range(lastbuildid, lastbuildid - amount, -1):
            current_build = self._jenkins_job.get_build(build_id)
            builds.append(current_build)

        return builds

    def getGreenBuilds(self, builds):
        green_builds = []
        for b in builds:
            if b.is_good():
                green_builds.append(b)
        return green_builds


