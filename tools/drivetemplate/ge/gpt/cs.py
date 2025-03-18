import re
import os

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

def combine_files(input1, input2, output):
    """
    Combines the contents of two input files into a single output file.

    Args:
        input1 (str): Path to the first input file.
        input2 (str): Path to the second input file.
        output (str): Path to the output file.
    """
    try:
        with open(input1, 'r') as file1, open(input2, 'r') as file2, open(output, 'w') as outfile:
            # Write contents of the first file
            outfile.write(file1.read())
            outfile.write("\n")  # Add a newline between the two files
            
            # Write contents of the second file
            outfile.write(file2.read())
        
        print(f"Successfully combined {input1} and {input2} into {output}.")
    except Exception as e:
        print(f"An error occurred: {e}")

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

    # Combine command
    combine_parser = subparsers.add_parser("combine", help="Combine two files into one.")
    combine_parser.add_argument("--input1", type=str, required=True, help="Path to the first input file")
    combine_parser.add_argument("--input2", type=str, required=True, help="Path to the second input file")
    combine_parser.add_argument("--output", type=str, default="combined.txt", help="Path to the output file")

    args = parser.parse_args()

    if args.command == "split":
        split_game_txt(input_file=args.input)
    elif args.command == "rebuild":
        rebuild_game_txt(output_file=args.output)
    elif args.command == "combine":
        combine_files(input1=args.input1, input2=args.input2, output=args.output)

    # Automatically rebuild game.txt after every run
    rebuild_game_txt()