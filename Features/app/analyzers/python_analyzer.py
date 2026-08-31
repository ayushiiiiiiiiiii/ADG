import ast
from app.analyzers.base_analyzer import BaseAnalyzer
from app.features.feature_schema import ExtractedFeatures

class FeatureExtractionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.features = ExtractedFeatures()
        self.current_loop_depth = 0
        self.defined_functions = set()
        self.current_function = None

    def visit_For(self, node):
        self.features.for_loop_count += 1
        self.features.loop_count += 1
        
        self.current_loop_depth += 1
        self.features.max_loop_depth = max(self.features.max_loop_depth, self.current_loop_depth)
        if self.current_loop_depth > 1:
            self.features.nested_loop_count += 1
            
        # Very rudimentary check for linear vs logarithmic (for-loops in Python are typically linear if iterating over range)
        # We'll just assume linear for simplicity unless we see specific patterns, but counting all as linear initially
        self.features.linear_loop_count += 1
        
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node):
        self.features.while_loop_count += 1
        self.features.loop_count += 1
        
        self.current_loop_depth += 1
        self.features.max_loop_depth = max(self.features.max_loop_depth, self.current_loop_depth)
        if self.current_loop_depth > 1:
            self.features.nested_loop_count += 1

        # Determine if it's logarithmic (checking for *= or /=)
        is_log = False
        for child in ast.walk(node):
            if isinstance(child, ast.AugAssign):
                if isinstance(child.op, (ast.Mult, ast.Div, ast.FloorDiv)):
                    is_log = True
                    break
        
        if is_log:
            self.features.logarithmic_loop_count += 1
        else:
            self.features.linear_loop_count += 1
            
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_If(self, node):
        self.features.if_count += 1
        self.features.condition_count += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.features.function_count += 1
        self.defined_functions.add(node.name)
        
        prev_function = self.current_function
        self.current_function = node.name
        
        self.generic_visit(node)
        
        self.current_function = prev_function

    def visit_Call(self, node):
        self.features.function_call_count += 1
        if isinstance(node.func, ast.Name):
            if node.func.id == self.current_function:
                self.features.recursive = True
                self.features.recursive_call_count += 1
        self.generic_visit(node)
        
    def generic_visit(self, node):
        self.features.ast_depth += 1
        if isinstance(node, ast.stmt):
            self.features.statement_count += 1
        super().generic_visit(node)
        self.features.ast_depth -= 1


class PythonAnalyzer(BaseAnalyzer):
    def analyze(self, code: str) -> ExtractedFeatures:
        try:
            tree = ast.parse(code)
            visitor = FeatureExtractionVisitor()
            visitor.visit(tree)
            return visitor.features
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {e}")
