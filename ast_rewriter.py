import ast
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
                            )
                        ],
                        keywords=[]
                    )
                )
                hooks.append(hook)
        if hooks:
            return [node] + hooks
        return node
def rewrite_source(source_code):
    """
        Parse and rewrite Python source code.
    """
    tree = ast.parse(source_code)
    rewriter = ASTRewriter()
    new_tree = rewriter.visit(tree)
    ast.fix_missing_locations(new_tree)
    return ast.unparse(new_tree)
def rewrite_file(input_file, output_file):
    """
        Read original Python file,
    rewrite it using AST,
    and save the rewritten code.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        source_code = file.read()
    rewritten_code = rewrite_source(source_code)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(rewritten_code)
if __name__ == "__main__":
    input_file = "test_target.py"
    output_file = "rewritten_target.py"
    rewrite_file(input_file, output_file)
    print("AST rewriting completed!")
    print("Output file:", output_file)