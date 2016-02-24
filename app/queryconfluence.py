import requests
from urllib.parse import urljoin


class QueryConfluence(object):

    def packContent(self, page_id, content):
        return {
            "type": "page",
            "id": page_id,
            "body": {
                "storage": {
                    "value": content
                }
            },
            "id": page_id,
        }

    def checkPageExists(self, server_url, page_id):
        response = requests.get(
            urljoin(server_url, str(page_id))
        )
        if response.status_code == 200:
            return True
        else:
            return False

    def replacePageContent(self, server_url, page_id, content):
        if self.checkPageExists(server_url, page_id):
            requests.post(
                urljoin(server_url, str(page_id)),
                self.packContent(page_id, content),
                auth=('admin', 'admin'),
                headers=({'Content-Type': 'application/json'})
            )
