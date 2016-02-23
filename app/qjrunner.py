import sys
import argparse
from app.queryjenkins import QueryJenkins


NUMBER_OF_PAST_BUILDS = 5
DATE_FORMAT = "%Y.%m.%d"


def _parseArguments(argv):
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


def main(argv):
    argvdict = _parseArguments(argv)
    qj = QueryJenkins()
    builds = qj.getBuilds(
        argvdict["server"],
        argvdict["username"],
        argvdict["password"],
        argvdict["jobname"],
        NUMBER_OF_PAST_BUILDS)

    entries = {}

    for b in builds:
        print("main loop build: ", b.get_number())
        time = b.get_timestamp()
        tickets = len(qj.getTicketNumbers(b, r"([A-Z]+-\d+)"))
        time_formatted = str(time.strftime(DATE_FORMAT))
        if time_formatted in entries:
            entries[time_formatted] = entries[time_formatted] + tickets
        else:
            entries[time_formatted] = tickets

    per_day_values = qj.mapBuildEntriesToPerDayValues(entries)
    qj.exportAsExcelFile("buildtickets.xlsx", per_day_values)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

