import re

with open('scratch/restored_game_engine.js', 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Strip line numbers if present (e.g. "12: 1404: ...")
cleaned_lines = []
for line in raw_text.splitlines():
    sub = re.sub(r'^\d+:\s*(\d+:\s*)?', '', line)
    cleaned_lines.append(sub)

clean_block = '\n'.join(cleaned_lines)

# Now read index.html and insert clean_block before PattyController
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

patty_marker = '// ==========================================\n        // 11. MÁQUINA DE ESTADOS DA CARNE'
if patty_marker in html:
    html = html.replace(patty_marker, clean_block + '\n\n        ' + patty_marker)
    print("Reinserted GameEngine block before PattyController successfully.")
else:
    print("Could not find patty_marker in index.html!")

# Update createRecipeBoard position to fit wall between shelves
old_recipe_pos = 'recipeBoardMesh.position.set(0.0, 1.68, -1.87);'
new_recipe_pos = 'recipeBoardMesh.position.set(0.0, 1.75, -1.87);'
html = html.replace(old_recipe_pos, new_recipe_pos)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html update complete.")
