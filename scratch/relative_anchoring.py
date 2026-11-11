import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Room Dimensions and Walls setup with window.* references so all objects can calculate relatively
walls_pattern = r'// DIMENS.*?scene\.add\(ceiling\);'
new_walls_code = """// DIMENSÕES ESTRUTURAIS FIXAS DO CENÁRIO (SALA GRANDE DE LANCHONETE)
            // ==========================================
            const ROOM_WIDTH = 14.0;
            const ROOM_DEPTH = 10.0;
            const ROOM_HEIGHT = 3.8;

            const WALL_BACK_Z = -2.20;
            const WALL_FRONT_Z = 7.80;
            const CENTER_Z = (WALL_BACK_Z + WALL_FRONT_Z) / 2; // 2.80
            const HALF_W = ROOM_WIDTH / 2; // 7.00
            const WALL_LEFT_X = -HALF_W; // -7.00
            const WALL_RIGHT_X = HALF_W; // 7.00

            // Piso Visível Cobrindo Toda a Sala Grande
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH), new THREE.MeshStandardMaterial({ color: 0x17233B, roughness: 0.6 }));
            floor.position.set(0, 0, CENTER_Z);
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);
            window.roomFloor = floor;

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
            // Parede de Fundo (Fechada em Z = -2.20)
            const backWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            backWall.position.set(0, ROOM_HEIGHT / 2, WALL_BACK_Z);
            backWall.receiveShadow = true;
            scene.add(backWall);
            window.backWall = backWall;

            // Parede Lateral Esquerda (Fechada em X = -7.00)
            const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            leftWall.position.set(WALL_LEFT_X, ROOM_HEIGHT / 2, CENTER_Z);
            leftWall.rotation.y = Math.PI / 2;
            leftWall.receiveShadow = true;
            scene.add(leftWall);
            window.leftWall = leftWall;

            // Parede Lateral Direita (Fechada em X = 7.00)
            const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            rightWall.position.set(WALL_RIGHT_X, ROOM_HEIGHT / 2, CENTER_Z);
            rightWall.rotation.y = -Math.PI / 2;
            rightWall.receiveShadow = true;
            scene.add(rightWall);
            window.rightWall = rightWall;

            // Parede Frontal do Salão (Fechada em Z = 7.80)
            const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            frontWall.position.set(0, ROOM_HEIGHT / 2, WALL_FRONT_Z);
            frontWall.rotation.y = Math.PI;
            frontWall.receiveShadow = true;
            scene.add(frontWall);
            window.frontWall = frontWall;

            // Teto (Fechamento Superior da Lanchonete em Y = 3.80 com azulejos brancos)
            const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH), tileMat);
            ceiling.position.set(0, ROOM_HEIGHT, CENTER_Z);
            ceiling.rotation.x = Math.PI / 2;
            scene.add(ceiling);
            window.roomCeiling = ceiling;"""

