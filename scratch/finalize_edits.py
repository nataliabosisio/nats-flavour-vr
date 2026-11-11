import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update GameEngine assemblyHeight assignments
content = content.replace("this.assemblyHeight = 0.9320;", "this.assemblyHeight = window.plateSurfaceTopY || 0.9320;")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated assemblyHeight assignments in index.html.")
