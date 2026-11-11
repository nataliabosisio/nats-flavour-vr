import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Room Dimensions and Walls (Section 1)
# ROOM_WIDTH = 8.0, ROOM_DEPTH = 6.0, ROOM_HEIGHT = 3.2
# WALL_BACK_Z = -1.90, WALL_FRONT_Z = 3.10, WALL_LEFT_X = -4.00, WALL_RIGHT_X = 4.00
# All walls and ceiling using tileMat!
room_pattern = r'// DIMENS.*?scene\.add\(tilesFront\);'
new_room_code = """// DIMENSÕES ESTRUTURAIS FIXAS DO CENÁRIO (LANCHONETE)
            // ==========================================
            const ROOM_WIDTH = 8.0;
            const ROOM_DEPTH = 6.0;
            const ROOM_HEIGHT = 3.2;

            const WALL_BACK_Z = -1.90;
            const WALL_FRONT_Z = 3.10;
            const CENTER_Z = (WALL_BACK_Z + WALL_FRONT_Z) / 2; // 0.60
            const HALF_W = ROOM_WIDTH / 2; // 4.00
            const WALL_LEFT_X = -HALF_W; // -4.00
            const WALL_RIGHT_X = HALF_W; // 4.00

            // Piso Visível
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH), new THREE.MeshStandardMaterial({ color: 0x17233B, roughness: 0.6 }));
            floor.position.set(0, 0, CENTER_Z);
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);

            // Malha de Teletransporte VR no Piso (Invisível para Raycast)
            teleportFloorMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH),
                new THREE.MeshBasicMaterial({ visible: false })
            );
            teleportFloorMesh.position.set(0, 0, CENTER_Z);
            teleportFloorMesh.rotation.x = -Math.PI / 2;
            teleportFloorMesh.name = 'teleportFloor';
            scene.add(teleportFloorMesh);
            window.teleportFloorMesh = teleportFloorMesh;

            // Todas as 4 paredes e o teto revestidos com os azulejos brancos (tileMat)
            // Parede de Fundo (Fechada exatamente em Z = -1.90)
            const backWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            backWall.position.set(0, ROOM_HEIGHT / 2, WALL_BACK_Z);
            backWall.receiveShadow = true;
            scene.add(backWall);

            // Parede Lateral Esquerda (Fechada em X = -4.00)
            const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            leftWall.position.set(WALL_LEFT_X, ROOM_HEIGHT / 2, CENTER_Z);
            leftWall.rotation.y = Math.PI / 2;
            leftWall.receiveShadow = true;
            scene.add(leftWall);

            // Parede Lateral Direita (Fechada em X = 4.00)
            const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            rightWall.position.set(WALL_RIGHT_X, ROOM_HEIGHT / 2, CENTER_Z);
            rightWall.rotation.y = -Math.PI / 2;
            rightWall.receiveShadow = true;
            scene.add(rightWall);

            // Parede Frontal dos Clientes (Fechada em Z = 3.10)
            const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            frontWall.position.set(0, ROOM_HEIGHT / 2, WALL_FRONT_Z);
            frontWall.rotation.y = Math.PI;
            frontWall.receiveShadow = true;
            scene.add(frontWall);

            // Teto (Fechamento Superior da Lanchonete em Y = 3.20 com azulejos brancos)
            const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH), tileMat);
            ceiling.position.set(0, ROOM_HEIGHT, CENTER_Z);
            ceiling.rotation.x = Math.PI / 2;
            scene.add(ceiling);"""

