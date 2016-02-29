"""Test cases for dayentry module"""
import unittest
from datetime import date, timedelta
from app.dayentry import AllJenkinsDayEntries, JenkinsDayEntry


class DayEntriesTestCase(unittest.TestCase):
    """Test cases for JenkinsDayEntry and AllJenkinsDayEntries classes"""

    def test_storing_entries(self):
        """Verify storing JenkinsDayEntry instances"""
        allentries = AllJenkinsDayEntries()
        dayentry = JenkinsDayEntry()
        dayentry.date = date(2016, 2, 8)
        dayentry.tickets = ["XY-123", "XY-124"]
        allentries.add(dayentry)

        dayentry = JenkinsDayEntry()
        dayentry.date = date(2016, 2, 5)
        dayentry.tickets = ["XY-111"]
        allentries.add(dayentry)

        dayentry = JenkinsDayEntry()
        dayentry.date = date(2016, 2, 9)
        dayentry.tickets = ["XY-222", "XY-333", "XY-444"]
        allentries.add(dayentry)

        self.assertEqual(allentries.get(date(2016, 2, 9)), dayentry)
        self.assertEqual(len(allentries.alldays()), 3)
        self.assertEqual(
            allentries.alldays_as_string(),
            ["2016.02.08", "2016.02.05", "2016.02.09"]
        )

    def test_store_multiple_per_day(self):
        """Multiple entries for a day should be grouped in one entry"""
        allentries = AllJenkinsDayEntries()
        dayentry = JenkinsDayEntry()
        dayentry.date = date(2016, 2, 8)
        dayentry.tickets = ["XY-123", "XY-124"]
        allentries.add(dayentry)

        dayentry = JenkinsDayEntry()
        dayentry.date = date(2016, 2, 8)
        dayentry.tickets = ["XY-111"]
        allentries.add(dayentry)

        self.assertEqual(len(allentries.alldays()), 1)
        self.assertEqual(
            allentries.alldays_as_string(),
            ["2016.02.08"]
        )
        self.assertEqual(allentries.entries[0].num_tickets(), 3)

    def test_entries_with_empty_days(self):
        """Test method to fill sparse data with zero values so that we have
           entries for each day, starting from today to the oldest entry"""
        allentries = AllJenkinsDayEntries()

        dayentry = JenkinsDayEntry()
        dayentry.date = date.today() - timedelta(days=3)
        dayentry.tickets = ["XY-123", "XY-124"]
        allentries.add(dayentry)

        dayentry = JenkinsDayEntry()
        dayentry.date = date.today() - timedelta(days=2)
        dayentry.tickets = ["XY-111"]
        allentries.add(dayentry)

        self.assertEqual(len(allentries.entries_with_empty_days()), 4)
        self.assertEqual(
            allentries.entries_with_empty_days()[0].date,
            date.today() - timedelta(days=3)
        )

    def test_tickets_as_jql(self):
        """List of tickets for an entry can be retrieved as JIRA JQL query"""
        dayentry = JenkinsDayEntry()
        dayentry.date = date.today() - timedelta(days=3)
        dayentry.tickets = ["XY-123", "XY-124"]
        self.assertEqual(
            dayentry.tickets_as_jql(),
            "key IN (XY-123,XY-124)"
        )
