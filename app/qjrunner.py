from app.queryjenkins import QueryJenkins
import re
import xlsxwriter
from datetime import date
from datetime import datetime
from datetime import timedelta


JENKINS_JOB = ""
JENKINS_SERVER = ""
NUMBER_OF_PAST_BUILDS = 250 # use 250 to start from 2015.09.16
DATE_FORMAT = "%Y.%m.%d"


def _getTicketNumbers(build, ticket_regex):
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


def _findWebTickets(build):
    web_ticket_numbers = _getTicketNumbers(
        build, r"([A-Z]+-\d+).+?\[W[eE][bB]\]")
    return web_ticket_numbers


def _findAllTickets(build):
    all_ticket_numbers = _getTicketNumbers(build, r"([A-Z]+-\d+)")
    return all_ticket_numbers


def _findPHPTickets(build, alltickets, webtickets):
    return list(set(alltickets) - set(webtickets))


def _mapBuildEntriesToPerDayValues(buildentries):
    lowest_time = sorted(buildentries.keys())[0]

    history = datetime.strptime(lowest_time, DATE_FORMAT).date()
    today = date.today()
    delta = timedelta(days=1)

    dayvalues = {}
    current_entry = history
    while current_entry < today:
        current_as_string = date.strftime(current_entry, DATE_FORMAT)

        if current_as_string in buildentries:
            dayvalues[current_as_string] = buildentries[current_as_string]
        else:
            dayvalues[current_as_string] = 0

        current_entry += delta

    return dayvalues


workbook = xlsxwriter.Workbook("buildtickets.xlsx")
worksheet = workbook.add_worksheet()
xls_number_format = workbook.add_format({'num_format': '0'})
xls_date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})

qjinstance = QueryJenkins()
qjinstance.connectToJenkins(JENKINS_SERVER)
buildlist = qjinstance.getBuilds(JENKINS_JOB, NUMBER_OF_PAST_BUILDS)
greenbuilds = qjinstance.getGreenBuilds(buildlist)

entries = {}

for b in greenbuilds:
    print("main loop build: ", b.get_number())
    time = b.get_timestamp()
    tickets = len(_getTicketNumbers(b))
    time_formatted = str(time.strftime(DATE_FORMAT))
    if time_formatted in entries:
        entries[time_formatted] = entries[time_formatted] + tickets
    else:
        entries[time_formatted] = tickets


dayvalues = _mapBuildEntriesToPerDayValues(entries)

line_counter = 1
for t in sorted(dayvalues):
    worksheet.write(
        'A'+str(line_counter), t, xls_date_format)
    worksheet.write_number(
        'B'+str(line_counter), dayvalues[t], xls_number_format)
    line_counter += 1

workbook.close()
