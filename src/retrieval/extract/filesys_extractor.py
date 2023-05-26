from typing import List
import os

from .document_extractor import DocumentExtractor, DocumentExtractorResult

def file_metadata(file_path):
    return {
        'file_name': os.path.basename(file_path),
        'file_path': file_path,
        'last_modified_time': int(os.path.getmtime(file_path)),
    }

class FileExtractor(DocumentExtractor):
    def condition(self, file_path):
        return True

    def extract(self, file_path, additional_metadata = None) -> List[DocumentExtractorResult]:
        if not self.condition(file_path):
            return []

        try:
          with open(file_path, 'r', encoding='utf-8') as f:
              document = f.read()
              metadata = file_metadata(file_path)
              if additional_metadata is not None:
                  metadata.update(additional_metadata)
              return super().extract(document, metadata)
        except UnicodeDecodeError:
            # TODO handle
            return []
        except IOError as e:
            # TODO handle
            return []

class DirectoryExtractor(DocumentExtractor):
    def __init__(self, extractors: List[FileExtractor]=None):
        if extractors is None:
            extractors = [FileExtractor()]

        super().__init__(extractors)

    def extract(self, directory, additional_metadata = None) -> List[DocumentExtractorResult]:
        extracted = []

        for root, dirs, files in os.walk(directory):
            for file_name in files:
                absolute_file_path = os.path.join(os.path.abspath(root), file_name)
                extracted.extend(super().extract(absolute_file_path, additional_metadata))

        return extracted
