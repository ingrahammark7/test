#!/usr/bin/env python3
import sys
import os
import re
import textwrap
import ast
import astunparse  # Install with: pip install astunparse
import subprocess  # To execute the bash command

def split_game_txt(input_file="game.txt"):
    """Splits game.txt into individual Python files based on class definitions."""
    try:
        with open(input_file, "r") as f:
            content = f.read()
        sections = content.split("media_rw")
        class_content_map = {}
        for section in sections:
            section = section.strip()
            if not section:
                continue
            match = re.search(r"class\s+(\w+)", section)
            if match:
                class_name = match.group(1)
                class_content_map[class_name] = section
            else:
                if class_content_map:
                    last_class = list(class_content_map.keys())[-1]
                    class_content_map[last_class] += "\n\n" + section
        for class_name, content in class_content_map.items():
            with open(f"{class_name}.py", "w") as pyfile:
                pyfile.write(content)
            print(f"Created: {class_name}.py")
        print("Splitting completed.")
    except Exception as e:
        print(f"An error occurred during splitting: {e}")

def rebuild_game_txt(output_file="game.txt"):
    """Rebuilds game.txt by concatenating all .py files in the current directory."""
    try:
        py_files = [f for f in os.listdir() if f.endswith(".py")]
        with open(output_file, "w") as outfile:
            for py_file in py_files:
                with open(py_file, "r") as f:
                    content = f.read()
                    outfile.write("media_rw\n")
                    outfile.write(content.strip() + "\n")
        print(f"{output_file} successfully rebuilt from .py files.")
    except Exception as e:
        print(f"An error occurred during rebuilding: {e}")

def combine_files(input1, input2, output):
    """
    Combines two Python files into one output file.

    A fake class wrapper ("class Foo:") is added to temp2.txt if necessary
    to ensure proper AST parsing. After merging, the fake class is removed
    entirely from the final result using a bash command.

    Args:
        input1 (str): Path to the first input file (e.g., temp1.txt).
        input2 (str): Path to the second input file (e.g., temp2.txt).
        output (str): Path for the output file (e.g., result.txt).
    """
    if not os.path.exists(input1) or not os.path.exists(input2):
        print(f"Error: One or both input files do not exist.")
        return

    try:
        # Normalize both input files for consistent indentation
        norm1 = normalize_indentation(input1)
        norm2 = normalize_indentation(input2)

        # Add a fake wrapper to temp2.txt if needed
        tree2 = parse_with_fake_wrapper(norm2, input2)
        tree1 = ast.parse(norm1, filename=input1)

        # Merge the trees
        merged_tree = merge_ast(tree1, tree2)

        # Convert the merged AST back to Python code
        merged_code = astunparse.unparse(merged_tree)

        # Write the merged code to the output file
        with open(output, "w") as out:
            out.write(merged_code)

        # Run a bash command to remove any line containing "foo" or "Foo"
        remove_lines_with_foo(output)

        print(f"Successfully combined '{input1}' and '{input2}' into '{output}'.")
    except Exception as e:
        print(f"An error occurred during combination: {e}")

def normalize_indentation(file_path):
    """
    Reads a file and ensures consistent 4-space indentation.

    Args:
        file_path (str): Path to the file to normalize.

    Returns:
        str: The normalized file content as a string.
    """
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        # Replace tabs with 4 spaces and remove trailing whitespace.
        norm_lines = [line.replace("\t", "    ").rstrip() for line in lines]
        return "\n".join(norm_lines)
    except Exception as e:
        raise RuntimeError(f"Failed to normalize indentation for {file_path}: {e}")

def parse_with_fake_wrapper(content, filename):
    """
    Ensures the content of the second file is parsable by wrapping it in a fake class
    if necessary.

    Args:
        content (str): The file content as a string.
        filename (str): The file name for reference.

    Returns:
        ast.Module: The parsed AST, with a fake wrapper if applied.
    """
    stripped_content = content.lstrip()
    if stripped_content and not stripped_content.startswith(" "):
        # Add a fake wrapper to ensure proper indentation for parsing
        wrapped_content = "class Foo:\n" + "\n".join("    " + line for line in content.splitlines())
        tree_with_wrapper = ast.parse(wrapped_content, filename=filename)
        print("Applied fake class wrapper to ensure parsing of input2.")
        return tree_with_wrapper
    return ast.parse(content, filename=filename)

def remove_lines_with_foo(file_path):
    """
    Removes any line containing "foo" or "Foo" (case-insensitive) using a bash command.

    Args:
        file_path (str): Path to the file to modify.
    """
    try:
        command = f"sed -i '/[Ff][Oo][Oo]/d' {file_path}"
        subprocess.run(command, shell=True, check=True)
        print("Removed all lines containing 'foo' or 'Foo' from the result file.")
    except Exception as e:
        raise RuntimeError(f"Failed to remove lines containing 'foo' or 'Foo' from {file_path}: {e}")

def merge_ast(tree1, tree2):
    """
    Merges two ASTs by appending elements from tree2 into tree1.

    If tree2 contains function definitions (methods) and tree1 ends with a class,
    those functions are appended to the body of the last class in tree1.

    Args:
        tree1 (ast.Module): The AST of the first file.
        tree2 (ast.Module): The AST of the second file.

    Returns:
        ast.Module: The merged AST.
    """
    if not isinstance(tree1, ast.Module) or not isinstance(tree2, ast.Module):
        raise ValueError("Both ASTs must be ast.Module instances.")

    body1 = tree1.body
    body2 = tree2.body

    # If the last element of tree1 is a class definition, append functions from tree2 to it.
    if body1 and isinstance(body1[-1], ast.ClassDef):
        class_node = body1[-1]
        for node in body2:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                class_node.body.append(node)
            else:
                body1.append(node)
    else:
        body1.extend(body2)

    return tree1

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage game.txt and Python files.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Split command
    split_parser = subparsers.add_parser("split", help="Split game.txt into individual .py files.")
    split_parser.add_argument("--input", type=str, default="game.txt", help="Path to game.txt")

    # Rebuild command
    rebuild_parser = subparsers.add_parser("rebuild", help="Rebuild game.txt from the individual .py files.")
    rebuild_parser.add_argument("--output", type=str, default="game.txt", help="Output path for game.txt")

    # Combine command
    combine_parser = subparsers.add_parser("combine", help="Combine two files into one result file.")
    combine_parser.add_argument("--input1", type=str, required=True, help="Path to the first input file (e.g., temp1.txt)")
    combine_parser.add_argument("--input2", type=str, required=True, help="Path to the second input file (e.g., temp2.txt)")
    combine_parser.add_argument("--output", type=str, default="result.txt", help="Output file path (e.g., result.txt)")

    args = parser.parse_args()
    if args.command == "split":
        split_game_txt(input_file=args.input)
    elif args.command == "rebuild":
        rebuild_game_txt(output_file=args.output)
    elif args.command == "combine":
        combine_files(args.input1, args.input2, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
