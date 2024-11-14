import os
from pathlib import Path
import re
import ast
import argparse

def read_rst_file(file_path):
    """Read and return content of an RST file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_module_description(intro_content):
    """Extract the complete introduction including features but excluding example usage."""
    # First split to get relevant content
    content = intro_content.split('Example Usage')[0]  # Stop at Example Usage section
    
    # Clean up RST formatting
    content = content.replace('Introduction\n============\n', '')
    content = content.replace('.. code-block:: python\n', '')
    content = content.replace('.. code-block:: text\n', '')
    content = content.replace('.. code-block::', '')
    
    # Split content into sections
    sections = content.split('\n\n')
    
    # Process each section
    processed_sections = []
    for section in sections:
        # Skip empty sections
        if not section.strip():
            continue
            
        # Clean up section
        section = section.replace('--------\n', '')
        section = section.replace('Getting Started\n', '## Getting Started\n')
        section = section.replace('Features\n', '## Features\n')
        
        # Clean up feature bullet points
        if '**' in section:
            lines = section.split('\n')
            cleaned_lines = []
            for line in lines:
                if line.strip().startswith('**'):
                    line = '- ' + line.replace('**', '')
                cleaned_lines.append(line)
            section = '\n'.join(cleaned_lines)
            
        processed_sections.append(section)
    
    return '\n\n'.join(processed_sections)

def extract_registration_info(registration_content):
    """Extract registration instructions from registration.rst."""
    # Remove the header and everything after citation
    content = registration_content.split('To cite LobbyView')[0]
    content = content.replace('Registration\n============\n', '')
    
    # Clean up code block formatting
    content = content.replace('.. code-block:: text\n\n', '')
    content = content.replace('.. code-block:: python\n\n', '')
    content = content.replace('For Unix/Linux (includes MacOS):', '**For Unix/Linux (includes MacOS):**')
    content = content.replace('For Windows:', '**For Windows:**')
    
    # Keep only the registration steps and contact info
    content = content.strip()
    return content

def clean_code_example(text):
    """Clean up code example formatting."""
    # Remove RST code block indicators
    text = text.replace('.. code-block:: python\n\n', '')
    text = text.replace('.. code-block:: text\n\n', '')
    
    # Fix code block formatting
    lines = text.split('\n')
    clean_lines = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Start code block
        if stripped.startswith('>>>'):
            if not in_code_block:
                clean_lines.append('```python')
                in_code_block = True
            clean_lines.append(line)
        # Handle code block content
        elif in_code_block and stripped:
            clean_lines.append(line)
        # End code block on empty line if in code block
        elif in_code_block and not stripped:
            clean_lines.append('```')
            clean_lines.append('')
            in_code_block = False
        # Normal line
        else:
            clean_lines.append(line)
    
    # Close any open code block
    if in_code_block:
        clean_lines.append('```')
    
    return '\n'.join(clean_lines)

def parse_docstring(docstring):
    """Parse a method's docstring to extract description, parameters, and examples."""
    if not docstring:
        return "", [], []
    
    lines = docstring.split('\n')
    description = []
    parameters = []
    examples = []
    current_section = description
    example_content = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Handle parameter documentation
        if stripped_line.startswith(':param'):
            current_section = parameters
            # Remove :param and type information, keep only parameter name and description
            param_parts = stripped_line.split(':', 2)
            if len(param_parts) >= 3:
                param_name = param_parts[1].strip()
                param_desc = param_parts[2].strip()
                parameters.append(f"- `{param_name}`: {param_desc}")
            continue
        # Handle return documentation
        elif stripped_line.startswith(':return'):
            continue
        # Handle examples
        elif '>>>' in stripped_line:
            if example_content and '>>>' in stripped_line:
                # If we find a new example and already have content, close the previous one
                examples.extend(example_content)
                example_content = []
            if not example_content:
                example_content.append('```python')
            example_content.append(stripped_line)
        # Continue example if we're in one
        elif example_content and stripped_line:
            example_content.append(stripped_line)
        # Close example if we hit an empty line
        elif example_content and not stripped_line:
            example_content.append('```')
            examples.extend(example_content)
            example_content = []
        # Regular description line
        elif stripped_line and current_section == description:
            description.append(stripped_line)
    
    # Close any open example block
    if example_content:
        example_content.append('```')
        examples.extend(example_content)
    
    return (
        ' '.join(description).strip(),
        parameters,
        examples
    )

