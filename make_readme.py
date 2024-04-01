import ast

def parse_docstring(docstring):
    """
    Parse the docstring to extract and format description, parameters, returns sections,
    and format examples as code blocks.
    """
    if not docstring:
        return "No documentation available."

    lines = docstring.split('\n')
    description, params, returns, example_block = [], [], [], []
    current_section = description

    for line in lines:
        if line.startswith(':param'):
            current_section = params
            line = line.replace(':param', '').strip()
            line = f"- {line}"
        elif line.startswith(':return:'):
            current_section = returns
            line = line.replace(':return:', '').strip()
            line = f"- {line}"
        elif line.strip().startswith('>>>') or (example_block and not line.strip().startswith(':')):
            # This line is part of an example or subsequent line of an example block
            current_section = example_block
        current_section.append(line)

    # Format sections
    formatted_docstring = ""
    if description: formatted_docstring += '\n'.join(description) + '\n\n'
    if params: formatted_docstring += "#### Parameters:\n" + '\n'.join(params) + '\n\n'
    if returns: formatted_docstring += "#### Returns:\n" + '\n'.join(returns) + '\n\n'
    if example_block:
        formatted_example = "#### Example:\n" + "```python\n" + '\n'.join(example_block) + "\n```\n"
        formatted_docstring += formatted_example

    return formatted_docstring

def generate_markdown_documentation(file_path, output_file='README.md'):
    with open(file_path, 'r') as file:
        source_code = file.read()

    module = ast.parse(source_code)
    module_docstring = ast.get_docstring(module)
    documentation = "# LobbyView Package Documentation\n\n"
    if module_docstring:
        documentation += f"{module_docstring}\n\n"

    for node in ast.iter_child_nodes(module):
        if isinstance(node, ast.ClassDef):
            class_docstring = ast.get_docstring(node)
            documentation += f"## Class: {node.name}\n\n"
            if class_docstring:
                documentation += f"{parse_docstring(class_docstring)}\n"
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_docstring = ast.get_docstring(child)
                    if method_docstring:
                        documentation += f"### Method: {child.name}\n\n"
                        documentation += f"{parse_docstring(method_docstring)}\n"

    with open(output_file, 'w') as md_file:
        md_file.write(documentation)

# Correct path to the uploaded file
file_path = 'src/lobbyview/LobbyView.py'  # Adjust the file path as necessary
generate_markdown_documentation(file_path)

print(f"LobbyView Package Documentation has been successfully generated and written to README.md")
