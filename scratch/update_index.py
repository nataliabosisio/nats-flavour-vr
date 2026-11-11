import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace fitAndPlaceOnSurface and placeCooktopBuiltIn with updated placeOnSurface
old_place_functions = '''        function fitModelToSize(model, targetSize) {
            if (!model || targetSize == null) return model;

            model.scale.setScalar(1);
            model.updateMatrixWorld(true);

            const box = new THREE.Box3().setFromObject(model);
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            if (maxDim > 0) {
                model.scale.setScalar(targetSize / maxDim);
                model.updateMatrixWorld(true);
            }

            return model;
        }

        function placeCooktopBuiltIn(model, x, surfaceY, z) {
            if (!model) return model;

            // Escala proporcional realista em 3D (~0.54m de largura) sem achatar verticalmente
            fitModelToSize(model, 0.54);

            model.position.set(x, surfaceY, z);
            model.rotation.set(0, 0, 0);
            model.updateMatrixWorld(true);

            // Alinha o topo dos queimadores do fogão com a superfície desejada (surfaceY)
            const box = new THREE.Box3().setFromObject(model);
            const deltaY = surfaceY - box.max.y;
            if (Number.isFinite(deltaY)) {
                model.position.y += deltaY;
            }

            return model;
        }

        function fitAndPlaceOnSurface(model, x, surfaceY, z, targetSize = null) {
            if (!model) return model;

            if (targetSize) {
                fitModelToSize(model, targetSize);
            }

            model.position.set(x, surfaceY, z);
            model.updateMatrixWorld(true);
            const boxAfter = new THREE.Box3().setFromObject(model);
            const deltaY = surfaceY - boxAfter.min.y;
            if (Number.isFinite(deltaY)) {
                model.position.y += deltaY;
            }

            return model;
        }'''

new_place_functions = '''        function fitModelToSize(model, targetSize) {
            if (!model || targetSize == null) return model;

            model.scale.setScalar(1);
            model.updateMatrixWorld(true);

            const box = new THREE.Box3().setFromObject(model);
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            if (maxDim > 0) {
                model.scale.setScalar(targetSize / maxDim);
                model.updateMatrixWorld(true);
            }

            return model;
        }

        function placeOnSurface(model, x, targetSurfaceY, z, targetSize = null) {
            if (!model) return model;

            model.position.set(0, 0, 0);
            model.rotation.set(0, 0, 0);
            model.scale.set(1, 1, 1);
            model.updateMatrixWorld(true);

            if (targetSize != null) {
                const box = new THREE.Box3().setFromObject(model);
                const size = box.getSize(new THREE.Vector3());
                const maxDim = Math.max(size.x, size.y, size.z);
                if (maxDim > 0) {
                    model.scale.setScalar(targetSize / maxDim);
                    model.updateMatrixWorld(true);
                }
            }

            const boxFinal = new THREE.Box3().setFromObject(model);
            const minY = boxFinal.min.y;

            model.position.set(x, targetSurfaceY - minY, z);
            model.updateMatrixWorld(true);

            return model;
        }

        function fitAndPlaceOnSurface(model, x, surfaceY, z, targetSize = null) {
            return placeOnSurface(model, x, surfaceY, z, targetSize);
        }'''

if old_place_functions in content:
    content = content.replace(old_place_functions, new_place_functions)
    print("Replaced placement functions successfully.")
else:
    print("Could not find exact old placement functions!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
