import ast
import os
import fnmatch
from radon.raw import analyze

from ..document_extractor import AbstractDocumentExtractor, DocumentExtractorResult, DocumentExtractorResults

class Extractor:
    node_type = None
    output_type = None

    def condition(self, node):
        return NotImplementedError

    def extract(self, node): # TODO rename document
        return NotImplementedError
    
    def metadata(self, node, additional_metadata=None):
        code = ast.unparse(node)
        raw_metrics = analyze(code)

        metadata = {
            'node_type': self.node_type,
            'output_type': self.output_type,
            'node_name': hasattr(node, 'name') and node.name or "",
            'lineno': hasattr(node, 'lineno') and node.lineno or "",
            'loc': raw_metrics.loc,  # Lines of code
            'lloc': raw_metrics.lloc,  # Logical lines of code
            'sloc': raw_metrics.sloc,  # Source lines of code (excluding comments and blank lines)
        }

        if additional_metadata is not None:
            metadata.update(additional_metadata)
        
        return metadata

    def process(self, node, additional_metadata=None): # TODO rename extract
        if self.condition(node):
            return DocumentExtractorResult(
                document=self.extract(node),
                metadata=self.metadata(node, additional_metadata)
            )
        else:
            return None

class CodeExtractor(Extractor):
    output_type = "code"
    def extract(self, node):
        return ast.unparse(node)

class AstExtractor(Extractor):
    output_type = "ast"
    def extract(self, node):
        return ast.dump(node)

class ModuleExtractor(CodeExtractor):
    node_type = "module"

    def condition(self, node):
        return isinstance(node, ast.Module)
    
class ModuleAstExtractor(AstExtractor):
    node_type = "module"

    def condition(self, node):
        return isinstance(node, ast.Module)

class FunctionExtractor(CodeExtractor):
    node_type = "function"

    def condition(self, node):
        return isinstance(node, ast.FunctionDef) and not isinstance(node.parent, ast.ClassDef)

class FunctionAstExtractor(AstExtractor):
    node_type = "function"

    def condition(self, node):
        return isinstance(node, ast.FunctionDef) and not isinstance(node.parent, ast.ClassDef)

class MethodExtractor(CodeExtractor):
    node_type = "method"

    def condition(self, node):
        return isinstance(node, ast.FunctionDef) and isinstance(node.parent, ast.ClassDef)

class MethodAstExtractor(AstExtractor):
    node_type = "method"

    def condition(self, node):
        return isinstance(node, ast.FunctionDef) and isinstance(node.parent, ast.ClassDef)

class ClassExtractor(CodeExtractor):
    node_type = "class"

    def condition(self, node):
        return isinstance(node, ast.ClassDef)

class ClassAstExtractor(AstExtractor):
    node_type = "class"

    def condition(self, node):
        return isinstance(node, ast.ClassDef)

class CommentExtractor(Extractor):
    node_type = "comment"
    output_type = "comment"

    def condition(self, node):
        return isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)

    def extract(self, node):
        return node.value.s

EXTRACTORS = [
    ModuleExtractor(),
    ModuleAstExtractor(),
    FunctionExtractor(),
    FunctionAstExtractor(),
    MethodExtractor(),
    MethodAstExtractor(),
    ClassExtractor(),
    ClassAstExtractor(),
    # ImportExtractor(),
    CommentExtractor(),
    # DecoratorExtractor(),
    # CallExtractor(),
    # AssignExtractor(),
    # AttributeAccessExtractor(),
]

def file_metadata(file_name, file_path):
    return {
        'file_name': file_name,
        'file_path': file_path,
        'last_modified_time': int(os.path.getmtime(file_path)),
    }

class PythonExtractor(AbstractDocumentExtractor):
    def __init__(self, extractors=None):
        self.extractors = extractors or EXTRACTORS

    def extract_from_source(self, source_code, additional_metadata_for_node=None) -> DocumentExtractorResults:
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            # TODO handle
            return []

        # Add parent references to each node
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        extracted = []

        for node in ast.walk(tree):
            for extractor in self.extractors:
                result = extractor.process(node, additional_metadata_for_node)
                if result is not None:
                    extracted.append(result)

        return extracted

    def extract_from_file(self, directory, file_name) -> DocumentExtractorResults:
        try:
          file_path = os.path.join(os.path.abspath(directory), file_name)

          with open(file_path, 'r', encoding='utf-8') as f:
              source_code = f.read()
              metadata = file_metadata(file_name, file_path)
              return self.extract_from_source(source_code, metadata)
        except UnicodeDecodeError:
            # TODO handle
            return []
        except IOError as e:
            # TODO handle
            return []

    def extract(self, directory) -> DocumentExtractorResults:
        extracted = []

        for root, dirs, files in os.walk(directory):
            for file_name in fnmatch.filter(files, '*.py'):
                extracted.extend(self.extract_from_file(root, file_name))

        return extracted
