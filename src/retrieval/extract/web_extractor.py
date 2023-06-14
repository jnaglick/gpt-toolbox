import requests

from utils import web_request

from typing import List
from .document_extractor import DocumentExtractor, DocumentExtractorResult

def web_metadata(url):
    return {
        'url': url,
    }

class WebExtractor(DocumentExtractor):
    def condition(self, url, additional_metadata):
        # TOOD check if the URL is valid/accessible
        return True

    def run_extract(self, url, additional_metadata=None) -> List[DocumentExtractorResult]:
        try:
            response = web_request(url)
            metadata = web_metadata(url)
            if additional_metadata is not None:
                metadata.update(additional_metadata)
            return super().run_extract(response, metadata)
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6

        return []
