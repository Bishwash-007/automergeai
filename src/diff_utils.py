import difflib
import re

def get_diff(a, b):
    a_lines = a.splitlines() if a else []
    b_lines = b.splitlines() if b else []
    diff = list(difflib.unified_diff(a_lines, b_lines, lineterm=''))
    return "\n".join([
        line for line in diff
        if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))
    ])

def extract_changed_lines_from_patch(patch):
    lines = patch.splitlines()
    changed = []
    for line in lines:
        if line.startswith('+') and not line.startswith('+++'):
            changed.append(line)
        elif line.startswith('-') and not line.startswith('---'):
            changed.append(line)
    return '\n'.join(changed)

def extract_conflict_blocks(content):
    pattern = re.compile(r"<<<<<<<.*?\n(.*?)=======\n(.*?)>>>>>>>.*?\n", re.DOTALL)
    matches = pattern.findall(content)
    return [f"<<<<<<<\n{left}=======\n{right}>>>>>>>" for left, right in matches]