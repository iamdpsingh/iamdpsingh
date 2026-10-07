import re

svg = open("gitartwork.svg").read()

cols = set()
for g in re.finditer(r'<g transform="translate\((\d+),\s*0\)">', svg):
    x_offset = int(g.group(1))
    
    # get the content inside this <g>
    content = svg[g.end():svg.find('</g>', g.end())]
    
    # check if there is any colored rect inside this g
    if 'class="o c c' in content:
        cols.add(x_offset)

print("Colored columns:", sorted(cols))
