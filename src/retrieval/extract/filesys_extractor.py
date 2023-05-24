from typing import List
import os

from .document_extractor import DocumentExtractor, DocumentExtractorResult

def file_metadata(file_name, file_path):
    return {
        'file_name': file_name,
        'file_path': file_path,
        'last_modified_time': int(os.path.getmtime(file_path)),
    }

class FilesysExtractor(DocumentExtractor):
    def extract_from_file(self, directory, file_name) -> List[DocumentExtractorResult]:
        try:
          file_path = os.path.join(os.path.abspath(directory), file_name)

          if not self.should_extract_file(file_path):
                return []

          with open(file_path, 'r', encoding='utf-8') as f:
              document = f.read()
              metadata = file_metadata(file_name, file_path)
              return self.extract(document, metadata)
        except UnicodeDecodeError:
            # TODO handle
            return []
        except IOError as e:
            # TODO handle
            return []

    def extract_from_directory(self, directory) -> List[DocumentExtractorResult]:
        extracted = []

        for root, dirs, files in os.walk(directory):
            for file_name in files:
                extracted.extend(self.extract_from_file(root, file_name))

        return extracted
    
    def should_extract_file(self, file_path):
        return True
