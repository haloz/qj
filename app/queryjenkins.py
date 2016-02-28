"""This module handles access to Jenkins"""

import re
from datetime import date
from datetime import datetime
from datetime import timedelta
import xlsxwriter
from jenkinsapi.jenkins import Jenkins
from app.dayentry import AllJenkinsDayEntries, JenkinsDayEntry


class QueryJenkins():
    """Gathers Jenkins job builds and the processed tickets"""

    DATE_FORMAT = "%Y.%m.%d"

    @classmethod
    def get_builds(cls, server, jobname, amount):
        """Given a Jenkins server URL, a job name and the amount of builds
           returns a list of Jenkins builds"""
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
    def export_as_excel_file(cls, filename, values):
        """Output day-to-tickets dictionary into a Excel file"""
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        xls_number_format = workbook.add_format({'num_format': '0'})
        xls_date_format = workbook.add_format({'num_format': 'yyyy.mm.dd'})
        line_counter = 1

        for dayentry in values:
            worksheet.write(
                'A'+str(line_counter), 
                dayentry.date_as_string(), 
                xls_date_format)
            worksheet.write_number(
                'B'+str(line_counter),
                dayentry.num_tickets(),
                xls_number_format)
            worksheet.write(
                'C'+str(line_counter),
                dayentry.tickets_as_jql())
            line_counter += 1
        print("wrote file:", filename)
        workbook.close()
