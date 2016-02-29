"""Test cases for QueryJenkins module"""

import unittest
from unittest import mock
import re
from jenkinsapi.jenkins import Jenkins
from app.queryjenkins import QueryJenkins


class QueryJenkinsTest(unittest.TestCase):
    """Test Jenkins toolox class implemention"""

    JENKINS_TEST_SERVER = "http://127.0.0.1"
    JENKINS_TEST_JOB = "testjob"
    DATE_FORMAT = "%Y.%m.%d"
    TEST_VALUES = {
        "2016.02.08": {
            "num_tickets": 2,
            "tickets_jql": ""
        },
        "2016.02.05": {
            "num_tickets": 3,
            "tickets_jql": ""
        },
        "2016.02.09": {
            "num_tickets": 4,
            "tickets_jql": ""
        }
    }

    _qjinstance = None

    def setUp(self):
        self._qjinstance = QueryJenkins()

    @mock.patch.object(Jenkins, "_poll")
    @mock.patch.object(Jenkins, "get_job")
    def test_get_builds_job(self, mock_getjob, mock_poll):
        """Test call to get_builds method"""
        mock_poll.return_value = {}
        builds = self._qjinstance.get_builds(
            self.JENKINS_TEST_SERVER,
            self.JENKINS_TEST_JOB,
            10
        )
        self.assertEqual(builds, [], "get_builds returns a list")
        mock_getjob.assert_called_once_with(self.JENKINS_TEST_JOB)

    @mock.patch("app.queryjenkins.xlsxwriter")
    def test_export_as_excel_file(self, mock_xlswriter):
        """Tests export of the results into an Excel file"""
        self._qjinstance.export_as_excel_file("test.xlsx", [])
        mock_xlswriter.Workbook.assert_called_once_with("test.xlsx")


class RegexTest(unittest.TestCase):
    """Test class for checking regular expressions matches"""

    def test_ticket_regex(self):
        """Verify parsing of ticket ids from commit messages"""
        expressions = [
            "XX-123 [test] test test test",
            "test test XY-1234",
            "Etc etc XYTABC-123123 Etc Etc",
            "AA-1111 [category] test test test test test test test test test",
            "AA-1111 [CATEGORY] test ",
            "AA-1111 [test] Test test",
            "AA-1111 [Test][Test2]test test test test test test test",
            "Test \"AA-1111 test test test 1.1.1 test\"",
            "test test test test AA-1111 test"
        ]
        alltickets_regex = re.compile(QueryJenkins.TICKET_REGEX)
        for exp in expressions:
            match = alltickets_regex.search(exp)

            assert match.group(1) is not None
