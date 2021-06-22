import os
from node_definitions import IntegerNode, VarRef, CallNode, DefNode


class Generator:
    def __init__(self):
        pass

    def generate(self, node):
        if isinstance(node, int):
            return f"{node}"
        if isinstance(node, IntegerNode):
            return f"{node.value}"
        if isinstance(node, VarRef):
            return f"{node.value}"
        if isinstance(node, CallNode):
            args = [self.generate(expression) for expression in node.arg_expressions]
            return f"{node.name}({','.join(args)})"
        if isinstance(node, DefNode):
            return f"def {node.name}({','.join(node.arg_names)}): return {self.generate(node.body)}"
        raise RuntimeError(f"Unexpected ndoe type: {type(node)}")

    @staticmethod
    def write_code_to_working_directory(code, file_path):
        with open(os.getcwd() + f"/outputs/{file_path}", "w") as file:
            file.write(code)
