import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update ASSET_LIST
old_asset_list = '''        const ASSET_LIST = [
            'fogao.glb', 'frigideira.glb', 'geladeira.glb', 'torradeira.glb',
            'prato-quadrado.glb', 'espatula.glb', 'faca-de-cozinhar.glb', 'faca.glb',
            'colher.glb', 'fuet.glb', 'bottom-pao.glb', 'burger-top.glb',
            'pao-burger.glb', 'fatia-queijo.glb', 'carne-crua-burger.glb',
            'carne-burger.glb', 'tomate.glb', 'tomate-cortado.glb'
        ];'''

new_asset_list = '''        const ASSET_LIST = [
            'cooktop.glb', 'cozinha-completa.glb', 'frigideira.glb', 'geladeira.glb', 'torradeira.glb',
            'prato-quadrado.glb', 'espatula.glb', 'faca-de-cozinhar.glb', 'faca.glb',
            'colher.glb', 'fuet.glb', 'bottom-pao.glb', 'burger-top.glb',
            'pao-burger.glb', 'fatia-queijo.glb', 'carne-crua-burger.glb',
            'carne-burger.glb', 'tomate.glb', 'tomate-cortado.glb'
        ];'''

if old_asset_list in content:
    content = content.replace(old_asset_list, new_asset_list)
    print("Updated ASSET_LIST successfully.")
else:
    print("Could not find exact old ASSET_LIST.")

# Replace buildKitchen function body
old_build_kitchen_pattern = r'function buildKitchen\(\)\s*\{.*?\n        \}'

