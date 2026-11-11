import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# 1. Removal of cozinha-completa.glb and restoration of solid continuous L-shape counter
if "'cozinha-completa.glb'" in html:
    errors.append("cozinha-completa.glb is still in ASSET_LIST.")

if "topShape = new THREE.Shape()" not in html or "ExtrudeGeometry(topShape" not in html:
    errors.append("Solid continuous L-shape counter top extrusion missing.")

if "tilesBack" not in html or "tilesLeft" not in html:
    errors.append("Tiled wall background missing.")

# 2. Application of cooktop.glb
if "'fogao.glb'" in html:
    errors.append("Old fogao.glb is still in ASSET_LIST.")

if "'cooktop.glb'" not in html:
    errors.append("cooktop.glb is missing from ASSET_LIST.")

if "placeOnSurface(cooktopMesh, -1.15, COUNTER_TOP_Y + 0.002, -0.55, 0.46)" not in html:
    errors.append("cooktop.glb placement on counter with Y offset missing.")

if "placeOnSurface(skilletMesh, -1.15, cooktopTopY + 0.002, -0.55, 0.38)" not in html:
    errors.append("skillet placement on cooktop burner missing.")

# 3. Knife & Station Organization
if "placeOnSurface(facaSimples, 1.22, LEVEL_1_Y, -0.60, 0.20)" not in html:
    errors.append("Flat knife placement beside cutting board missing.")

if "'bottom-pao': { x: 0.68, z: -0.60" not in html or "'burger-top': { x: 1.02, z: -0.60" not in html:
    errors.append("Preparation station side-by-side spacing missing.")

if "placeOnSurface(plateMesh, 0.0, yellowMatTopY + 0.002, -0.65, 0.28)" not in html:
    errors.append("Assembly station center plate alignment missing.")

if "placeOnSurface(toasterMesh, 1.45, LEVEL_1_Y, -0.88, 0.22)" not in html:
    errors.append("Rear edge straight-line alignment missing.")

# 4. Logic & Mechanics
if "window.skilletCenter" not in html or "window.meatTrayCenter" not in html or "verifyOrder()" not in html:
    errors.append("Gameplay logic and interactions missing.")

print("=== VERIFICATION RESULTS ===")
if errors:
    print("ERRORS FOUND:")
    for err in errors:
        print(" -", err)
    sys.exit(1)
else:
    print("SUCCESS: All 4 restoration & cooktop requirements verified!")
