from datetime import date, timedelta


class JenkinsDayEntry(object):
    DATE_FORMAT = "%Y.%m.%d"
    date = None
    tickets = []

    def __init(self):
        self.date = None
        self.tickets = []

    def num_tickets(self):
        return len(self.tickets)

    def date_as_string(self):
        return date.strftime(self.date, self.DATE_FORMAT)

    def tickets_as_jql(self):
        if self.num_tickets() > 0:
            return "key IN (" + str.join(",", self.tickets) + ")"
        else:
            return ""


class AllJenkinsDayEntries(object):

    def __init__(self):
        self.entries = []

    def get(self, date):
        for item in self.entries:
            if item.date == date:
                return item
        return False

    def add(self, item):
        if item.date in self.alldays():
            existing = self.get(item.date)
            self.entries.remove(existing)
            item.tickets += existing.tickets

        self.entries.append(item)

    def alldays(self):
        items = []
        for item in self.entries:
            items.append(item.date)
        return items

    def alldays_as_string(self):
        items = []
        for item in self.entries:
            items.append(item.date_as_string())
        return items

    def lowest_date(self):        
        lowest_item = self.entries[0]
        for item in self.entries:
            if lowest_item.date > item.date:
                lowest_item = item
        return lowest_item.date

    def entries_with_empty_days(self):
        withemptydays = []        
        today = date.today()
        delta = timedelta(days=1)

        current_entry = self.lowest_date()
        while current_entry <= today:
            possibleentry = self.get(current_entry)
            if possibleentry:
                withemptydays.append(possibleentry)
            else:
                jde = JenkinsDayEntry()
                jde.date = current_entry
                withemptydays.append(jde)
            current_entry += delta
        return withemptydays