text, count = re.subn(room_pattern, new_room_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace room code'

# 2. Reconstrução completa de Geladeira, Coifa, Prateleiras, Estação de Cocção,
# Estação de Montagem, Estação de Preparo e Decoração de Paredes
stations_pattern = r'// Geladeira \(Encostada na parede esquerda e de fundo.*?scene\.add\(mesa3\);'

new_stations_code = """// Geladeira (Encostada na parede de fundo/esquerda em X = -2.80, Z = -1.85)
            const fridgeMesh = getAsset('geladeira');
            placeOnSurface(fridgeMesh, -2.80, 0.0, -1.85, 1.85);
            fridgeMesh.rotation.y = 0.0;
            scene.add(fridgeMesh);

            // Coifa / Exaustor suspensa exatamente acima do cooktop em X = -0.80, Y = 2.10, Z = -0.55
            const hoodGroup = new THREE.Group();
            const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.16, 0.55), stainlessMat);
            hoodCanopy.position.set(-0.80, 2.10, -0.55);
            hoodCanopy.castShadow = true;
            hoodGroup.add(hoodCanopy);

            const hoodDuct = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 1.10, 16), stainlessMat);
            hoodDuct.position.set(-0.80, 2.65, -0.55);
            hoodGroup.add(hoodDuct);
            scene.add(hoodGroup);

            // ==========================================
            // 3.A) PRATELEIRAS SUSPENSAS NA PAREDE DO FUNDO
            // ==========================================
            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            
            // Prateleira Esquerda
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf1.position.set(-0.75, 1.82, -1.78);
            shelf1.castShadow = true;
            scene.add(shelf1);

            // Prateleira Direita
            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf2.position.set(0.75, 1.82, -1.78);
            shelf2.castShadow = true;
            scene.add(shelf2);

            // Saleiro e Pimenta-do-reino
            const saleiroMesh = getAsset('saleiro');
            placeOnSurface(saleiroMesh, -0.90, 1.835, -1.78, 0.08);
            scene.add(saleiroMesh);

            const pimentaMesh = getAsset('pimenta-do-reino');
            placeOnSurface(pimentaMesh, -0.60, 1.835, -1.78, 0.08);
            scene.add(pimentaMesh);

            // Pote de Geleia, Manteiga de Amendoim e Garrafa
            const geleiaMesh = getAsset('pote-de-geleia');
            placeOnSurface(geleiaMesh, 0.55, 1.835, -1.78, 0.09);
            scene.add(geleiaMesh);

            const manteigaMesh = getAsset('manteiga-de-amendoim');
            placeOnSurface(manteigaMesh, 0.75, 1.835, -1.78, 0.09);
            scene.add(manteigaMesh);

            const garrafaMesh = getAsset('garrafa');
            placeOnSurface(garrafaMesh, 0.95, 1.835, -1.78, 0.16);
            scene.add(garrafaMesh);

            // Assadeira na prateleira esquerda contendo pães reservas (estoque visual)
            const assadeiraMesh = getAsset('assadeira');
            placeOnSurface(assadeiraMesh, -0.75, 1.835, -1.78, 0.32);
            scene.add(assadeiraMesh);

            // ==========================================
            // 3.B) ESTAÇÃO DE COCÇÃO (ESQUERDA - X = -0.80)
            // ==========================================
            // Cooktop em X = -0.80, Y = COUNTER_TOP_Y + 0.002, Z = -0.55
            const cooktopMesh = getAsset('cooktop');
            placeOnSurface(cooktopMesh, -0.80, COUNTER_TOP_Y + 0.002, -0.55, 0.46);
            scene.add(cooktopMesh);

            const cooktopBox = new THREE.Box3().setFromObject(cooktopMesh);
            const cooktopTopY = cooktopBox.max.y;

            // Frigideira colocada em cima do cooktop
            const skilletMesh = getAsset('frigideira');
            skilletMesh.rotation.set(0, 0, 0);
            placeOnSurface(skilletMesh, -0.80, cooktopTopY + 0.002, -0.55, 0.38);
            scene.add(skilletMesh);

            const skilletBox = new THREE.Box3().setFromObject(skilletMesh);
            window.skilletTopY = skilletBox.max.y;
            window.skilletCenter = new THREE.Vector3(-0.80, skilletBox.max.y + 0.002, -0.55);

            // Bandeja de carne crua à esquerda em X = -1.35, Z = -0.50
            const meatTray = new THREE.Mesh(
                new THREE.BoxGeometry(0.26, 0.012, 0.20),
                stainlessMat
            );
            placeOnSurface(meatTray, -1.35, LEVEL_1_Y, -0.50);
            meatTray.castShadow = true;
            meatTray.receiveShadow = true;
            scene.add(meatTray);

            const meatTrayBox = new THREE.Box3().setFromObject(meatTray);
            window.meatTrayTopY = meatTrayBox.max.y;
            window.meatTrayCenter = new THREE.Vector3(-1.35, meatTrayBox.max.y + 0.002, -0.50);

            // ==========================================
            // 3.B) ESTAÇÃO DE MONTAGEM (CENTRO PERFEITO - X = 0.00)
            // ==========================================
            // Mantém APENAS o tapete amarelo e o prato quadrado centralizado em X = 0.00, Z = -0.65
            const yellowMatMesh = new THREE.Mesh(
                new THREE.BoxGeometry(0.52, 0.006, 0.42),
                new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.3, flatShading: true })
            );
            placeOnSurface(yellowMatMesh, 0.00, LEVEL_1_Y, -0.65);
            yellowMatMesh.receiveShadow = true;
            scene.add(yellowMatMesh);

            // Prato Quadrado (100% livre e vazio para a montagem)
            const plateMesh = getAsset('prato-quadrado');
            plateMesh.rotation.set(0, 0, 0);
            placeOnSurface(plateMesh, 0.00, LEVEL_1_Y + 0.008, -0.65, 0.28);
            scene.add(plateMesh);

            const plateBox = new THREE.Box3().setFromObject(plateMesh);
            window.plateSurfaceTopY = plateBox.max.y;

            // ==========================================
            // 3.B) ESTAÇÃO DE PREPARO (DIREITA - X = 0.80)
            // ==========================================
            // Tábua de Corte posicionada em X = 0.80, Z = -0.60
            const cuttingBoard = new THREE.Mesh(
                new THREE.BoxGeometry(0.48, 0.02, 0.36),
                new THREE.MeshStandardMaterial({ color: 0xB5651D, roughness: 0.6, flatShading: true })
            );
            placeOnSurface(cuttingBoard, 0.80, LEVEL_1_Y, -0.60, 0.48);
            cuttingBoard.rotation.y = 0;
            cuttingBoard.castShadow = true;
            cuttingBoard.receiveShadow = true;
            scene.add(cuttingBoard);

            const cuttingBoardBox = new THREE.Box3().setFromObject(cuttingBoard);
            window.boardTopY = cuttingBoardBox.max.y;

            // Faca de Cozinha (deitada na horizontal sobre a bancada ao lado da tábua)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.12, LEVEL_1_Y, -0.60, 0.22);
            facaSimples.rotation.x = Math.PI / 2;
            facaSimples.rotation.z = Math.PI / 6;
            scene.add(facaSimples);

            // Tomate e fatia alinhados atrás da tábua
            const tomatoMesh = getAsset('tomate');
            placeOnSurface(tomatoMesh, 0.74, LEVEL_1_Y, -0.80, 0.09);
            scene.add(tomatoMesh);

            const tomatoSlicedMesh = getAsset('tomate-cortado');
            placeOnSurface(tomatoSlicedMesh, 0.86, LEVEL_1_Y, -0.80, 0.09);
            scene.add(tomatoSlicedMesh);

            // Bisnagas de Ketchup e Mostarda alinhadas ao fundo em Z = -0.85
            const ketchupBottle = createSqueezeBottleMesh(0xD32F2F); placeOnSurface(ketchupBottle, 0.45, LEVEL_1_Y, -0.85); scene.add(ketchupBottle);
            const mustardBottle = createSqueezeBottleMesh(0xFFD700); placeOnSurface(mustardBottle, 0.57, LEVEL_1_Y, -0.85); scene.add(mustardBottle);

            const espatulaMesh = getAsset('espatula');
            placeOnSurface(espatulaMesh, 1.00, LEVEL_1_Y, -0.85, 0.24);
            espatulaMesh.rotation.y = Math.PI / 4;
            scene.add(espatulaMesh);

            // 3 Copos Vermelhos juntos no canto direito do balcão (X = 1.40, Z = -0.80), longe do prato central
            const cup1 = createCupMesh(); placeOnSurface(cup1, 1.35, LEVEL_1_Y, -0.82); scene.add(cup1);
            const cup2 = createCupMesh(); placeOnSurface(cup2, 1.45, LEVEL_1_Y, -0.82); scene.add(cup2);
            const cup3 = createCupMesh(); placeOnSurface(cup3, 1.40, LEVEL_1_Y, -0.74); scene.add(cup3);

            // Torradeira e Papel Towel encostados no canto direito em X = 1.30, Z = -0.50
            const toasterMesh = getAsset('torradeira');
            placeOnSurface(toasterMesh, 1.25, LEVEL_1_Y, -0.50, 0.22);
            scene.add(toasterMesh);

            const papelToalhaMesh = getAsset('papel-toalha');
            placeOnSurface(papelToalhaMesh, 1.45, LEVEL_1_Y, -0.50, 0.22);
            scene.add(papelToalhaMesh);

            // ==========================================
            // 3.C) CHÃO E PISO (Lixeira encostada à lateral)
            // ==========================================
            const lixeiraMesh = getAsset('lixeira');
            placeOnSurface(lixeiraMesh, 2.80, 0.0, -0.50, 0.45);
            scene.add(lixeiraMesh);

            // ==========================================
            // 3.D) DECORAÇÃO E PAREDES (PROPORÇÕES E ALTURAS CORRETAS)
            // ==========================================
            // 1. Lâmpadas Pendentes sobre a bancada
            const lampada1 = getAsset('lampada');
            placeOnSurface(lampada1, -0.20, 1.75, -0.65, 0.45);
            scene.add(lampada1);

            const lampLight1 = new THREE.PointLight(0xFFF1C5, 1.2, 3.0);
            lampLight1.position.set(-0.20, 1.75, -0.65);
            scene.add(lampLight1);

            const lampada2 = getAsset('lampada');
            placeOnSurface(lampada2, 0.70, 1.75, -0.65, 0.45);
            scene.add(lampada2);

            const lampLight2 = new THREE.PointLight(0xFFF1C5, 1.2, 3.0);
            lampLight2.position.set(0.70, 1.75, -0.65);
            scene.add(lampLight2);

            // 2. Janela fixada na parede lateral esquerda em X = -3.95, Y = 1.80, Z = 0.0, rotation.y = Math.PI / 2
            const janela1 = getAsset('janela');
            placeOnSurface(janela1, -3.95, 1.80, 0.0, 1.2);
            janela1.rotation.y = Math.PI / 2;
            scene.add(janela1);

            // 3. Porta encostada na parede lateral direita em X = 3.95, Y = 0.0, Z = 1.0, rotation.y = -Math.PI / 2
            const portaMesh = getAsset('porta');
            placeOnSurface(portaMesh, 3.95, 0.0, 1.0, 2.2);
            portaMesh.rotation.y = -Math.PI / 2;
            scene.add(portaMesh);

            // Placa decorativa "SAÍDA / EXIT" acima da porta
            const exitSign = createExitSignMesh();
            placeOnSurface(exitSign, 3.95, 2.28, 1.0);
            exitSign.rotation.y = -Math.PI / 2;
            scene.add(exitSign);

            // 4. Parede Frontal (De frente para o balcão - Z = 3.08)
            // Quadro Negro: Centralizado na altura dos olhos (Y = 1.80), amplo (escala 1.50)
            const quadroMesh = getAsset('quadro-negro');
            placeOnSurface(quadroMesh, 0.0, 1.80, 3.08, 1.50);
            quadroMesh.rotation.y = Math.PI;
            scene.add(quadroMesh);

            // Armários: 3 armários alinhados no alto em Y = 2.50, bem acima do quadro negro
            const armario1 = getAsset('armario-cozinha');
            placeOnSurface(armario1, -1.20, 2.50, 3.08, 0.85);
            armario1.rotation.y = Math.PI;
            scene.add(armario1);

            const armario2 = getAsset('armario-cozinha');
            placeOnSurface(armario2, 0.00, 2.50, 3.08, 0.85);
            armario2.rotation.y = Math.PI;
            scene.add(armario2);

            const armario3 = getAsset('armario-cozinha');
            placeOnSurface(armario3, 1.20, 2.50, 3.08, 0.85);
            armario3.rotation.y = Math.PI;
            scene.add(armario3);

            // Relógio: No topo central da parede em Y = 2.90
            const relogioMesh = getAsset('relogio');
            placeOnSurface(relogioMesh, 0.0, 2.90, 3.08, 0.40);
            relogioMesh.rotation.y = Math.PI;
            scene.add(relogioMesh);

            // 5. Mesas do Salão (2 mesas com distância de segurança do balcão)
            const mesa1 = getAsset('mesa-com-comida');
            placeOnSurface(mesa1, -2.0, 0.0, 1.80, 1.0);
            scene.add(mesa1);

            const mesa2 = getAsset('mesa-com-comida');
            placeOnSurface(mesa2, 2.0, 0.0, 1.80, 1.0);
            scene.add(mesa2);"""

text, count = re.subn(stations_pattern, new_stations_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace stations code'

# 3. Painel de Receitas (TV) encostado no centro da parede de fundo em X = 0.00, Y = 2.00, Z = -1.88
recipe_board_pattern = r'recipeBoardMesh\.position\.set\(0\.00,\s*[0-9\.]+,\s*-[0-9\.]+\);'
assert re.search(recipe_board_pattern, text), 'recipeBoardMesh pattern not found'
text = re.sub(recipe_board_pattern, 'recipeBoardMesh.position.set(0.00, 2.00, -1.88);', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success! Layout completely restored.')
