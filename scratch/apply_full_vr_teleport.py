import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ASSET_LIST with all requested keys
new_asset_list = '''        const ASSET_LIST = [
            'cooktop.glb', 'frigideira.glb', 'geladeira.glb', 'torradeira.glb',
            'prato-quadrado.glb', 'espatula.glb', 'faca-de-cozinhar.glb', 'faca.glb',
            'colher.glb', 'fuet.glb', 'bottom-pao.glb', 'burger-top.glb',
            'pao-burger.glb', 'fatia-queijo.glb', 'carne-crua-burger.glb',
            'carne-burger.glb', 'tomate.glb', 'tomate-cortado.glb',
            'assadeira.glb', 'saleiro.glb', 'pimenta-do-reino.glb',
            'pote-de-geleia.glb', 'manteiga-de-amendoim.glb', 'garrafa.glb',
            'papel-toalha.glb', 'lixeira.glb'
        ];'''

old_asset_pattern = r'const ASSET_LIST = \[\s*.*?\];'
content = re.sub(old_asset_pattern, new_asset_list, content, flags=re.DOTALL)

# 2. Update createFallbackMesh to support all new keys
new_fallback_mesh = '''        function createFallbackMesh(key) {
            let mesh;
            switch (key) {
                case 'fogao':
                case 'cooktop':
                    mesh = new THREE.Mesh(
                        new THREE.BoxGeometry(0.46, 0.04, 0.46),
                        new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.35, metalness: 0.8, flatShading: true })
                    );
                    break;
                case 'frigideira':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.135, 0.038, 16), new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.8, roughness: 0.3, flatShading: true }));
                    break;
                case 'prato-quadrado':
                    mesh = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.015, 0.26), new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.2, flatShading: true }));
                    break;
                case 'bottom-pao':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.08, 0.032, 14), new THREE.MeshStandardMaterial({ color: 0xD4A373, roughness: 0.5, flatShading: true }));
                    break;
                case 'burger-top':
                    const domeGeo = new THREE.SphereGeometry(0.085, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2);
                    domeGeo.scale(1, 0.65, 1);
                    mesh = new THREE.Mesh(domeGeo, new THREE.MeshStandardMaterial({ color: 0xD2B48C, roughness: 0.5, flatShading: true }));
                    break;
                case 'fatia-queijo':
                    mesh = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.006, 0.15), new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.35, flatShading: true }));
                    break;
                case 'carne-crua-burger':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.024, 16), new THREE.MeshStandardMaterial({ color: 0xA03333, roughness: 0.7, flatShading: true }));
                    break;
                case 'carne-burger':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.024, 16), new THREE.MeshStandardMaterial({ color: 0x4A2511, roughness: 0.6, flatShading: true }));
                    break;
                case 'geladeira':
                    mesh = new THREE.Mesh(new THREE.BoxGeometry(0.65, 1.4, 0.65), new THREE.MeshStandardMaterial({ color: 0x1B2A4A, roughness: 0.3, flatShading: true }));
                    break;
                case 'torradeira':
                    mesh = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.16, 0.14), new THREE.MeshStandardMaterial({ color: 0xB0B8C0, metalness: 0.8, roughness: 0.2, flatShading: true }));
                    break;
                case 'assadeira':
                    mesh = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.025, 0.26), new THREE.MeshStandardMaterial({ color: 0x808080, metalness: 0.8, roughness: 0.3, flatShading: true }));
                    break;
                case 'saleiro':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.07, 12), new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.2, flatShading: true }));
                    break;
                case 'pimenta-do-reino':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.07, 12), new THREE.MeshStandardMaterial({ color: 0x333333, roughness: 0.4, flatShading: true }));
                    break;
                case 'pote-de-geleia':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.08, 12), new THREE.MeshStandardMaterial({ color: 0xB71C1C, roughness: 0.2, flatShading: true }));
                    break;
                case 'manteiga-de-amendoim':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.09, 12), new THREE.MeshStandardMaterial({ color: 0xD78B30, roughness: 0.3, flatShading: true }));
                    break;
                case 'garrafa':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.035, 0.22, 12), new THREE.MeshStandardMaterial({ color: 0x2E7D32, roughness: 0.15, flatShading: true }));
                    break;
                case 'papel-toalha':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.22, 16), new THREE.MeshStandardMaterial({ color: 0xFAFAFA, roughness: 0.7, flatShading: true }));
                    break;
                case 'lixeira':
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.16, 0.45, 16), new THREE.MeshStandardMaterial({ color: 0x212121, metalness: 0.5, roughness: 0.4, flatShading: true }));
                    break;
                default:
                    mesh = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 0.1), new THREE.MeshStandardMaterial({ color: 0x20B2AA, flatShading: true }));
                    break;
            }

            mesh.traverse(child => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                }
            });

            return mesh;
        }'''

