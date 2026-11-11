import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = []
warnings = []

# 1. Check L-Shape bench top implementation
if 'topShape = new THREE.Shape()' not in html or 'ExtrudeGeometry(topShape' not in html:
    errors.append("Counter top L-shape extrusion not found.")

if 'COUNTER_TOP_Y = 0.9100' not in html:
    errors.append("COUNTER_TOP_Y constant not found or incorrect.")

# 2. Check Stove loading & alignment
if "'fogao.glb'" not in html:
    errors.append("fogao.glb not in asset list.")

if 'placeOnSurface(cooktop, -1.15, COUNTER_TOP_Y + 0.005' not in html:
    errors.append("Stove not placed with +0.005 offset on counter top.")

if 'placeOnSurface(skilletMesh, -1.15, stoveTopY + 0.003' not in html:
    errors.append("Skillet not aligned to stove burners.")

if 'placeOnSurface(meatTray, -1.55, LEVEL_1_Y' not in html:
    errors.append("Meat tray not placed on counter left of stove.")

# 3. Check Stations organization
if 'placeOnSurface(cuttingBoard, 0.85, LEVEL_1_Y' not in html:
    errors.append("Cutting board not placed flat on right counter top.")

if "'bottom-pao': { x: 0.68, z: -0.60" not in html:
    errors.append("Side-by-side ingredients layout for preparation station missing.")

if 'placeOnSurface(facaCozinhar, 1.22, LEVEL_1_Y' not in html:
    errors.append("Cooking knife position fix missing.")

if 'placeOnSurface(plateMesh, 0.0, yellowMatTopY + 0.002, -0.65' not in html:
    errors.append("Central plate alignment on yellow mat missing.")

# 4. Check placeOnSurface matrix update and bounding box validation
if 'const boxFinal = new THREE.Box3().setFromObject(model)' not in html or 'targetSurfaceY - minY' not in html:
    errors.append("Bounding box validation in placeOnSurface missing.")

print("=== VERIFICATION RESULTS ===")
if errors:
    print("ERRORS FOUND:")
    for err in errors:
        print(" -", err)
    sys.exit(1)
else:
    print("SUCCESS: All 4 critical requirements verified in index.html!")
