"""This module handles access to Jenkins"""

import re
from datetime import date
from datetime import datetime
from datetime import timedelta
import xlsxwriter
from jenkinsapi.jenkins import Jenkins


class QueryJenkins(object):
    """Gathers Jenkins job builds and the processed tickets"""

    DATE_FORMAT = "%Y.%m.%d"

    @classmethod
    def get_builds(cls, server, username, password, jobname, amount):
        """Given a Jenkins server URL, a job name and the amount of builds
           returns a list of Jenkins builds"""
        jenkins_libary = Jenkins(server, username, password)
        jenkins_job = jenkins_libary.get_job(jobname)
        lastgoodbuild = jenkins_job.get_last_good_build()
        lastbuildid = lastgoodbuild.get_number()
        builds = []
        for build_id in range(lastbuildid, lastbuildid - amount, -1):
            current_build = jenkins_job.get_build(build_id)
            if current_build.is_good():
                builds.append(current_build)

        return builds

    @classmethod
    def get_ticket_tumbers(cls, build, ticket_regex):
        """Extract ticket ids from the changeset of a Jenkins build"""
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
                    print(
                        "found malformed message in build: ",
                        build.get_number(), "\n",
                        "with message: ",
                        message
                    )
                else:
                    ticket = match.group(1)
                    if ticket not in ticket_numbers:
                        ticket_numbers.append(ticket)

        return ticket_numbers

    @classmethod
    def map_build_entries_to_days(cls, buildentries):
        """Output a dictionary with per-day entries and the
           amount of tickets on that day"""
        lowest_time = sorted(buildentries.keys())[0]

        history = datetime.strptime(lowest_time, cls.DATE_FORMAT).date()
        today = date.today()
        delta = timedelta(days=1)

        dayvalues = {}
        current_entry = history
        while current_entry <= today:
            current_as_string = date.strftime(current_entry, cls.DATE_FORMAT)

            if current_as_string in buildentries:
                dayvalues[current_as_string] = buildentries[current_as_string]
            else:
                dayvalues[current_as_string] = 0

            current_entry += delta

        return dayvalues

    @classmethod
    def export_as_excel_file(cls, filename, values):
        """Output day-to-tickets dictionary into a Excel file"""
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        xls_number_format = workbook.add_format({'num_format': '0'})
        xls_date_format = workbook.add_format({'num_format': 'yyyy.mm.dd'})
        line_counter = 1
        for entry in sorted(values):
            worksheet.write(
                'A'+str(line_counter), entry, xls_date_format)
            worksheet.write_number(
                'B'+str(line_counter), values[entry], xls_number_format)
            line_counter += 1
        print("wrote file:", filename)
        workbook.close()
