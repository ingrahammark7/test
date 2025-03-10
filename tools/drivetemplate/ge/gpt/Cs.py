import re
import os
import ast
import textwrap

def split_game_txt(input_file="game.txt"):
    """Splits game.txt into individual Python files based on class names."""
    try:
        with open(input_file, "r") as file:
            content = file.read()

        # Split by separator
        sections = content.split("media_rw")
        class_content_map = {}

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Extract class name
            match = re.search(r"class\s+(\w+)", section)
            if match:
                class_name = match.group(1)
                if class_name not in class_content_map:
                    class_content_map[class_name] = section
                else:
                    class_content_map[class_name] += "\n\n" + section
            else:
                if class_content_map:
                    last_class = list(class_content_map.keys())[-1]
                    class_content_map[last_class] += "\n\n" + section

        # Write each class to its own .py file
        for class_name, content in class_content_map.items():
            with open(f"{class_name}.py", "w") as py_file:
                py_file.write(content)
            print(f"Created: {class_name}.py")

        print("Splitting completed.")
    except Exception as e:
        print(f"An error occurred during splitting: {e}")

def rebuild_game_txt(output_file="game.txt"):
    """Rebuilds game.txt by concatenating all .py files in the current directory."""
    try:
        py_files = [f for f in os.listdir() if f.endswith(".py")]
        with open(output_file, "w") as game_file:
            for py_file in py_files:
                with open(py_file, "r") as file:
                    content = file.read()
                    game_file.write("media_rw\n")
                    game_file.write(content.strip() + "\n")
        print(f"{output_file} successfully rebuilt from .py files.")
    except Exception as e:
        print(f"An error occurred during rebuilding: {e}")

def validate_snippet(snippet):
    """Validates the syntax of a code snippet using Python's AST module."""
    try:
        dedented_snippet = textwrap.dedent(snippet)  # Remove unnecessary indentation
        ast.parse(dedented_snippet)
        print("Snippet is syntactically valid.")
        return True
    except SyntaxError as e:
        print(f"Syntax error in snippet: {e}")
        print("Snippet content:")
        print(snippet)
        return False

def modify_file_from_temp(temp_file="temp.txt"):
    """Modifies a .py file based on instructions from temp.txt."""
    try:
        with open(temp_file, "r") as file:
            lines = file.readlines()

        filename = lines[0].strip()
        start_line = int(lines[1].strip())
        end_line = int(lines[2].strip())
        snippet = "".join(lines[3:])

        # Validate the snippet syntax before applying
        if not validate_snippet(snippet):
            print("Modification aborted due to invalid syntax in snippet.")
            return

        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return

        # Ensure the specified line range is valid
        with open(filename, "r") as file:
            file_contents = file.readlines()
        if start_line > len(file_contents) or end_line > len(file_contents) + 1:
            print(f"Invalid line range: {start_line}-{end_line}. File has {len(file_contents)} lines.")
            return

        # Create a backup of the file
        backup_filename = f"{filename}.bak"
        os.rename(filename, backup_filename)
        print(f"Backup created: {backup_filename}")

        # Apply modification
        modified_contents = (
            file_contents[:start_line - 1] + file_contents[end_line:]  # Remove specified lines
        )
        modified_contents.insert(start_line - 1, snippet)  # Insert new snippet

        with open(filename, "w") as file:
            file.writelines(modified_contents)
        print(f"{filename} successfully modified.")
    except Exception as e:
        print(f"An error occurred during modification: {e}")

def generate_temp_snippet(filename, start_line, end_line, new_code):
    """Dynamically generates temp.txt based on the parameters provided."""
    try:
        temp_content = f"{filename}\n{start_line}\n{end_line}\n{new_code}"
        with open("temp.txt", "w") as temp_file:
            temp_file.write(temp_content)
        print("Generated temp.txt with the following content:")
        print(temp_content)
    except Exception as e:
        print(f"An error occurred during temp.txt generation: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage game.txt and Python files.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Split command
    split_parser = subparsers.add_parser("split", help="Split game.txt into individual .py files.")
    split_parser.add_argument("--input", type=str, default="game.txt", help="Path to game.txt")

    # Rebuild command
    rebuild_parser = subparsers.add_parser("rebuild", help="Rebuild game.txt from .py files.")
    rebuild_parser.add_argument("--output", type=str, default="game.txt", help="Path to output game.txt")

    # Modify command
    modify_parser = subparsers.add_parser("modify", help="Modify a .py file based on temp.txt.")
    modify_parser.add_argument("--temp", type=str, default="temp.txt", help="Path to temp.txt")

    # Generate temp.txt command
    generate_parser = subparsers.add_parser("generate", help="Generate a temp.txt snippet.")
    generate_parser.add_argument("--filename", type=str, required=True, help="Target filename to modify")
    generate_parser.add_argument("--start", type=int, required=True, help="Start line number")
    generate_parser.add_argument("--end", type=int, required=True, help="End line number")
    generate_parser.add_argument("--code", type=str, required=True, help="Code to insert at start line")

    args = parser.parse_args()

    if args.command == "split":
        split_game_txt(input_file=args.input)
    elif args.command == "rebuild":
        rebuild_game_txt(output_file=args.output)
    elif args.command == "modify":
        modify_file_from_temp(temp_file=args.temp)
    elif args.command == "generate":
        generate_temp_snippet(args.filename, args.start, args.end, args.code)

    # Automatically rebuild game.txt after every run
    rebuild_game_txt()
