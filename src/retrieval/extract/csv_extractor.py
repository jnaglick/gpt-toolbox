import csv
import fnmatch

from .document_extractor import DocumentExtractor
from .filesys_extractor import FileExtractor

class CsvExtractor(DocumentExtractor):
    def condition(self, source, additional_metadata):
        try:
            reader = csv.reader(source.splitlines())
            headers = next(reader, None)
            if headers is None:
                return False
            for row in reader:
                if len(row) != len(headers):
                    return False
            return True
        except Exception:
            return False

    def run_extract(self, source, additional_metadata=None):
        results = []
        reader = csv.reader(source.splitlines())
        headers = next(reader, None)

        for rownum, row in enumerate(reader):
            document_dict = {headers[i]: value for i, value in enumerate(row)}
            document = '\n'.join(f'{key}: {value}' for key, value in document_dict.items())
            metadata = {'rownum': rownum}
            if additional_metadata is not None:
                metadata.update(additional_metadata)
            results.extend(super().run_extract(document, metadata))
        
        return results

class CsvFileExtractor(FileExtractor):
    def __init__(self):
        super().__init__([CsvExtractor()])

    @staticmethod
    def s_condition(file_path, additional_metadata):
        return fnmatch.fnmatch(file_path, "*.csv")

    def condition(self, file_path, additional_metadata):
        return fnmatch.fnmatch(file_path, "*.csv")
