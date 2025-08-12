import re

def fix_indentation(filename, indent='    '):  # indent defaults to 4 spaces
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        # Remove leading whitespace and re-indent with the desired indent size
        stripped_line = line.lstrip('\t ').rstrip('\n')
        leading_whitespace = line[:len(line) - len(line.lstrip())]

        # Count indentation levels assuming tabs or 4 spaces = 1 indent level
        # Convert tabs to spaces assuming tab = 4 spaces
        space_equiv = leading_whitespace.replace('\t', '    ')

        # Calculate indent level by dividing spaces by 4
        indent_level = len(space_equiv) // 4

        # Create new indent with indent_level times the indent string
        new_indent = indent * indent_level

        fixed_lines.append(new_indent + stripped_line + '\n')

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print(f'Indentation fixed and enforced in {filename}')

if __name__ == '__main__':
    fix_indentation('pen.py')