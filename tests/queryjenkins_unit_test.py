"""Test cases for QueryJenkins module"""

import unittest
from unittest import mock
import re
from datetime import date
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
        pass


class RegexTest(unittest.TestCase):
    """Test class for checking regular expressions matches"""
    def test_ticket_regex(self):
        """Verify parsing of ticket ids from commit messages"""
        expressions = [
            "LV-246 [Logging] Adding locations to user properties",
            "removed the exception when event type is unknown LV-2470",
            "Etc etc PHPBAC-342 Etc Etc",
            "LV-2731 [News] Changed from using the app ID to the advert ID for",
            "LV-2731 [News] Fix using combination of both IDs",
            "LV-2796 [Tests] Fixed multiple instantiation of user object",
            "LV-2779 [Misc] Remove config from ai",
            "LV-2522 [Web][Match]Add prevenDefault to match vote to avoid constant",
            "Revert \"LV-2734 increase api_version_minimum to 1.13\"",
            "removed old benchmark logic to cleanup the code LV-2741"
        ]
        alltickets_regex = re.compile(r"([A-Z]+-\d+)")
        for exp in expressions:
            match = alltickets_regex.search(exp)

            assert match.group(1) is not None

        web_regex = re.compile(r"([A-Z]+-\d+).+?\[W[eE][bB]\]")
        for i, exp in enumerate(expressions):
            match = web_regex.search(exp)
            if i in [0, 1, 2, 3, 4, 5, 6, 8, 9]:
                assert match is None
            else:
                assert match.group(1) is not None
