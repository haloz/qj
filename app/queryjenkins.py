import re
from datetime import date
from datetime import datetime
from datetime import timedelta
from jenkinsapi.jenkins import Jenkins


class QueryJenkins(object):

    DATE_FORMAT = "%Y.%m.%d"

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

    def getTicketNumbers(self, build, ticket_regex):
        items = build.get_changeset_items()
        ticket_numbers = []
        regex = re.compile(ticket_regex)

        for entry in items:
            message = entry["msg"]

            noissue = re.compile(r"#noissue")
            if not noissue.search(message):
                match = regex.search(message)
                if match is None:
                    print("found malformed message in build: ", build.get_number())
                    print("with message: ", message)
                else:
                    ticket = match.group(1)
                    if ticket not in ticket_numbers:
                        ticket_numbers.append(ticket)

        return ticket_numbers

    def mapBuildEntriesToPerDayValues(self, buildentries):
        lowest_time = sorted(buildentries.keys())[0]

        history = datetime.strptime(lowest_time, self.DATE_FORMAT).date()
        today = date.today()
        delta = timedelta(days=1)

        dayvalues = {}
        current_entry = history
        while current_entry <= today:
            current_as_string = date.strftime(current_entry, self.DATE_FORMAT)

            if current_as_string in buildentries:
                dayvalues[current_as_string] = buildentries[current_as_string]
            else:
                dayvalues[current_as_string] = 0

            current_entry += delta

        return dayvalues

