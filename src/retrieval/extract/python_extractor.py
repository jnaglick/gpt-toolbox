import ast
import fnmatch
from typing import List
from radon.raw import analyze

from .document_extractor import DocumentExtractorResult
from .filesys_extractor import FilesysExtractor

class PythonNodeExtractor:
    node_type = None
    output_type = None

    def condition(self, node):
        return NotImplementedError

    def document(self, node):
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

    def extract(self, node, additional_metadata=None):
        if self.condition(node):
            return [DocumentExtractorResult(
                document=self.document(node),
                metadata=self.metadata(node, additional_metadata)
            )]
        else:
            return []

class CodeExtractor(PythonNodeExtractor):
    output_type = "code"
    def document(self, node):
        return ast.unparse(node)

class AstExtractor(PythonNodeExtractor):
    output_type = "ast"
    def document(self, node):
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

class CommentExtractor(PythonNodeExtractor):
    node_type = "comment"
    output_type = "comment"

    def condition(self, node):
        return isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)

    def document(self, node):
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

class PythonExtractor(FilesysExtractor):
    def __init__(self, extractors: List[PythonNodeExtractor]=None):
        super().__init__(extractors or EXTRACTORS)

    def should_extract_file(self, file_path):
        return fnmatch.fnmatch(file_path, "*.py")

    def extract(self, source_code, additional_metadata_for_node=None):
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            print(e)
            # TODO handle
            return []

        # Add parent references to each node
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        extracted = []

        for node in ast.walk(tree):
            extracted.extend(super().extract(node, additional_metadata_for_node))

        return extracted
