"""
This script gathers data about the JIRA ticket ids that are processed in the
last n successful builds of a Jenkins job.

The output is written into an Excel file that can the be processed further
with a chart.

The data output is a table with a date and the amount of processed tickets
of the Jenkins builds on that data.
"""

import sys
import argparse
from app.queryjenkins import QueryJenkins
from app.dayentry import AllJenkinsDayEntries, JenkinsDayEntry


NUMBER_OF_PAST_BUILDS = 5
DATE_FORMAT = "%Y.%m.%d"


def _parse_arguments():
    """Parse command line parameters"""
    parser = argparse.ArgumentParser(
        description="QueryJenkins: a Jenkins build statistics tool.")
    parser.add_argument(
        "-s", dest="server", required=True,
        help="jenkins server url incl. protocol")
    parser.add_argument(
        "-j", dest="jobname", required=True,
        help="jenkins job name")
    parser.add_argument(
        "-d", dest="startdate", required=False,
        help="start date in format \"yyyy.mm.dd\"")
    return vars(parser.parse_args())


def main():
    """Orchestrate our toolbox to run the Jenkins analysis"""
    argvdict = _parse_arguments()
    qjinstance = QueryJenkins()

    buildlist = qjinstance.get_builds(
        argvdict["server"],
        argvdict["jobname"],
        NUMBER_OF_PAST_BUILDS)

    allentries = AllJenkinsDayEntries()

    for build in buildlist:
        dayentry = JenkinsDayEntry()
        dayentry.date = build.get_timestamp().date()
        dayentry.tickets = qjinstance.get_ticket_tumbers(
            build,
            r"([A-Z]+-\d+)"
        )
        allentries.add(dayentry)

    per_day_values = allentries.entries_with_empty_days()
    qjinstance.export_as_excel_file("buildtickets.xlsx", per_day_values)

if __name__ == "__main__":
    sys.exit(main())
