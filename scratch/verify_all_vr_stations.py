import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# 1. VR Teleportation System
if "window.teleportFloorMesh" not in html or "teleportReticle" not in html:
    errors.append("VR Teleport floor mesh or reticle missing.")

if "cameraGroup.position.set(targetPos.x, 0, targetPos.z)" not in html:
    errors.append("CameraGroup teleportation movement on WebXR trigger release missing.")

if "updateVRTeleportPointer()" not in html:
    errors.append("VR teleport pointer update loop missing.")

# 2. Restored Recipe Board & Ingredients
if "recipeBoardMesh.position.set(0.0, 1.75, -1.87)" not in html:
    errors.append("Recipe board UI on back wall missing or mispositioned.")

if "'carne-crua-burger.glb'" not in html or "'bottom-pao.glb'" not in html or "'burger-top.glb'" not in html:
    errors.append("Ingredients missing from ASSET_LIST.")

# 3. Station Organization
# A) Shelves
if "placeOnSurface(saleiroMesh, -0.90, 1.835, -1.82, 0.08)" not in html or "placeOnSurface(pimentaMesh, -0.60, 1.835, -1.82, 0.08)" not in html:
    errors.append("Left shelf salt & pepper placement missing.")

if "placeOnSurface(geleiaMesh, 0.55, 1.835, -1.82, 0.09)" not in html or "placeOnSurface(garrafaMesh, 0.95, 1.835, -1.82, 0.16)" not in html:
    errors.append("Right shelf jam, peanut butter, bottle placement missing.")

if "placeOnSurface(assadeiraMesh, -0.75, 1.835, -1.82, 0.32)" not in html:
    errors.append("Assadeira with reserve buns on shelf missing.")

# B) Counter
if "placeOnSurface(cooktopMesh, -1.15, COUNTER_TOP_Y + 0.002, -0.55, 0.46)" not in html:
    errors.append("Cooktop placement on left counter missing.")

if "placeOnSurface(skilletMesh, -1.15, cooktopTopY + 0.002, -0.55, 0.38)" not in html:
    errors.append("Skillet placement on cooktop burner missing.")

if "placeOnSurface(facaSimples, 1.22, LEVEL_1_Y, -0.60, 0.20)" not in html:
    errors.append("Flat knife placement beside cutting board missing.")

if "placeOnSurface(papelToalhaMesh, 1.58, LEVEL_1_Y, -0.55, 0.22)" not in html:
    errors.append("Paper towel roll placement missing.")

# C) Floor
if "placeOnSurface(lixeiraMesh, 1.62, 0.0, -0.10, 0.45)" not in html:
    errors.append("Trash bin placement on floor missing.")

# 4. Gameplay Logic
if "verifyOrder()" not in html or "PattyController" not in html or "GameEngine" not in html:
    errors.append("Core gameplay mechanics / verifyOrder missing.")

print("=== VERIFICATION RESULTS ===")
if errors:
    print("ERRORS FOUND:")
    for err in errors:
        print(" -", err)
    sys.exit(1)
else:
    print("SUCCESS: All 4 VR Teleportation System and station organization requirements verified!")
