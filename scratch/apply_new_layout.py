import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add placeStoveOnFloor function
new_placement_code = '''        function placeStoveOnFloor(stoveMesh, x, z, targetTopY) {
            if (!stoveMesh) return stoveMesh;

            stoveMesh.position.set(0, 0, 0);
            stoveMesh.rotation.set(0, 0, 0);
            stoveMesh.scale.set(1, 1, 1);
            stoveMesh.updateMatrixWorld(true);

            const box = new THREE.Box3().setFromObject(stoveMesh);
            const rawHeight = box.max.y - box.min.y;

            if (rawHeight > 0) {
                const scaleFactor = targetTopY / rawHeight;
                stoveMesh.scale.setScalar(scaleFactor);
                stoveMesh.updateMatrixWorld(true);
            }

            const boxScaled = new THREE.Box3().setFromObject(stoveMesh);
            stoveMesh.position.set(x, -boxScaled.min.y, z);
            stoveMesh.updateMatrixWorld(true);

            return stoveMesh;
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
        }'''

# Replace placement functions block
old_place_block_pattern = r'function fitModelToSize\(model, targetSize\)\s*\{.*?function fitAndPlaceOnSurface\(model, x, surfaceY, z, targetSize = null\)\s*\{.*?\}'

new_full_place_block = '''        function fitModelToSize(model, targetSize) {
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

''' + new_placement_code + '''

        function fitAndPlaceOnSurface(model, x, surfaceY, z, targetSize = null) {
            return placeOnSurface(model, x, surfaceY, z, targetSize);
        }'''

content = re.sub(old_place_block_pattern, new_full_place_block, content, flags=re.DOTALL)

# Replace buildKitchen function body
old_build_kitchen_pattern = r'function buildKitchen\(\)\s*\{.*?\n        \}'