old_fallback_pattern = r'function createFallbackMesh\(key\)\s*\{.*?\n        \}'
content = re.sub(old_fallback_pattern, new_fallback_mesh, content, flags=re.DOTALL)

# 3. Replace buildKitchen function body to layout all stations and VR teleport floor
new_build_kitchen = '''function buildKitchen() {
            const topMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4, metalness: 0.05 });
            const cabinetMat = new THREE.MeshStandardMaterial({ color: 0x1B2A4A, roughness: 0.45, flatShading: true });
            const handleMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.25, metalness: 0.8, flatShading: true });
            const wallMat = new THREE.MeshStandardMaterial({ color: 0xF5F2EB, roughness: 0.8 });
            const tileMat = new THREE.MeshStandardMaterial({ map: createTileTexture(), roughness: 0.15, color: 0xFFFFFF });
            const stainlessMat = new THREE.MeshStandardMaterial({ color: 0xD0D5DD, metalness: 0.85, roughness: 0.2, flatShading: true });

            // Piso Visível
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(12, 12), new THREE.MeshStandardMaterial({ color: 0x17233B, roughness: 0.6 }));
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);

            // Malha de Teletransporte VR no Piso (Invisível para Raycast)
            window.teleportFloorMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(12, 12),
                new THREE.MeshBasicMaterial({ visible: false })
            );
            window.teleportFloorMesh.rotation.x = -Math.PI / 2;
            window.teleportFloorMesh.name = 'teleportFloor';
            scene.add(window.teleportFloorMesh);

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
            // BANCADA PRINCIPAL EM L (TAMPÃO SÓLIDO CONTÍNUO)
            // ==========================================
            const COUNTER_TOP_Y = 0.9100;
            const COUNTER_BASE_HEIGHT = 0.8600;
            const TOP_THICKNESS = 0.0500;

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

            for (let i = 0; i < 5; i++) {
                const drawer = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.22, 0.02), new THREE.MeshStandardMaterial({ color: 0x142038, flatShading: true }));
                drawer.position.set(-1.2 + i * 0.6, 0.5, -0.29);
                scene.add(drawer);

                const handle = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.025, 0.03), handleMat);
                handle.position.set(-1.2 + i * 0.6, 0.5, -0.275);
                handle.castShadow = true;
                scene.add(handle);
            }

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

            // Geladeira
            const fridgeMesh = getAsset('geladeira');
            placeOnSurface(fridgeMesh, -2.10, 0.0, -1.55, 1.85);
            fridgeMesh.rotation.y = 0.15;
            scene.add(fridgeMesh);

            // Coifa de Inox
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
            // 3.A) PRATELEIRAS SUSPENSAS (PAREDE DO FUNDO)
            // ==========================================
            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            
            // Prateleira Esquerda
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf1.position.set(-0.75, 1.82, -1.84);
            shelf1.castShadow = true;
            scene.add(shelf1);

            // Prateleira Direita
            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf2.position.set(0.75, 1.82, -1.84);
            shelf2.castShadow = true;
            scene.add(shelf2);

            // Prateleira Esquerda: Saleiro e Pimenta-do-reino lado a lado
            const saleiroMesh = getAsset('saleiro');
            placeOnSurface(saleiroMesh, -0.90, 1.835, -1.82, 0.08);
            scene.add(saleiroMesh);

            const pimentaMesh = getAsset('pimenta-do-reino');
            placeOnSurface(pimentaMesh, -0.60, 1.835, -1.82, 0.08);
            scene.add(pimentaMesh);

            // Prateleira Direita: Pote de Geleia, Manteiga de Amendoim e Garrafa alinhados
            const geleiaMesh = getAsset('pote-de-geleia');
            placeOnSurface(geleiaMesh, 0.55, 1.835, -1.82, 0.09);
            scene.add(geleiaMesh);

            const manteigaMesh = getAsset('manteiga-de-amendoim');
            placeOnSurface(manteigaMesh, 0.75, 1.835, -1.82, 0.09);
            scene.add(manteigaMesh);

            const garrafaMesh = getAsset('garrafa');
            placeOnSurface(garrafaMesh, 0.95, 1.835, -1.82, 0.16);
            scene.add(garrafaMesh);

            // Assadeira na prateleira esquerda contendo pães reservas (estoque visual)
            const assadeiraMesh = getAsset('assadeira');
            placeOnSurface(assadeiraMesh, -0.75, 1.835, -1.82, 0.32);
            scene.add(assadeiraMesh);

            const assadeiraBox = new THREE.Box3().setFromObject(assadeiraMesh);
            const assadeiraTopY = assadeiraBox.max.y;

            const reserveBun1 = getAsset('bottom-pao');
            placeOnSurface(reserveBun1, -0.82, assadeiraTopY + 0.001, -1.82, 0.12);
            scene.add(reserveBun1);

            const reserveBun2 = getAsset('burger-top');
            placeOnSurface(reserveBun2, -0.68, assadeiraTopY + 0.001, -1.82, 0.12);
            scene.add(reserveBun2);

            // ==========================================
            // 3.B) ESTAÇÃO DE COCÇÃO (ESQUERDA)
            // ==========================================
            const cooktopMesh = getAsset('cooktop');
            placeOnSurface(cooktopMesh, -1.15, COUNTER_TOP_Y + 0.002, -0.55, 0.46);
            scene.add(cooktopMesh);

            const cooktopBox = new THREE.Box3().setFromObject(cooktopMesh);
            const cooktopTopY = cooktopBox.max.y;

            const skilletMesh = getAsset('frigideira');
            skilletMesh.rotation.set(0, 0, 0);
            placeOnSurface(skilletMesh, -1.15, cooktopTopY + 0.002, -0.55, 0.38);
            scene.add(skilletMesh);

            const skilletBox = new THREE.Box3().setFromObject(skilletMesh);
            window.skilletTopY = skilletBox.max.y;
            window.skilletCenter = new THREE.Vector3(-1.15, skilletBox.max.y + 0.002, -0.55);

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

            const bowl1 = createBowlMesh(0xD32F2F, 'sauce'); placeOnSurface(bowl1, -0.85, LEVEL_1_Y, -0.65); scene.add(bowl1);
            const bowl2 = createBowlMesh(0xFFD700, 'sauce'); placeOnSurface(bowl2, -0.70, LEVEL_1_Y, -0.65); scene.add(bowl2);
            const bowl3 = createBowlMesh(0x38B000, 'sauce'); placeOnSurface(bowl3, -0.55, LEVEL_1_Y, -0.65); scene.add(bowl3);
            const utensilJar = createUtensilJarMesh(); placeOnSurface(utensilJar, -0.40, LEVEL_1_Y, -0.65); scene.add(utensilJar);

            // ==========================================
            // 3.B) ESTAÇÃO DE MONTAGEM (CENTRO)
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
            // 3.B) ESTAÇÃO DE PREPARO (DIREITA)
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

            // Faca deitada plana sobre o tampo da bancada (NUNCA fincada dentro do pão)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.22, LEVEL_1_Y, -0.60, 0.20);
            facaSimples.rotation.set(0, Math.PI / 6, 0);
            scene.add(facaSimples);

            // Papel toalha no canto direito da bancada
            const papelToalhaMesh = getAsset('papel-toalha');
            placeOnSurface(papelToalhaMesh, 1.58, LEVEL_1_Y, -0.55, 0.22);
            scene.add(papelToalhaMesh);

            // Borda Traseira: Torradeira, Ketchup e Mostarda em linha reta (Z = -0.88)
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

            // ==========================================
            // 3.C) CHÃO E PISO (Lixeira encostada à lateral da bancada)
            // ==========================================
            const lixeiraMesh = getAsset('lixeira');
            placeOnSurface(lixeiraMesh, 1.62, 0.0, -0.10, 0.45);
            scene.add(lixeiraMesh);
}'''

