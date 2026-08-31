import javalang
from app.analyzers.base_analyzer import BaseAnalyzer
from app.features.feature_schema import ExtractedFeatures

class JavaAnalyzer(BaseAnalyzer):
    def analyze(self, code: str) -> ExtractedFeatures:
        features = ExtractedFeatures()
        
        try:
            # Often Java code given might just be a method snippet. 
            # javalang requires a full class definition to parse. 
            # If parsing fails, we'll try wrapping it in a dummy class.
            try:
                tree = javalang.parse.parse(code)
            except javalang.parser.JavaSyntaxError:
                dummy_code = f"public class DummyClass {{\n public void dummyMethod() {{\n {code} \n}}\n}}"
                tree = javalang.parse.parse(dummy_code)
        except Exception as e:
            raise ValueError(f"Invalid Java code: {e}")

        # Basic sets to track current context
        defined_methods = set()
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            defined_methods.add(node.name)
            features.method_count += 1
            features.function_count += 1

        def traverse(node, current_loop_depth=0):
            features.statement_count += 1
            features.ast_depth += 1

            next_loop_depth = current_loop_depth

            if isinstance(node, javalang.tree.ForStatement):
                features.for_loop_count += 1
                features.loop_count += 1
                next_loop_depth += 1
                features.max_loop_depth = max(features.max_loop_depth, next_loop_depth)
                if next_loop_depth > 1:
                    features.nested_loop_count += 1
                
                # Assume linear for simplicity
                features.linear_loop_count += 1
                
            elif isinstance(node, javalang.tree.WhileStatement) or isinstance(node, javalang.tree.DoStatement):
                features.while_loop_count += 1
                features.loop_count += 1
                next_loop_depth += 1
                features.max_loop_depth = max(features.max_loop_depth, next_loop_depth)
                if next_loop_depth > 1:
                    features.nested_loop_count += 1
                
                # Simple check for logarithmic behavior in while (e.g., node containing *= or /=)
                is_log = False
                # Just a very simple heuristic: convert node to string and check
                if "*=" in str(node) or "/=" in str(node):
                    is_log = True
                
                if is_log:
                    features.logarithmic_loop_count += 1
                else:
                    features.linear_loop_count += 1

            elif isinstance(node, javalang.tree.IfStatement):
                features.if_count += 1
                features.condition_count += 1

            elif isinstance(node, javalang.tree.MethodInvocation):
                features.function_call_count += 1
                if node.member in defined_methods:
                    features.recursive = True
                    features.recursive_call_count += 1

            # Recursively visit children
            if hasattr(node, 'children'):
                for child in node.children:
                    if isinstance(child, javalang.tree.Node):
                        traverse(child, next_loop_depth)
                    elif isinstance(child, list):
                        for item in child:
                            if isinstance(item, javalang.tree.Node):
                                traverse(item, next_loop_depth)
            
            features.ast_depth -= 1

        traverse(tree)
        return features
