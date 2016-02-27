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
    parser.add_argument(
        "-u", dest="username", nargs="?", default=None, help="username")
    parser.add_argument(
        "-p", dest="password", nargs="?", default=None, help="password")
    return vars(parser.parse_args())


def main():
    """Orchestrate our toolbox to run the Jenkins analysis"""
    argvdict = _parse_arguments()
    qjinstance = QueryJenkins()
    builds = qjinstance.get_builds(
        argvdict["server"],
        argvdict["username"],
        argvdict["password"],
        argvdict["jobname"],
        NUMBER_OF_PAST_BUILDS)

    entries = {}

    for build in builds:
        print("main loop build: ", build.get_number())
        time = build.get_timestamp()
        tickets = len(qjinstance.get_ticket_tumbers(build, r"([A-Z]+-\d+)"))
        time_formatted = str(time.strftime(DATE_FORMAT))
        if time_formatted in entries:
            entries[time_formatted] = entries[time_formatted] + tickets
        else:
            entries[time_formatted] = tickets

    per_day_values = qjinstance.map_build_entries_to_days(entries)
    qjinstance.export_as_excel_file("buildtickets.xlsx", per_day_values)

if __name__ == "__main__":
    sys.exit(main())