text, count = re.subn(walls_pattern, new_walls_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace walls code'

# 2. Geladeira encostada 100% no chão e na parede de fundo:
# Y = 0.0, Z = backWall.position.z + 0.35, X = -3.2
# Coifa em X = -0.80, Y = 2.10, Z = -0.55
# Prateleiras em Z = backWall.position.z + 0.15 (sem colidir com a TV de receitas)
# Estação de cocção, montagem, preparo e decoração frontal/lateral
stations_pattern = r'// Geladeira \(Encostada na parede do fundo/esquerda.*?scene\.add\(mesa4\);'

new_stations_code = """// Geladeira: 100% no chão (Y = 0.0) e encostada na parede de fundo (Z = backWall.position.z + 0.35, X = -3.2)
            const fridgeMesh = getAsset('geladeira');
            placeOnSurface(fridgeMesh, -3.20, 0.0, backWall.position.z + 0.35, 1.85);
            fridgeMesh.rotation.y = 0.0;
            scene.add(fridgeMesh);

            // Coifa / Exaustor suspensa exatamente acima do fogão em X = -0.80, Y = 2.10, Z = -0.55
            const hoodGroup = new THREE.Group();
            const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.16, 0.55), stainlessMat);
            hoodCanopy.position.set(-0.80, 2.10, -0.55);
            hoodCanopy.castShadow = true;
            hoodGroup.add(hoodCanopy);

            const hoodDuct = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 1.70, 16), stainlessMat);
            hoodDuct.position.set(-0.80, 2.95, -0.55);
            hoodGroup.add(hoodDuct);
            scene.add(hoodGroup);

            // ==========================================
            // 3.A) PRATELEIRAS DE MADEIRA NA PAREDE DO FUNDO (Z = backWall.position.z + 0.15)
            // Afastadas do centro (X = 0) para não colidir com o Painel de Receitas/TV
            // ==========================================
            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            const SHELF_Z = backWall.position.z + 0.15;
            
            // Prateleira Esquerda
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf1.position.set(-1.00, 1.82, SHELF_Z);
            shelf1.castShadow = true;
            scene.add(shelf1);

            // Prateleira Direita
            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf2.position.set(1.00, 1.82, SHELF_Z);
            shelf2.castShadow = true;
            scene.add(shelf2);

            // Saleiro e Pimenta-do-reino sobre a prateleira esquerda
            const saleiroMesh = getAsset('saleiro');
            placeOnSurface(saleiroMesh, -1.20, 1.835, SHELF_Z, 0.08);
            scene.add(saleiroMesh);

            const pimentaMesh = getAsset('pimenta-do-reino');
            placeOnSurface(pimentaMesh, -0.80, 1.835, SHELF_Z, 0.08);
            scene.add(pimentaMesh);

            // Pote de Geleia, Manteiga de Amendoim e Garrafa sobre a prateleira direita
            const geleiaMesh = getAsset('pote-de-geleia');
            placeOnSurface(geleiaMesh, 0.70, 1.835, SHELF_Z, 0.09);
            scene.add(geleiaMesh);

            const manteigaMesh = getAsset('manteiga-de-amendoim');
            placeOnSurface(manteigaMesh, 0.95, 1.835, SHELF_Z, 0.09);
            scene.add(manteigaMesh);

            const garrafaMesh = getAsset('garrafa');
            placeOnSurface(garrafaMesh, 1.20, 1.835, SHELF_Z, 0.16);
            scene.add(garrafaMesh);

            // Assadeira na prateleira esquerda com pães reservas
            const assadeiraMesh = getAsset('assadeira');
            placeOnSurface(assadeiraMesh, -1.00, 1.835, SHELF_Z, 0.32);
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

            // Frigideira assentada sobre o cooktop em X = -0.80, Y = COUNTER_TOP_Y + 0.02, Z = -0.55
            const skilletMesh = getAsset('frigideira');
            skilletMesh.rotation.set(0, 0, 0);
            placeOnSurface(skilletMesh, -0.80, COUNTER_TOP_Y + 0.02, -0.55, 0.38);
            scene.add(skilletMesh);

            const skilletBox = new THREE.Box3().setFromObject(skilletMesh);
            window.skilletTopY = skilletBox.max.y;
            window.skilletCenter = new THREE.Vector3(-0.80, skilletBox.max.y + 0.002, -0.55);

            // Bandeja de carne crua à esquerda em X = -1.35, Y = LEVEL_1_Y, Z = -0.50
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
            // Tapete amarelo e prato quadrado centralizado em X = 0.00, Z = -0.65
            const yellowMatMesh = new THREE.Mesh(
                new THREE.BoxGeometry(0.52, 0.006, 0.42),
                new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.3, flatShading: true })
            );
            placeOnSurface(yellowMatMesh, 0.00, LEVEL_1_Y, -0.65);
            yellowMatMesh.receiveShadow = true;
            scene.add(yellowMatMesh);

            // Prato Central totalmente limpo sobre o tapete amarelo em X = 0.0, Z = -0.65
            const plateMesh = getAsset('prato-quadrado');
            plateMesh.rotation.set(0, 0, 0);
            placeOnSurface(plateMesh, 0.00, LEVEL_1_Y + 0.008, -0.65, 0.28);
            scene.add(plateMesh);

            const plateBox = new THREE.Box3().setFromObject(plateMesh);
            window.plateSurfaceTopY = plateBox.max.y;

            // ==========================================
            // 3.B) ESTAÇÃO DE PREPARO (DIREITA - X = 0.80)
            // ==========================================
            // Tábua de corte em X = 0.80, Z = -0.60
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

            // Faca deitada de lado sobre a bancada (rotation.z = Math.PI / 2)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.12, LEVEL_1_Y, -0.60, 0.22);
            facaSimples.rotation.set(0, 0, Math.PI / 2);
            scene.add(facaSimples);

            // Tomate e fatia alinhados atrás da tábua
            const tomatoMesh = getAsset('tomate');
            placeOnSurface(tomatoMesh, 0.74, LEVEL_1_Y, -0.80, 0.09);
            scene.add(tomatoMesh);

            const tomatoSlicedMesh = getAsset('tomate-cortado');
            placeOnSurface(tomatoSlicedMesh, 0.86, LEVEL_1_Y, -0.80, 0.09);
            scene.add(tomatoSlicedMesh);

            // Bisnagas de Ketchup e Mostarda alinhadas no fundo (Z = -0.85)
            const ketchupBottle = createSqueezeBottleMesh(0xD32F2F); placeOnSurface(ketchupBottle, 0.45, LEVEL_1_Y, -0.85); scene.add(ketchupBottle);
            const mustardBottle = createSqueezeBottleMesh(0xFFD700); placeOnSurface(mustardBottle, 0.57, LEVEL_1_Y, -0.85); scene.add(mustardBottle);

            const espatulaMesh = getAsset('espatula');
            placeOnSurface(espatulaMesh, 1.00, LEVEL_1_Y, -0.85, 0.24);
            espatulaMesh.rotation.y = Math.PI / 4;
            scene.add(espatulaMesh);

            // Copos vermelhos, torradeira e rolo de papel no canto direito da bancada (X = 1.60 a 1.76)
            const cup1 = createCupMesh(); placeOnSurface(cup1, 1.62, LEVEL_1_Y, -0.80); scene.add(cup1);
            const cup2 = createCupMesh(); placeOnSurface(cup2, 1.72, LEVEL_1_Y, -0.80); scene.add(cup2);
            const cup3 = createCupMesh(); placeOnSurface(cup3, 1.67, LEVEL_1_Y, -0.72); scene.add(cup3);

            const toasterMesh = getAsset('torradeira');
            placeOnSurface(toasterMesh, 1.62, LEVEL_1_Y, -0.50, 0.22);
            scene.add(toasterMesh);

            const papelToalhaMesh = getAsset('papel-toalha');
            placeOnSurface(papelToalhaMesh, 1.76, LEVEL_1_Y, -0.50, 0.22);
            scene.add(papelToalhaMesh);

            // ==========================================
            // 3.C) CHÃO E PISO (Lixeira encostada à lateral)
            // ==========================================
            const lixeiraMesh = getAsset('lixeira');
            placeOnSurface(lixeiraMesh, 3.20, 0.0, -0.50, 0.45);
            scene.add(lixeiraMesh);

            // ==========================================
            // 3.D) DECORAÇÃO E FIXAÇÃO RELATIVA ÀS PAREDES REAIS
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

            // 2. Janelas nas Paredes Lateral Esquerda e Direita (Sem flutuar)
            // Janela Esquerda: X = leftWall.position.x + 0.05, Y = 1.80, Z = 0.0, rotation.y = Math.PI / 2
            const janela1 = getAsset('janela');
            placeOnSurface(janela1, leftWall.position.x + 0.05, 1.80, 0.0, 1.3);
            janela1.rotation.y = Math.PI / 2;
            scene.add(janela1);

            // Janela Direita: X = rightWall.position.x - 0.05, Y = 1.80, Z = 0.0, rotation.y = -Math.PI / 2
            const janela2 = getAsset('janela');
            placeOnSurface(janela2, rightWall.position.x - 0.05, 1.80, 0.0, 1.3);
            janela2.rotation.y = -Math.PI / 2;
            scene.add(janela2);

            // 3. Porta assentada no chão na parede lateral direita
            const portaMesh = getAsset('porta');
            placeOnSurface(portaMesh, rightWall.position.x - 0.05, 0.0, 4.0, 2.2);
            portaMesh.rotation.y = -Math.PI / 2;
            scene.add(portaMesh);

            // Placa "SAÍDA / EXIT" acima da porta
            const exitSign = createExitSignMesh();
            placeOnSurface(exitSign, rightWall.position.x - 0.05, 2.28, 4.0);
            exitSign.rotation.y = -Math.PI / 2;
            scene.add(exitSign);

            // 4. Parede Frontal (Z = frontWall.position.z):
            // Armários: 3 módulos num único bloco contínuo no alto: Y = 2.60, Z = frontWall.position.z - 0.15
            const armario1 = getAsset('armario-cozinha');
            placeOnSurface(armario1, -0.80, 2.60, frontWall.position.z - 0.15, 0.80);
            armario1.rotation.y = Math.PI;
            scene.add(armario1);

            const armario2 = getAsset('armario-cozinha');
            placeOnSurface(armario2, 0.00, 2.60, frontWall.position.z - 0.15, 0.80);
            armario2.rotation.y = Math.PI;
            scene.add(armario2);

            const armario3 = getAsset('armario-cozinha');
            placeOnSurface(armario3, 0.80, 2.60, frontWall.position.z - 0.15, 0.80);
            armario3.rotation.y = Math.PI;
            scene.add(armario3);

            // Quadro Negro: Centralizado abaixo dos armários em Y = 1.75, Z = frontWall.position.z - 0.05, escala 1.6
            const quadroMesh = getAsset('quadro-negro');
            placeOnSurface(quadroMesh, 0.0, 1.75, frontWall.position.z - 0.05, 1.60);
            quadroMesh.rotation.y = Math.PI;
            scene.add(quadroMesh);

            // Relógio: Centralizado acima dos armários em Y = 3.00, Z = frontWall.position.z - 0.05
            const relogioMesh = getAsset('relogio');
            placeOnSurface(relogioMesh, 0.0, 3.00, frontWall.position.z - 0.05, 0.40);
            relogioMesh.rotation.y = Math.PI;
            scene.add(relogioMesh);

            // 5. Mesas de Clientes no Salão
            const mesa1 = getAsset('mesa-com-comida');
            placeOnSurface(mesa1, -3.20, 0.0, 2.50, 1.10);
            scene.add(mesa1);

            const mesa2 = getAsset('mesa-com-comida');
            placeOnSurface(mesa2, 3.20, 0.0, 2.50, 1.10);
            scene.add(mesa2);

            const mesa3 = getAsset('mesa-com-comida');
            placeOnSurface(mesa3, -3.20, 0.0, 4.80, 1.10);
            scene.add(mesa3);

            const mesa4 = getAsset('mesa-com-comida');
            placeOnSurface(mesa4, 3.20, 0.0, 4.80, 1.10);
            scene.add(mesa4);"""

text, count = re.subn(stations_pattern, new_stations_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace stations code'

# 3. Painel de Receitas (TV) fixado diretamente na parede em Z = backWall.position.z + 0.02, Y = 2.10, X = 0.0
recipe_board_pattern = r'recipeBoardMesh\.position\.set\(0\.00,\s*[0-9\.]+,\s*-[0-9\.]+\);'
assert re.search(recipe_board_pattern, text), 'recipeBoardMesh pattern not found'
new_recipe_board_set = """const targetBackWallZ = (window.backWall ? window.backWall.position.z : -2.20);
recipeBoardMesh.position.set(0.00, 2.10, targetBackWallZ + 0.02);"""
text = re.sub(recipe_board_pattern, new_recipe_board_set, text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success! All objects relative to actual wall and floor meshes.')