old_build_kitchen_pattern = r'function buildKitchen\(\)\s*\{.*?\n        \}'
content = re.sub(old_build_kitchen_pattern, new_build_kitchen, content, flags=re.DOTALL)

# 4. Update createRecipeBoard to position recipe TV board centered on back wall between shelves
new_recipe_board = '''        function createRecipeBoard() {
            const canvas = document.createElement('canvas');
            canvas.width = 600;
            canvas.height = 360;
            recipeCanvasCtx = canvas.getContext('2d');

            recipeTexture = new THREE.CanvasTexture(canvas);
            const boardGeo = new THREE.PlaneGeometry(0.85, 0.50);
            const boardMat = new THREE.MeshBasicMaterial({ map: recipeTexture, transparent: true });
            recipeBoardMesh = new THREE.Mesh(boardGeo, boardMat);
            // Fixado na parede de azulejos claros ao fundo, centralizado na altura dos olhos entre as prateleiras
            recipeBoardMesh.position.set(0.0, 1.75, -1.87);
            recipeBoardMesh.visible = true;
            scene.add(recipeBoardMesh);

            updateRecipeBoard();
        }'''

old_recipe_board_pattern = r'function createRecipeBoard\(\)\s*\{.*?\n        \}'
content = re.sub(old_recipe_board_pattern, new_recipe_board, content, flags=re.DOTALL)

