import io
from jira import JIRA


class QueryJira(object):

    _jira_handle = None

    def _oauth(self, token, secret, key, certfile):
        key_cert_data = None
        with io.open(certfile, 'r') as key_cert_file:
            key_cert_data = key_cert_file.read()

        oauth_dict = {
            'access_token': token,
            'access_token_secret': secret,
            'consumer_key': key,
            'key_cert': key_cert_data
        }
        return oauth_dict

    def connectToJira(self, server, token, secret, key, certfile):
        self._oauth(token, secret, key, certfile)
        #_jira_handle = JIRA(oauth=oauth_dict)
        pass

    def findTicketChapterValues(self, tickets):
        tickets_chapters = {}
        query = "key in (" + tickets.join(",") + ")"
        results = self._jira_handle.search_issues(query)
        for issue in results:
            tickets_chapters[issue.key] = issue.fields.customfield_11902
        return tickets_chapters
