import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# 1. Floor Stove Correction (fogao.glb)
if 'placeStoveOnFloor(cooktop, -1.15, -0.55, COUNTER_TOP_Y)' not in html:
    errors.append("fogao.glb is not placed on floor with placeStoveOnFloor.")

# 2. Knife and Ingredients Spacing
if 'placeOnSurface(facaCozinhar, 1.22, LEVEL_1_Y' not in html or 'placeOnSurface(facaSimples, 1.34, LEVEL_1_Y' not in html:
    errors.append("Knife removal from bread / flat placement on counter missing.")

if "'bottom-pao': { x: 0.68, z: -0.60" not in html or "'burger-top': { x: 1.02, z: -0.60" not in html:
    errors.append("Side-by-side ingredient spacing on cutting board missing.")

# 3. Skillet and Accoutrements Alignment
if 'placeOnSurface(skilletMesh, -1.15, stoveTopY + 0.003, -0.55, 0.38)' not in html:
    errors.append("Skillet placement on stove burner missing.")

if 'placeOnSurface(toasterMesh, 1.40, LEVEL_1_Y, -0.88' not in html:
    errors.append("Straight line back edge alignment at Z=-0.88 missing.")

if 'placeOnSurface(espatulaMesh, -0.60, LEVEL_1_Y, -0.50' not in html:
    errors.append("Spatula placement between stove and center plate missing.")

print("=== VERIFICATION RESULTS ===")
if errors:
    print("ERRORS FOUND:")
    for err in errors:
        print(" -", err)
    sys.exit(1)
else:
    print("SUCCESS: All floor stove, knife removal, ingredient spacing, and alignment requirements verified!")
