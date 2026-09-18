import ast
import json
class ASTRewriter(ast.NodeTransformer):
    def visit_Assign(self, node):
        self.generic_visit(node)
        hooks = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                hook = ast.Expr(
                    value=ast.Call(
                        func=ast.Name(
                            id="capture_state",
                            ctx=ast.Load()
                        ),
                        args=[
                            ast.Constant(value=variable_name),
                            ast.Name(
                                id=variable_name,
                                ctx=ast.Load()
                            ),
                            ast.Constant(value=node.lineno)
                        ],
                        keywords=[]
                    )
                )

                hook.lineno = node.lineno
                hook.col_offset = node.col_offset

                hooks.append(hook)
        if hooks:
            return [node] + hooks
        return node
def rewrite_source(source_code):
    tree = ast.parse(source_code)
    rewriter = ASTRewriter()
    new_tree = rewriter.visit(tree)
    ast.fix_missing_locations(new_tree)
    return ast.unparse(new_tree)
def analyze_code(source_code):
    tree = ast.parse(source_code)
    assignments = []
    variables = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_name = target.id
                    if variable_name in variables:
                        assignment_type = "update"
                    else:
                        assignment_type = "new assignment"
                        variables.add(variable_name)
                    assignments.append({
                        "variable_name": variable_name,
                        "line_number": node.lineno,
                        "assignment_type": assignment_type
                    })
    return assignments
if __name__ == "__main__":
    source_code = """x = 10
x = 20
y = x + 5"""
    print("Assignment Information:")
    print(json.dumps(analyze_code(source_code), indent=4))
    print("\nInstrumented Code:")
    print(rewrite_source(source_code))