new_build_kitchen = '''function buildKitchen() {
            const topMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4, metalness: 0.05 });
            const cabinetMat = new THREE.MeshStandardMaterial({ color: 0x1B2A4A, roughness: 0.45, flatShading: true });
            const handleMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.25, metalness: 0.8, flatShading: true });
            const wallMat = new THREE.MeshStandardMaterial({ color: 0xF5F2EB, roughness: 0.8 });
            const tileMat = new THREE.MeshStandardMaterial({ map: createTileTexture(), roughness: 0.15, color: 0xFFFFFF });
            const stainlessMat = new THREE.MeshStandardMaterial({ color: 0xD0D5DD, metalness: 0.85, roughness: 0.2, flatShading: true });

            // ==========================================
            // 1. ESTRUTURA DO AMBIENTE COMPLETO (cozinha-completa.glb)
            // ==========================================
            const kitchenFull = getAsset('cozinha-completa');
            if (kitchenFull) {
                // Escala e posicionamento para envolver o cenário sem áreas escuras
                placeOnSurface(kitchenFull, 0.0, 0.0, -0.65, 3.8);
                scene.add(kitchenFull);
            } else {
                // Piso e paredes de apoio caso o asset esteja carregando
                const floor = new THREE.Mesh(new THREE.PlaneGeometry(12, 12), new THREE.MeshStandardMaterial({ color: 0x17233B, roughness: 0.6 }));
                floor.rotation.x = -Math.PI / 2;
                floor.receiveShadow = true;
                scene.add(floor);

                const backWall = new THREE.Mesh(new THREE.PlaneGeometry(12, 4), wallMat);
                backWall.position.set(0, 2, -1.9);
                scene.add(backWall);

                const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(12, 4), wallMat);
                leftWall.position.set(-2.60, 2, 0);
                leftWall.rotation.y = Math.PI / 2;
                scene.add(leftWall);
            }

            const COUNTER_TOP_Y = 0.9100;
            const COUNTER_BASE_HEIGHT = 0.8600;
            const TOP_THICKNESS = 0.0500;

            // Gabinetes Inferiores da Bancada Principal
            const mainBase = new THREE.Mesh(new THREE.BoxGeometry(3.50, COUNTER_BASE_HEIGHT, 0.75), cabinetMat);
            mainBase.position.set(0, COUNTER_BASE_HEIGHT / 2, -0.675);
            mainBase.castShadow = true;
            mainBase.receiveShadow = true;
            scene.add(mainBase);

            const leftWingBase = new THREE.Mesh(new THREE.BoxGeometry(0.80, COUNTER_BASE_HEIGHT, 0.65), cabinetMat);
            leftWingBase.position.set(-1.35, COUNTER_BASE_HEIGHT / 2, 0.025);
            leftWingBase.castShadow = true;
            leftWingBase.receiveShadow = true;
            scene.add(leftWingBase);

            // Gavetas e Puxadores Frontais
            for (let i = 0; i < 5; i++) {
                const drawer = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.22, 0.02), new THREE.MeshStandardMaterial({ color: 0x142038, flatShading: true }));
                drawer.position.set(-1.2 + i * 0.6, 0.5, -0.29);
                scene.add(drawer);

                const handle = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.025, 0.03), handleMat);
                handle.position.set(-1.2 + i * 0.6, 0.5, -0.275);
                handle.castShadow = true;
                scene.add(handle);
            }

            // Tampo da Bancada em L Sólido Contínuo
            const topShape = new THREE.Shape();
            topShape.moveTo(-1.75, 1.05);
            topShape.lineTo(1.75, 1.05);
            topShape.lineTo(1.75, 0.30);
            topShape.lineTo(-0.95, 0.30);
            topShape.lineTo(-0.95, -0.35);
            topShape.lineTo(-1.75, -0.35);
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

            const LEVEL_1_Y = COUNTER_TOP_Y + 0.003;

            // Coifa de Inox sobre o Cooktop
            const hoodGroup = new THREE.Group();
            const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.16, 0.55), stainlessMat);
            hoodCanopy.position.set(-1.15, 1.95, -0.55);
            hoodCanopy.castShadow = true;
            hoodGroup.add(hoodCanopy);

            const hoodDuct = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.8, 16), stainlessMat);
            hoodDuct.position.set(-1.15, 2.40, -0.55);
            hoodGroup.add(hoodDuct);
            scene.add(hoodGroup);

            // ==========================================
            // 2. INTEGRAÇÃO DO COOKTOP (cooktop.glb)
            // ==========================================
            const cooktopMesh = getAsset('cooktop');
            placeOnSurface(cooktopMesh, -1.15, COUNTER_TOP_Y + 0.002, -0.55, 0.46);
            scene.add(cooktopMesh);

            const cooktopBox = new THREE.Box3().setFromObject(cooktopMesh);
            const cooktopTopY = cooktopBox.max.y; // Topo dos queimadores do cooktop

            // Frigideira plana e centralizada diretamente sobre uma das bocas do cooktop
            const skilletMesh = getAsset('frigideira');
            skilletMesh.rotation.set(0, 0, 0);
            placeOnSurface(skilletMesh, -1.15, cooktopTopY + 0.002, -0.55, 0.38);
            scene.add(skilletMesh);

            const skilletBox = new THREE.Box3().setFromObject(skilletMesh);
            window.skilletTopY = skilletBox.max.y;
            window.skilletCenter = new THREE.Vector3(-1.15, skilletBox.max.y + 0.002, -0.55);

            // Bandeja com a carne crua na superfície da bancada, ao lado esquerdo do cooktop
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

            // Potes brancos entre o cooktop e o prato central
            const bowl1 = createBowlMesh(0xD32F2F, 'sauce'); placeOnSurface(bowl1, -0.85, LEVEL_1_Y, -0.65); scene.add(bowl1);
            const bowl2 = createBowlMesh(0xFFD700, 'sauce'); placeOnSurface(bowl2, -0.70, LEVEL_1_Y, -0.65); scene.add(bowl2);
            const bowl3 = createBowlMesh(0x38B000, 'sauce'); placeOnSurface(bowl3, -0.55, LEVEL_1_Y, -0.65); scene.add(bowl3);
            const utensilJar = createUtensilJarMesh(); placeOnSurface(utensilJar, -0.40, LEVEL_1_Y, -0.65); scene.add(utensilJar);

            // ==========================================
            // 3. ESTAÇÃO DE MONTAGEM (CENTRO: X 0.0, Z -0.65)
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
            // 3. ESTAÇÃO DE PREPARO (DIREITA: X +0.50 a +1.60)
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

            // Faca deitada na horizontal sobre a bancada ao lado da tábua (NÃO cravada no pão)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.22, LEVEL_1_Y, -0.60, 0.20);
            facaSimples.rotation.set(0, Math.PI / 6, 0);
            scene.add(facaSimples);

            // Condimentos e Utensílios em linha reta ao longo da borda traseira (Z = -0.88)
            const ketchupBottle = createSqueezeBottleMesh(0xD32F2F); placeOnSurface(ketchupBottle, 0.62, LEVEL_1_Y, -0.88); scene.add(ketchupBottle);
            const mustardBottle = createSqueezeBottleMesh(0xFFD700); placeOnSurface(mustardBottle, 0.74, LEVEL_1_Y, -0.88); scene.add(mustardBottle);

            const espatulaMesh = getAsset('espatula');
            placeOnSurface(espatulaMesh, 0.88, LEVEL_1_Y, -0.88, 0.24);
            espatulaMesh.rotation.y = Math.PI / 4;
            scene.add(espatulaMesh);

            const tomatoMesh = getAsset('tomate');
            placeOnSurface(tomatoMesh, 1.02, LEVEL_1_Y, -0.88, 0.08);
            scene.add(tomatoMesh);

            const tomatoSlicedMesh = getAsset('tomate-cortado');
            placeOnSurface(tomatoSlicedMesh, 1.14, LEVEL_1_Y, -0.88, 0.08);
            scene.add(tomatoSlicedMesh);

            const knifeBlock = createKnifeBlockMesh(); placeOnSurface(knifeBlock, 1.28, LEVEL_1_Y, -0.88); scene.add(knifeBlock);

            const toasterMesh = getAsset('torradeira');
            placeOnSurface(toasterMesh, 1.45, LEVEL_1_Y, -0.88, 0.22);
            scene.add(toasterMesh);
}'''

content = re.sub(old_build_kitchen_pattern, new_build_kitchen, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied cooktop.glb and cozinha-completa.glb integration successfully.")
