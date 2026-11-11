import re
import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script type="module">(.*?)</script>', html, re.DOTALL)
if m:
    js = m.group(1)
    with open('scratch/inline_script.js', 'w', encoding='utf-8') as f_out:
        f_out.write(js)
    print("JS extracted successfully. Size:", len(js))
else:
    print("Script tag not found!")
