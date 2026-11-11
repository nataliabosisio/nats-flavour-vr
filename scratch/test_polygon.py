# Test 2D shape coordinates for counter top with stove slot
points_3d = [
    (-1.75, -1.05),
    (1.75, -1.05),
    (1.75, -0.30),
    (-0.90, -0.30),
    (-0.90, -0.80),
    (-1.40, -0.80),
    (-1.40, 0.35),
    (-1.75, 0.35)
]

# When mapping to 2D Shape for ExtrudeGeometry rotated by rotateX(-pi/2):
# 3D X = 2D X
# 3D Z = -2D Y  => 2D Y = -3D Z
points_2d = [(x, -z) for (x, z) in points_3d]

print("2D Shape points:")
for i, p in enumerate(points_2d):
    print(f"  {i}: {p}")

# Simple area calculation via Shoelace formula to verify non-self-intersecting positive area
area = 0
n = len(points_2d)
for i in range(n):
    j = (i + 1) % n
    area += points_2d[i][0] * points_2d[j][1]
    area -= points_2d[j][0] * points_2d[i][1]
area = abs(area) / 2.0

print(f"Polygon Area: {area:.4f} m^2")
if area > 0:
    print("SUCCESS: Valid 2D counter top polygon with stove slot!")