def format_method_documentation():
    """Extract method documentation directly from source code."""
    # Path to your main module file
    module_path = Path('src/lobbyview/LobbyView.py')
    
    with open(module_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    module = ast.parse(source)
    
    # Find the LobbyView class
    lobbyview_class = None
    for node in ast.walk(module):
        if isinstance(node, ast.ClassDef) and node.name == 'LobbyView':
            lobbyview_class = node
            break
    
    if not lobbyview_class:
        return ""
    
    # Core methods we want to document
    core_methods = [
        'legislators', 'bills', 'clients', 'reports', 'issues', 
        'networks', 'texts', 'quarter_level_networks', 'bill_client_networks'
    ]
    
    method_docs = []
    
    for node in lobbyview_class.body:
        if isinstance(node, ast.FunctionDef) and node.name in core_methods:
            docstring = ast.get_docstring(node)
            if docstring:
                description, params, examples = parse_docstring(docstring)
                
                # Format the method documentation
                method_doc = [f"### Method: {node.name}\n"]
                if description:
                    method_doc.append(description + "\n")
                if params:
                    method_doc.append("#### Parameters:")
                    method_doc.extend(params)
                    method_doc.append("")
                if examples:
                    method_doc.append("#### Example:")
                    method_doc.extend(examples)
                
                method_docs.append('\n'.join(method_doc))
    
    return '\n\n'.join(method_docs)

def get_overview_content():
    """Return the overview content for the README."""
    return """This module provides a Python interface to the LobbyView REST API. It uses the same endpoints and parameter names as outlined in the LobbyView REST API Documentation (https://rest-api.lobbyview.org/).

The full documentation for the package is linked here: http://lobbyview.readthedocs.io/

Note: This repo is pre-release and our expected time table is December 2024 for a release that's ready for widespread public use."""

def generate_readme():
    """Generate README.md from Sphinx documentation and source code."""
    docs_path = Path('docs/source')
    
    # Read source files
    intro_content = read_rst_file(docs_path / 'introduction.rst')
    registration_content = read_rst_file(docs_path / 'registration.rst')
    
    # Generate API documentation from source
    api_content = format_method_documentation()
    
    readme_content = [
        "# LobbyView Package Documentation",
        "",
        "![Tests](https://github.com/lobbyview/LobbyViewPythonPackage/actions/workflows/python-package.yml/badge.svg)",
        "![Coverage](https://raw.githubusercontent.com/lobbyview/LobbyViewPythonPackage/main/coverage-badge.svg)",
        "![PyPI Downloads](https://raw.githubusercontent.com/lobbyview/LobbyViewPythonPackage/main/download-badge.svg)",
        "",
        get_overview_content(),  # Add the overview content here
        "",
        extract_module_description(intro_content),
        "",
        "# Registration",
        "",
        extract_registration_info(registration_content),
        "",
        "# Classes and Methods",
        "",
        "## Class: LobbyView",
        "",
        "Main class for interacting with the LobbyView API.",
        "",
        api_content
    ]
    
    # Write README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_content))

def verify_sphinx_files():
    """Verify that all required Sphinx files exist."""
    required_files = [
        'docs/source/introduction.rst',
        'docs/source/registration.rst',
        'docs/source/api.rst'
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        raise FileNotFoundError(f"Missing required files: {', '.join(missing_files)}")

def generate_test_readme():
    """Generate README to a test file for review."""
    # Store current README content for comparison
    current_readme = Path('README.md')
    if current_readme.exists():
        backup = current_readme.read_text(encoding='utf-8')
    
    # Generate new README content
    generate_readme()
    
    # Move new content to test file
    Path('README.md').rename('READMEnew.md')
    
    # Restore original README
    if 'backup' in locals():
        current_readme.write_text(backup, encoding='utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate README from Sphinx documentation')
    parser.add_argument('--test', action='store_true', 
                      help='Generate test README as README.md.new without replacing current README')
    args = parser.parse_args()
    
    try:
        print("Current working directory:", os.getcwd())
        print("Checking for required files...")
        for file in ['docs/source/introduction.rst', 'docs/source/registration.rst', 'docs/source/api.rst']:
            exists = os.path.exists(file)
            print(f"  {file}: {'Found' if exists else 'Not found'}")
        
        verify_sphinx_files()
        if args.test:
            print("Generating test README...")
            generate_test_readme()
        else:
            print("Generating README...")
            generate_readme()
        print("Done!")
    except Exception as e:
        print(f"Error generating README: {str(e)}")
        exit(1)