from app.queryjenkins import QueryJenkins


# JENKINS_SERVER = "http://127.0.0.1"
# JENKINS_JOB = "testjob"
JENKINS_SERVER = "http://builds.apache.org"
JENKINS_JOB = "Phoenix-4.4-HBase-1.0"
# use 250 to start from 2015.09.16
NUMBER_OF_PAST_BUILDS = 1
DATE_FORMAT = "%Y.%m.%d"


# def _findWebTickets(qj, build):
#     web_ticket_numbers = qj.getTicketNumbers(
#         build, r"([A-Z]+-\d+).+?\[W[eE][bB]\]")
#     return web_ticket_numbers


# def _findAllTickets(qj, build):
#     all_ticket_numbers = qj.getTicketNumbers(build, r"([A-Z]+-\d+)")
#     return all_ticket_numbers


# def _findPHPTickets(build, alltickets, webtickets):
#     return list(set(alltickets) - set(webtickets))


qj = QueryJenkins()
builds = qj.getBuilds(JENKINS_SERVER, JENKINS_JOB, NUMBER_OF_PAST_BUILDS)

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

