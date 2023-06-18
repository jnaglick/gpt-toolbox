from typing import List
import os

from utils import console
from .document_extractor import DocumentExtractor, DocumentExtractorResult

def file_metadata(file_path):
    return {
        'file_name': os.path.basename(file_path),
        'file_path': file_path,
        'last_modified_time': int(os.path.getmtime(file_path)),
    }

class FileExtractor(DocumentExtractor):
    def run_extract(self, file_path, additional_metadata = None) -> List[DocumentExtractorResult]:
        file_path = os.path.abspath(file_path)

        try:
          with open(file_path, 'r', encoding='utf-8') as f:
              document = f.read()
              metadata = file_metadata(file_path)
              if additional_metadata is not None:
                  metadata.update(additional_metadata)
              return super().run_extract(document, metadata)
        except UnicodeDecodeError as e:
            console.error(f"Failed to decode file: {file_path}: {e}")
            return []
        except IOError as e:
            console.error(f"Failed to extract file: {file_path}: {e}")
            return []

class DirectoryExtractor(DocumentExtractor):
    def __init__(self, extractors: List[FileExtractor]=None):
        if extractors is None:
            extractors = [FileExtractor()]

        super().__init__(extractors)

    def run_extract(self, directory, additional_metadata = None) -> List[DocumentExtractorResult]:
        result = []

        for root, dirs, files in os.walk(directory):
            for file_name in files:
                absolute_file_path = os.path.join(os.path.abspath(root), file_name)
                extract_result = super().run_extract(absolute_file_path, additional_metadata)
                result.extend(extract_result)

        return result
