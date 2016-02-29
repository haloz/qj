"""Collection of helper classes for date to jenkins-data entries"""
from datetime import date, timedelta


class JenkinsDayEntry(object):
    """Jenkins data on one day"""
    DATE_FORMAT = "%Y.%m.%d"
    date = None
    tickets = []

    def __init(self):
        self.date = None
        self.tickets = []

    def num_tickets(self):
        """Number of tickets on that day"""
        return len(self.tickets)

    def date_as_string(self):
        """The day value as String in Y.m.d format"""
        return date.strftime(self.date, self.DATE_FORMAT)

    def tickets_as_jql(self):
        """All ticket names on that day as little JIRA jql query"""
        if self.num_tickets() > 0:
            return "key IN (" + str.join(",", self.tickets) + ")"
        else:
            return ""


class AllJenkinsDayEntries(object):
    """All Jenkins data day entries"""
    entries = []

    def __init__(self):
        self.entries = []

    def get(self, dateentry):
        """Returns a JenkinsDayEntry for the given date"""
        for item in self.entries:
            if item.date == dateentry:
                return item
        return False

    def add(self, newitem):
        """Add a new JenkinsDayEntry to the entries, but only if for the given
           day we don't already have one. If there's already one then just add
           the tickets from the new entry to the existing ones"""
        if newitem.date in self.alldays():
            existingitem = self.get(newitem.date)
            self.entries.remove(existingitem)
            newitem.tickets += existingitem.tickets
        self.entries.append(newitem)

    def alldays(self):
        """All days from the stored JenkinsDayEntrys"""
        items = []
        for item in self.entries:
            items.append(item.date)
        return items

    def alldays_as_string(self):
        """All days as Y.m.d formated string from the stored
           JenkinsDayEntrys"""
        items = []
        for item in self.entries:
            items.append(item.date_as_string())
        return items

    def lowest_date(self):
        """In the stored data the day of the oldest entry"""
        lowest_item = self.entries[0]
        for item in self.entries:
            if lowest_item.date > item.date:
                lowest_item = item
        return lowest_item.date

    def entries_with_empty_days(self):
        """All stored entries but together with filled-in zero values.
           Based on the today date and going back to the oldest entry, for
           each day in that time frame a value is returned. If there's data
           for a day in the stored entries this is returned, otherwise an
           entry with zero tickets"""
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
