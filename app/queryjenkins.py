import re
from datetime import date
from datetime import datetime
from datetime import timedelta
import xlsxwriter
from jenkinsapi.jenkins import Jenkins


class QueryJenkins(object):

    DATE_FORMAT = "%Y.%m.%d"

    def getBuilds(self, server, jobname, amount):
        jenkins_libary = Jenkins(server)
        jenkins_job = jenkins_libary.get_job(jobname)
        lastgoodbuild = jenkins_job.get_last_good_build()
        lastbuildid = lastgoodbuild.get_number()
        builds = []
        for build_id in range(lastbuildid, lastbuildid - amount, -1):
            current_build = jenkins_job.get_build(build_id)
            if current_build.is_good():
                builds.append(current_build)

        return builds

    def getTicketNumbers(self, build, ticket_regex):
        items = build.get_changeset_items()
        ticket_numbers = []
        regex = re.compile(ticket_regex)

        for entry in items:
            message = entry["msg"]
            print("-- found message: ", message)

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

    def exportAsExcelFile(self, filename, values):
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        xls_number_format = workbook.add_format({'num_format': '0'})
        xls_date_format = workbook.add_format({'num_format': 'yyyy.mm.dd'})
        line_counter = 1
        for t in sorted(values):
            worksheet.write(
                'A'+str(line_counter), t, xls_date_format)
            worksheet.write_number(
                'B'+str(line_counter), values[t], xls_number_format)
            line_counter += 1
        print("wrote file:", filename)
        workbook.close()

