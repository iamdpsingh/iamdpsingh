import re
import sys

svg = open("gitartwork.svg").read()

# Find all blocks with class="o c cX"
# They look like: <rect ... x="13" y="90" ... class="o c c6"></rect>
# Wait, the x coordinate inside <rect> is what matters!
# Let's see the unique x coordinates for colored blocks:
xs = set()
for match in re.finditer(r'x="(\d+)"[^>]*class="o c c', svg):
    xs.add(int(match.group(1)))

print("Colored X columns:", sorted(xs))
