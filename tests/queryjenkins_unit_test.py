import unittest
import mock
import re
import tempfile
import os
import os.path
from datetime import date
from jenkinsapi.jenkins import Jenkins
from app.queryjenkins import QueryJenkins


class RegexTest(unittest.TestCase):
    def testTicketRegex(self):
        expressions = [
            "LV-246 [Logging] Adding locations to user properties",
            "removed the exception when event type is unknown LV-2470",
            "Etc etc PHPBAC-342 Etc Etc",
            "LV-2731 [News] Changed from using the app ID to the advert ID for",
            "LV-2731 [News] Fix using combination of both IDs",
            "LV-2796 [Tests] Fixed multiple instantiation of user object",
            "LV-2779 [Misc] Remove config from ai",
            "LV-2522 [Web][Match]Add prevenDefault to match vote to avoid constant"
        ]
        alltickets_regex = re.compile(r"([A-Z]+-\d+)")
        for exp in expressions:
            match = alltickets_regex.search(exp)
            assert match.group(1) is not None

        web_regex = re.compile(r"([A-Z]+-\d+).+?\[W[eE][bB]\]")
        for i, exp in enumerate(expressions):
            match = web_regex.search(exp)
            if i in [0, 1, 2, 3, 4, 5, 6]:
                assert match is None
            else:
                assert match.group(1) is not None


class QueryJenkinsTest(unittest.TestCase):

    JENKINS_TEST_JOB = "testjob"
    JENKINS_TEST_SERVER = "http://127.1.1.1"
    DATE_FORMAT = "%Y.%m.%d"
    TEST_VALUES = {
        "2016.02.08": 12,
        "2016.02.05": 18,
        "2016.02.09": 17
    }

    def setUp(self):
        self.qj = QueryJenkins()

    # @mock.patch.object("Jenkins", "get_job")
    # def testGetBuilds(self, _getjob):
    #     _getjob.return_value = {
    #         'jobs': [
    #             {'name': 'job_one',
    #              'url': 'http://localhost:8080/job_one',
    #              'color': 'blue'},
    #             {'name': 'job_two',
    #              'url': 'http://localhost:8080/job_two',
    #              'color': 'blue'},
    #         ]
    #     }
    #     builds = self.qj.getBuilds(
    #         self.JENKINS_TEST_SERVER, self.JENKINS_TEST_JOB, 3)
    #     # mock_jenkins.__init__.assert_called_with(self.JENKINS_TEST_SERVER)
    #     mock_jenkins.get_job.assert_called_with(self.JENKINS_TEST_JOB)

    def testMapBuildEntriesToPerDayValues(self):
        dayvalues = self.qj.mapBuildEntriesToPerDayValues(self.TEST_VALUES)
        sorted_dayvalues = sorted(dayvalues)
        assert "2016.02.05" == sorted_dayvalues[0]
        assert "2016.02.06" == sorted_dayvalues[1]
        today = date.today()
        today_as_string = date.strftime(today, self.DATE_FORMAT)
        assert today_as_string == sorted_dayvalues[-1]

    def testExportAsExcelFile(self):
        testfile = os.path.join(tempfile.gettempdir(), "test.xlsx")
        self.qj.exportAsExcelFile(testfile, self.TEST_VALUES)
        self.assertTrue(os.path.isfile(testfile), "Successfully created xlsx file")
        os.remove(testfile)
        # assume called xlsxwriter.Workbook("test.xlsx")
        # (this as integration test?) assume called worksheet.write('A'+str(line_counter), t, xls_date_format))
        # assume called xlsxwriter.Workbook.close()

    # @mock.patch.object(Jenkins, '_poll')
    # @mock.patch.object(QueryJenkins, 'getListOfBuilds')
    # def testGetListOfBuilds(self, _poll, getListOfBuilds):
    # 	getListOfBuilds.return_value = [ 1, 2, 3]
    # 	self.qj.connectToJenkins("http://127.0.0.1")
    # 	assert self.qj.getListOfBuilds("jobname") == [ 1, 2, 3]