# 5. Update WebXR Controllers and add VR Teleportation System & Reticle
old_xr_controllers_pattern = r'// ==========================================\s*// 14\. CONTROLES WEBXR.*?\n        // ==========================================\s*// 15\. EVENTOS DE UI'

new_xr_controllers = '''// ==========================================
        // 14. SISTEMA DE TELETRANSPORTE & CONTROLES WEBXR
        // ==========================================
        const controllerModelFactory = new XRControllerModelFactory();
        const controllers = [];

        // Anel visual de mira no piso para teletransporte VR
        const teleportReticle = new THREE.Mesh(
            new THREE.RingGeometry(0.12, 0.16, 32),
            new THREE.MeshBasicMaterial({ color: 0x20B2AA, side: THREE.DoubleSide })
        );
        teleportReticle.rotation.x = -Math.PI / 2;
        teleportReticle.visible = false;
        scene.add(teleportReticle);

        const tempXRMatrix = new THREE.Matrix4();
        const xrRaycaster = new THREE.Raycaster();

        for (let i = 0; i < 2; i++) {
            const controller = renderer.xr.getController(i);

            const laserGeo = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(0, 0, 0),
                new THREE.Vector3(0, 0, -2.5)
            ]);
            const laserMat = new THREE.LineBasicMaterial({ color: 0x20B2AA, linewidth: 2 });
            const laser = new THREE.Line(laserGeo, laserMat);
            controller.add(laser);

            const cursorGeo = new THREE.RingGeometry(0.01, 0.016, 16);
            const cursorMat = new THREE.MeshBasicMaterial({ color: 0x20B2AA, side: THREE.DoubleSide });
            const cursor = new THREE.Mesh(cursorGeo, cursorMat);
            cursor.position.z = -1.5;
            controller.add(cursor);

            scene.add(controller);

            const grip = renderer.xr.getControllerGrip(i);
            grip.add(controllerModelFactory.createControllerModel(grip));
            scene.add(grip);

            controller.addEventListener('selectstart', () => {
                if (!gameEngine || !gameEngine.isPlaying) return;
                audioManager.init();

                tempXRMatrix.identity().extractRotation(controller.matrixWorld);
                xrRaycaster.ray.origin.setFromMatrixPosition(controller.matrixWorld);
                xrRaycaster.ray.direction.set(0, 0, -1).applyMatrix4(tempXRMatrix);

                // 1. Verifica intersecção com itens interagíveis (hambúrguer, pães, carne)
                const meshes = interactiveItems.map(item => item.mesh);
                const intersects = xrRaycaster.intersectObjects(meshes, true);

                if (intersects.length > 0) {
                    let hitMesh = intersects[0].object;
                    while (hitMesh.parent && hitMesh.parent !== scene) hitMesh = hitMesh.parent;

                    const item = interactiveItems.find(i => i.mesh === hitMesh);
                    if (item) {
                        if (item.type === 'carne-crua' && pattyController.state === 0) {
                            pattyController.startCooking();
                            return;
                        }

                        if (pattyController.mesh === item.mesh && pattyController.state === 1) {
                            return;
                        }

                        controller.userData.selectedItem = item;
                        audioManager.playPop();
                        return;
                    }
                }

                // 2. Teletransporte VR se apontar para o piso (teleportFloorMesh)
                if (window.teleportFloorMesh) {
                    const floorIntersects = xrRaycaster.intersectObject(window.teleportFloorMesh);
                    if (floorIntersects.length > 0) {
                        const hitPos = floorIntersects[0].point;
                        controller.userData.teleportTarget = hitPos.clone();
                    }
                }
            });

            controller.addEventListener('selectend', () => {
                // Executa o agarrar/soltar objeto
                const item = controller.userData.selectedItem;
                if (item) {
                    controller.userData.selectedItem = null;

                    const pos = item.mesh.position;
                    const plateDist = pos.distanceTo(new THREE.Vector3(0.0, 0.9220, -0.65));
                    if (plateDist < 0.28) {
                        const snapped = gameEngine.trySnapToPlate(item);
                        if (snapped) return;
                    }

                    vfxManager.addLerp(item.mesh, item.originalPos);
                    return;
                }

                // Executa o Teletransporte VR movendo a câmera/jogador (cameraGroup)
                if (controller.userData.teleportTarget) {
                    const targetPos = controller.userData.teleportTarget;
                    controller.userData.teleportTarget = null;

                    cameraGroup.position.set(targetPos.x, 0, targetPos.z);
                    audioManager.playPop();
                    teleportReticle.visible = false;
                }
            });

            controllers.push(controller);
        }

        // Atualização do indicador de teletransporte VR no loop
        function updateVRTeleportPointer() {
            if (!renderer.xr.isPresenting) {
                teleportReticle.visible = false;
                return;
            }

            let reticleActive = false;
            controllers.forEach(controller => {
                if (controller.userData.selectedItem) return;

                tempXRMatrix.identity().extractRotation(controller.matrixWorld);
                xrRaycaster.ray.origin.setFromMatrixPosition(controller.matrixWorld);
                xrRaycaster.ray.direction.set(0, 0, -1).applyMatrix4(tempXRMatrix);

                if (window.teleportFloorMesh) {
                    const intersects = xrRaycaster.intersectObject(window.teleportFloorMesh);
                    if (intersects.length > 0) {
                        const p = intersects[0].point;
                        teleportReticle.position.set(p.x, 0.005, p.z);
                        teleportReticle.visible = true;
                        reticleActive = true;
                    }
                }
            });

            if (!reticleActive) {
                teleportReticle.visible = false;
            }
        }'''

content = re.sub(old_xr_controllers_pattern, new_xr_controllers + '\n\n        // ==========================================\n        // 15. EVENTOS DE UI', content, flags=re.DOTALL)

# 6. Add updateVRTeleportPointer() to render loop
content = content.replace("controls.update();", "controls.update();\n            updateVRTeleportPointer();")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied full VR teleport system, restored recipe board, and organized all 3D stations successfully.")
