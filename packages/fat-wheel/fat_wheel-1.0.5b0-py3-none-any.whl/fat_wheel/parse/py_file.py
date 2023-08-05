import ast

ignore_setup_options = ["install_requires", "extra_requires", "packages"]


def get_py_file_meta_data(py_file_path):

    def create_py_object(node_to_traverse, current_object):
        for node in node_to_traverse.body:
            if isinstance(node, ast.Expr):
                is_setup = node.value.func.id == "setup"
                if is_setup:
                    for params in node.value.keywords:
                        option = params.arg
                        value = params.value
                        if option not in ignore_setup_options:
                            if isinstance(value, ast.Str):
                                current_object.append([option, value.s, "str"])
                            elif isinstance(value, ast.NameConstant):
                                current_object.append([option, value.value, "bool"])
                            elif isinstance(value, ast.List):
                                print(value)
                        # else:
                        #     node.value.keywords.remove(params)

        return node_to_traverse

    file = open(py_file_path, "r")
    f = file.read()
    node_to_traverse = ast.parse(f)
    py_file_structure = []
    create_py_object(node_to_traverse, py_file_structure)
    return py_file_structure