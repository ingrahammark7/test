import re
from collections import Counter

# Files to scan
files = ["pen.py", "nuct.py"]

# Patterns for explicit units in variable names or constants
unit_patterns = [
    r'\bcm\b', r'\bkg\b', r'\bm3\b', r'\bs\b', r'\bJ\b', r'\bev\b', r'\bm\b',
    r'\b\d+e[+-]?\d+\b',            # scientific notation numbers (could indicate conversion)
    r'/[a-zA-Z_][a-zA-Z0-9_]*',     # division by a variable
    r'\*\*-\d',                      # negative exponent (reciprocal units)
    r'\*\*2', r'\*\*3',              # powers of 2 or 3 → derived units (m², m³, etc.)
]

counter = Counter()

for fname in files:
    with open(fname) as f:
        text = f.read()
        for pat in unit_patterns:
            matches = re.findall(pat, text)
            counter[pat] += len(matches)

# Sort by frequency
print("Unit usage frequency:")
for pat, count in counter.most_common():
    print(f"{pat:15s} {count}")