from app.queryjenkins import QueryJenkins


JENKINS_SERVER = "http://127.0.0.1"
JENKINS_JOB = "testjob"
# use 250 to start from 2015.09.16
NUMBER_OF_PAST_BUILDS = 250
DATE_FORMAT = "%Y.%m.%d"


def _findWebTickets(qj, build):
    web_ticket_numbers = qj.getTicketNumbers(
        build, r"([A-Z]+-\d+).+?\[W[eE][bB]\]")
    return web_ticket_numbers


def _findAllTickets(qj, build):
    all_ticket_numbers = qj.getTicketNumbers(build, r"([A-Z]+-\d+)")
    return all_ticket_numbers


def _findPHPTickets(build, alltickets, webtickets):
    return list(set(alltickets) - set(webtickets))


qj = QueryJenkins()
qj.connectToJenkins(JENKINS_SERVER)
buildlist = qj.getBuilds(JENKINS_JOB, NUMBER_OF_PAST_BUILDS)
greenbuilds = qj.getGreenBuilds(buildlist)

entries = {}

for b in greenbuilds:
    print("main loop build: ", b.get_number())
    time = b.get_timestamp()
    tickets = len(qj.getTicketNumbers(b))
    time_formatted = str(time.strftime(DATE_FORMAT))
    if time_formatted in entries:
        entries[time_formatted] = entries[time_formatted] + tickets
    else:
        entries[time_formatted] = tickets


dayvalues = qj.mapBuildEntriesToPerDayValues(entries)
qj.exportAsExcelFile("buildtickets.xlsx", dayvalues)