new_build_kitchen = '''function buildKitchen() {
            const topMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4, metalness: 0.05 });
            const cabinetMat = new THREE.MeshStandardMaterial({ color: 0x1B2A4A, roughness: 0.45, flatShading: true });
            const handleMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.25, metalness: 0.8, flatShading: true });
            const wallMat = new THREE.MeshStandardMaterial({ color: 0xF5F2EB, roughness: 0.8 });
            const tileMat = new THREE.MeshStandardMaterial({ map: createTileTexture(), roughness: 0.15, color: 0xFFFFFF });
            const stainlessMat = new THREE.MeshStandardMaterial({ color: 0xD0D5DD, metalness: 0.85, roughness: 0.2, flatShading: true });

            // Piso
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(12, 12), new THREE.MeshStandardMaterial({ color: 0x17233B, roughness: 0.6 }));
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);

            // Parede de Fundo (Fechada)
            const backWall = new THREE.Mesh(new THREE.PlaneGeometry(12, 4), wallMat);
            backWall.position.set(0, 2, -1.9);
            scene.add(backWall);

            // Parede Lateral Esquerda
            const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(12, 4), wallMat);
            leftWall.position.set(-2.60, 2, 0);
            leftWall.rotation.y = Math.PI / 2;
            scene.add(leftWall);

            // Azulejos na Parede de Fundo
            const tilesBack = new THREE.Mesh(new THREE.PlaneGeometry(10, 1.8), tileMat);
            tilesBack.position.set(0, 1.6, -1.89);
            tilesBack.receiveShadow = true;
            scene.add(tilesBack);

            // Azulejos na Parede Esquerda
            const tilesLeft = new THREE.Mesh(new THREE.PlaneGeometry(8, 1.8), tileMat);
            tilesLeft.position.set(-2.59, 1.6, 0);
            tilesLeft.rotation.y = Math.PI / 2;
            tilesLeft.receiveShadow = true;
            scene.add(tilesLeft);

            // ==========================================
            // 1. CORREÇÃO DA BANCADA E VÃO DO FOGÃO DE PISO:
            // - Superfície superior plana em Y = 0.9100.
            // - Encaixe sob medida para o fogão de piso (fogao.glb) no lado esquerdo.
            // ==========================================
            const COUNTER_TOP_Y = 0.9100;
            const COUNTER_BASE_HEIGHT = 0.8600;
            const TOP_THICKNESS = 0.0500;

            // Gabinete Principal (Centro e Direita)
            const mainBase = new THREE.Mesh(new THREE.BoxGeometry(2.60, COUNTER_BASE_HEIGHT, 0.75), cabinetMat);
            mainBase.position.set(0.40, COUNTER_BASE_HEIGHT / 2, -0.675);
            mainBase.castShadow = true;
            mainBase.receiveShadow = true;
            scene.add(mainBase);

            // Gabinete Lateral (Extremidade Esquerda)
            const leftWingBase = new THREE.Mesh(new THREE.BoxGeometry(0.35, COUNTER_BASE_HEIGHT, 1.40), cabinetMat);
            leftWingBase.position.set(-1.575, COUNTER_BASE_HEIGHT / 2, -0.35);
            leftWingBase.castShadow = true;
            leftWingBase.receiveShadow = true;
            scene.add(leftWingBase);

            // Gavetas e Puxadores Frontais
            for (let i = 0; i < 4; i++) {
                const drawer = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.22, 0.02), new THREE.MeshStandardMaterial({ color: 0x142038, flatShading: true }));
                drawer.position.set(-0.5 + i * 0.6, 0.5, -0.29);
                scene.add(drawer);

                const handle = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.025, 0.03), handleMat);
                handle.position.set(-0.5 + i * 0.6, 0.5, -0.275);
                handle.castShadow = true;
                scene.add(handle);
            }

            // TAMPO EM L COM ENCAIXE PARA FOGÃO DE PISO (SEM CORTES DESALINHADOS)
            const topShape = new THREE.Shape();
            topShape.moveTo(-1.75, 1.05);   // Canto traseiro esquerdo (3D Z = -1.05)
            topShape.lineTo(1.75, 1.05);    // Canto traseiro direito (3D Z = -1.05)
            topShape.lineTo(1.75, 0.30);    // Canto frontal direito (3D Z = -0.30)
            topShape.lineTo(-0.90, 0.30);   // Lado direito do vão do fogão (3D Z = -0.30)
            topShape.lineTo(-0.90, 0.80);   // Fundo do vão do fogão (3D Z = -0.80)
            topShape.lineTo(-1.40, 0.80);   // Lado esquerdo do vão do fogão (3D Z = -0.80)
            topShape.lineTo(-1.40, -0.35);  // Canto frontal da asa esquerda (3D Z = +0.35)
            topShape.lineTo(-1.75, -0.35);  // Canto externo frontal esquerdo (3D Z = +0.35)
            topShape.closePath();

            const extrudeSettings = {
                depth: TOP_THICKNESS,
                bevelEnabled: true,
                bevelSegments: 2,
                steps: 1,
                bevelSize: 0.004,
                bevelThickness: 0.004
            };
            const topGeo = new THREE.ExtrudeGeometry(topShape, extrudeSettings);
            topGeo.rotateX(-Math.PI / 2);

            const lShapeTop = new THREE.Mesh(topGeo, topMat);
            lShapeTop.position.set(0, COUNTER_BASE_HEIGHT, 0);
            lShapeTop.castShadow = true;
            lShapeTop.receiveShadow = true;
            scene.add(lShapeTop);

            // Nível 1 (+0.003 deslocamento para evitar z-fighting sem flutuar)
            const LEVEL_1_Y = COUNTER_TOP_Y + 0.003;

            // ==========================================
            // ELEMENTOS DE COMPOSIÇÃO DE FUNDO E APRELHOS
            // ==========================================
            const fridgeMesh = getAsset('geladeira');
            placeOnSurface(fridgeMesh, -2.10, 0.0, -1.55, 1.85);
            fridgeMesh.rotation.y = 0.15;
            scene.add(fridgeMesh);

            const hoodGroup = new THREE.Group();
            const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.16, 0.55), stainlessMat);
            hoodCanopy.position.set(-1.15, 1.95, -0.55);
            hoodCanopy.castShadow = true;
            hoodGroup.add(hoodCanopy);

            const hoodDuct = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.8, 16), stainlessMat);
            hoodDuct.position.set(-1.15, 2.40, -0.55);
            hoodGroup.add(hoodDuct);
            scene.add(hoodGroup);

            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.03, 0.22), shelfMat);
            shelf1.position.set(0.75, 1.82, -1.84);
            shelf1.castShadow = true;
            scene.add(shelf1);

            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.03, 0.22), shelfMat);
            shelf2.position.set(-0.65, 1.82, -1.84);
            shelf2.castShadow = true;
            scene.add(shelf2);

            const jar1 = createBowlMesh(0xC0392B, 'sauce'); placeOnSurface(jar1, 0.45, 1.835, -1.82); scene.add(jar1);
            const jar2 = createBowlMesh(0xF39C12, 'sauce'); placeOnSurface(jar2, 0.65, 1.835, -1.82); scene.add(jar2);
            const jar3 = createBowlMesh(0x27AE60, 'sauce'); placeOnSurface(jar3, 0.85, 1.835, -1.82); scene.add(jar3);

            // ==========================================
            // 1. CORREÇÃO CRÍTICA DO FOGÃO (fogao.glb): POSICIONAMENTO NO CHÃO
            // ==========================================
            // Fogão de piso com base no CHÃO (y=0) e bocas niveladas com o tampo da bancada (y=0.9100)
            const cooktop = getAsset('fogao');
            placeStoveOnFloor(cooktop, -1.15, -0.55, COUNTER_TOP_Y);
            scene.add(cooktop);

            const stoveBox = new THREE.Box3().setFromObject(cooktop);
            const stoveTopY = stoveBox.max.y; // Nível das bocas superiores do fogão (0.9100)

            // Frigideira: Plana e centralizada diretamente sobre uma das bocas superiores do fogão
            const skilletMesh = getAsset('frigideira');
            skilletMesh.rotation.set(0, 0, 0);
            placeOnSurface(skilletMesh, -1.15, stoveTopY + 0.003, -0.55, 0.38);
            scene.add(skilletMesh);

            const skilletBox = new THREE.Box3().setFromObject(skilletMesh);
            window.skilletTopY = skilletBox.max.y;
            window.skilletCenter = new THREE.Vector3(-1.15, skilletBox.max.y + 0.002, -0.55);

            // Bandeja de carne crua: Mover para a superfície da bancada, à esquerda do fogão
            const meatTray = new THREE.Mesh(
                new THREE.BoxGeometry(0.26, 0.012, 0.20),
                stainlessMat
            );
            placeOnSurface(meatTray, -1.55, LEVEL_1_Y, -0.50);
            meatTray.castShadow = true;
            meatTray.receiveShadow = true;
            scene.add(meatTray);

            const meatTrayBox = new THREE.Box3().setFromObject(meatTray);
            window.meatTrayTopY = meatTrayBox.max.y;
            window.meatTrayCenter = new THREE.Vector3(-1.55, meatTrayBox.max.y + 0.002, -0.50);

            // ==========================================
            // 3. ESPÁTULA E POTES BRANCOS: ENTRE O FOGÃO E O PRATO CENTRAL
            // ==========================================
            const bowl1 = createBowlMesh(0xD32F2F, 'sauce'); placeOnSurface(bowl1, -0.85, LEVEL_1_Y, -0.65); scene.add(bowl1);
            const bowl2 = createBowlMesh(0xFFD700, 'sauce'); placeOnSurface(bowl2, -0.70, LEVEL_1_Y, -0.65); scene.add(bowl2);
            const bowl3 = createBowlMesh(0x38B000, 'sauce'); placeOnSurface(bowl3, -0.55, LEVEL_1_Y, -0.65); scene.add(bowl3);
            const utensilJar = createUtensilJarMesh(); placeOnSurface(utensilJar, -0.40, LEVEL_1_Y, -0.65); scene.add(utensilJar);

            const espatulaMesh = getAsset('espatula');
            placeOnSurface(espatulaMesh, -0.60, LEVEL_1_Y, -0.50, 0.24);
            espatulaMesh.rotation.y = Math.PI / 4;
            scene.add(espatulaMesh);

            // ==========================================
            // ESTAÇÃO DE MONTAGEM (CENTRO: X 0.0, Z -0.65)
            // ==========================================
            const yellowMatMesh = new THREE.Mesh(
                new THREE.BoxGeometry(0.52, 0.006, 0.42),
                new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.3, flatShading: true })
            );
            placeOnSurface(yellowMatMesh, 0.0, LEVEL_1_Y, -0.65);
            yellowMatMesh.receiveShadow = true;
            scene.add(yellowMatMesh);

            const yellowMatBox = new THREE.Box3().setFromObject(yellowMatMesh);
            const yellowMatTopY = yellowMatBox.max.y;

            const snapRing = new THREE.Mesh(
                new THREE.RingGeometry(0.14, 0.165, 16),
                new THREE.MeshBasicMaterial({ color: 0x20B2AA, side: THREE.DoubleSide })
            );
            snapRing.rotation.x = -Math.PI / 2;
            snapRing.position.set(0.0, yellowMatTopY + 0.001, -0.65);
            scene.add(snapRing);

            const plateMesh = getAsset('prato-quadrado');
            plateMesh.rotation.set(0, 0, 0);
            placeOnSurface(plateMesh, 0.0, yellowMatTopY + 0.002, -0.65, 0.28);
            scene.add(plateMesh);

            const plateBox = new THREE.Box3().setFromObject(plateMesh);
            window.plateSurfaceTopY = plateBox.max.y;

            // ==========================================
            // ESTAÇÃO DE PREPARO (DIREITA: X +0.50 a +1.60)
            // ==========================================
            const cuttingBoard = new THREE.Mesh(
                new THREE.BoxGeometry(0.48, 0.02, 0.36),
                new THREE.MeshStandardMaterial({ color: 0xB5651D, roughness: 0.6, flatShading: true })
            );
            placeOnSurface(cuttingBoard, 0.85, LEVEL_1_Y, -0.60, 0.48);
            cuttingBoard.rotation.y = 0;
            cuttingBoard.castShadow = true;
            cuttingBoard.receiveShadow = true;
            scene.add(cuttingBoard);

            const cuttingBoardBox = new THREE.Box3().setFromObject(cuttingBoard);
            window.boardTopY = cuttingBoardBox.max.y;

            // 2. CORREÇÃO DA FACA: REMOVIDA DE DENTRO DO PÃO (Posicionada deitada plana à direita da tábua)
            const facaCozinhar = getAsset('faca-de-cozinhar');
            placeOnSurface(facaCozinhar, 1.22, LEVEL_1_Y, -0.60, 0.22);
            facaCozinhar.rotation.set(0, Math.PI / 6, 0);
            scene.add(facaCozinhar);

            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.34, LEVEL_1_Y, -0.60, 0.20);
            facaSimples.rotation.set(0, Math.PI / 6, 0);
            scene.add(facaSimples);

            // 3. ACOMPANHAMENTOS EM LINHA RETA AO LONGO DA BORDA TRASEIRA DA BANCADA (Z = -0.88)
            const tomatoMesh = getAsset('tomate');
            placeOnSurface(tomatoMesh, 0.58, LEVEL_1_Y, -0.88, 0.08);
            scene.add(tomatoMesh);

            const tomatoSlicedMesh = getAsset('tomate-cortado');
            placeOnSurface(tomatoSlicedMesh, 0.70, LEVEL_1_Y, -0.88, 0.08);
            scene.add(tomatoSlicedMesh);

            const ketchupBottle = createSqueezeBottleMesh(0xD32F2F); placeOnSurface(ketchupBottle, 0.82, LEVEL_1_Y, -0.88); scene.add(ketchupBottle);
            const mustardBottle = createSqueezeBottleMesh(0xFFD700); placeOnSurface(mustardBottle, 0.94, LEVEL_1_Y, -0.88); scene.add(mustardBottle);

            const knifeBlock = createKnifeBlockMesh(); placeOnSurface(knifeBlock, 1.15, LEVEL_1_Y, -0.88); scene.add(knifeBlock);

            const toasterMesh = getAsset('torradeira');
            placeOnSurface(toasterMesh, 1.40, LEVEL_1_Y, -0.88, 0.22);
            scene.add(toasterMesh);
}'''

content = re.sub(old_build_kitchen_pattern, new_build_kitchen, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied new floor stove layout and updated kitchen elements successfully.")
