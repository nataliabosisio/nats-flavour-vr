import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Dimensões Fixas do Espaço Ampliado (Sala Grande)
# ROOM_WIDTH = 14.0
# ROOM_DEPTH = 10.0
# ROOM_HEIGHT = 3.8
# Parede do Fundo (Atrás da bancada): Z = -2.20
# Parede Frontal (Frente do salão): Z = 7.80
# Parede Esquerda: X = -7.00
# Parede Direita: X = 7.00
# Teto (ceiling), chão (floor) e todas as 4 paredes totalmente fechados com azulejos brancos (tileMat).

room_pattern = r'// DIMENS.*?scene\.add\(ceiling\);'
new_room_code = """// DIMENSÕES FIXAS DO ESPAÇO AMPLIADO (SALA GRANDE DE LANCHONETE)
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

            // Todas as 4 paredes e o teto totalmente fechados com azulejos brancos (tileMat)
            // Parede de Fundo (Fechada em Z = -2.20)
            const backWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            backWall.position.set(0, ROOM_HEIGHT / 2, WALL_BACK_Z);
            backWall.receiveShadow = true;
            scene.add(backWall);

            // Parede Lateral Esquerda (Fechada em X = -7.00)
            const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            leftWall.position.set(WALL_LEFT_X, ROOM_HEIGHT / 2, CENTER_Z);
            leftWall.rotation.y = Math.PI / 2;
            leftWall.receiveShadow = true;
            scene.add(leftWall);

            // Parede Lateral Direita (Fechada em X = 7.00)
            const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            rightWall.position.set(WALL_RIGHT_X, ROOM_HEIGHT / 2, CENTER_Z);
            rightWall.rotation.y = -Math.PI / 2;
            rightWall.receiveShadow = true;
            scene.add(rightWall);

            // Parede Frontal do Salão (Fechada em Z = 7.80)
            const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            frontWall.position.set(0, ROOM_HEIGHT / 2, WALL_FRONT_Z);
            frontWall.rotation.y = Math.PI;
            frontWall.receiveShadow = true;
            scene.add(frontWall);

            // Teto (Fechamento Superior da Lanchonete em Y = 3.80 com azulejos brancos)
            const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH), tileMat);
            ceiling.position.set(0, ROOM_HEIGHT, CENTER_Z);
            ceiling.rotation.x = Math.PI / 2;
            scene.add(ceiling);"""

text, count = re.subn(room_pattern, new_room_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace room code'

# 2. Geladeira, Coifa, Prateleiras, Cocção, Montagem, Preparo, Janelas, Porta e Salão
stations_pattern = r'// Geladeira \(Encostada na parede de fundo/esquerda.*?scene\.add\(mesa2\);'

new_stations_code = """// Geladeira (Encostada na parede do fundo/esquerda em X = -3.50, Y = 0.0, Z = -2.15)
            const fridgeMesh = getAsset('geladeira');
            placeOnSurface(fridgeMesh, -3.50, 0.0, -2.15, 1.85);
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
            // 3.A) PRATELEIRAS SUSPENSAS NA PAREDE DO FUNDO (Z = -2.18)
            // ==========================================
            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            
            // Prateleira Esquerda
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf1.position.set(-0.75, 1.82, -2.07);
            shelf1.castShadow = true;
            scene.add(shelf1);

            // Prateleira Direita
            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf2.position.set(0.75, 1.82, -2.07);
            shelf2.castShadow = true;
            scene.add(shelf2);

            // Saleiro e Pimenta-do-reino
            const saleiroMesh = getAsset('saleiro');
            placeOnSurface(saleiroMesh, -0.90, 1.835, -2.07, 0.08);
            scene.add(saleiroMesh);

            const pimentaMesh = getAsset('pimenta-do-reino');
            placeOnSurface(pimentaMesh, -0.60, 1.835, -2.07, 0.08);
            scene.add(pimentaMesh);

            // Pote de Geleia, Manteiga de Amendoim e Garrafa
            const geleiaMesh = getAsset('pote-de-geleia');
            placeOnSurface(geleiaMesh, 0.55, 1.835, -2.07, 0.09);
            scene.add(geleiaMesh);

            const manteigaMesh = getAsset('manteiga-de-amendoim');
            placeOnSurface(manteigaMesh, 0.75, 1.835, -2.07, 0.09);
            scene.add(manteigaMesh);

            const garrafaMesh = getAsset('garrafa');
            placeOnSurface(garrafaMesh, 0.95, 1.835, -2.07, 0.16);
            scene.add(garrafaMesh);

            // Assadeira na prateleira esquerda com pães reservas
            const assadeiraMesh = getAsset('assadeira');
            placeOnSurface(assadeiraMesh, -0.75, 1.835, -2.07, 0.32);
            scene.add(assadeiraMesh);

            // ==========================================
            // 3.B) RESTAURAÇÃO COMPLETA DA ESTAÇÃO DE COCÇÃO (ESQUERDA - X = -0.80)
            // ==========================================
            // Cooktop / Fogão em X = -0.80, Y = COUNTER_TOP_Y + 0.002, Z = -0.55
            const cooktopMesh = getAsset('cooktop');
            placeOnSurface(cooktopMesh, -0.80, COUNTER_TOP_Y + 0.002, -0.55, 0.46);
            scene.add(cooktopMesh);

            // Frigideira posicionada sobre o cooktop em X = -0.80, Y = COUNTER_TOP_Y + 0.02, Z = -0.55
            const skilletMesh = getAsset('frigideira');
            skilletMesh.rotation.set(0, 0, 0);
            placeOnSurface(skilletMesh, -0.80, COUNTER_TOP_Y + 0.02, -0.55, 0.38);
            scene.add(skilletMesh);

            const skilletBox = new THREE.Box3().setFromObject(skilletMesh);
            window.skilletTopY = skilletBox.max.y;
            window.skilletCenter = new THREE.Vector3(-0.80, skilletBox.max.y + 0.002, -0.55);

            // Bandeja de Carne Crua posicionada à esquerda em X = -1.35, Y = LEVEL_1_Y, Z = -0.50
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
            // Exclusivamente com o tapete amarelo e o prato quadrado (SEM copos ou objetos em cima)
            const yellowMatMesh = new THREE.Mesh(
                new THREE.BoxGeometry(0.52, 0.006, 0.42),
                new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.3, flatShading: true })
            );
            placeOnSurface(yellowMatMesh, 0.00, LEVEL_1_Y, -0.65);
            yellowMatMesh.receiveShadow = true;
            scene.add(yellowMatMesh);

            // Prato Quadrado (100% livre e limpo para montagem do hambúrguer)
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

            // Faca deitada de lado na horizontal (rotation.z = Math.PI / 2)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.12, LEVEL_1_Y, -0.60, 0.22);
            facaSimples.rotation.set(0, 0, Math.PI / 2);
            scene.add(facaSimples);

            // Tomate e fatia alinhados organizadamente atrás da tábua
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

            // Copos vermelhos, torradeira e rolo de papel organizados no canto direito da bancada (X = 1.60 a 1.90)
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
            // 3.D) ELEMENTOS DECORATIVOS ADICIONAIS & PORTA / JANELAS / SALÃO
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

            // 2. Janelas na linha normal dos olhos (Y = 1.80) longe do teto
            // Janela 1 (Parede Esquerda): placeOnSurface(janela1, -6.95, 1.80, 1.0, 1.3), rotação Y = Math.PI / 2
            const janela1 = getAsset('janela');
            placeOnSurface(janela1, -6.95, 1.80, 1.0, 1.3);
            janela1.rotation.y = Math.PI / 2;
            scene.add(janela1);

            // Janela 2 (Parede Direita): placeOnSurface(janela2, 6.95, 1.80, 1.0, 1.3), rotação Y = -Math.PI / 2
            const janela2 = getAsset('janela');
            placeOnSurface(janela2, 6.95, 1.80, 1.0, 1.3);
            janela2.rotation.y = -Math.PI / 2;
            scene.add(janela2);

            // 3. Porta assentada no chão na parede lateral direita em placeOnSurface(portaMesh, 6.95, 0.0, 4.0, 2.2), rotação Y = -Math.PI / 2
            const portaMesh = getAsset('porta');
            placeOnSurface(portaMesh, 6.95, 0.0, 4.0, 2.2);
            portaMesh.rotation.y = -Math.PI / 2;
            scene.add(portaMesh);

            // Placa "SAÍDA / EXIT" acima da porta
            const exitSign = createExitSignMesh();
            placeOnSurface(exitSign, 6.95, 2.28, 4.0);
            exitSign.rotation.y = -Math.PI / 2;
            scene.add(exitSign);

            // 4. Decoração da Parede Frontal (Z = 7.75)
            // Quadro Negro: Centralizado em X = 0.0, Y = 1.80, Z = 7.75 com escala 1.80
            const quadroMesh = getAsset('quadro-negro');
            placeOnSurface(quadroMesh, 0.0, 1.80, 7.75, 1.80);
            quadroMesh.rotation.y = Math.PI;
            scene.add(quadroMesh);

            // Relógio: No alto em X = 0.0, Y = 2.90, Z = 7.75
            const relogioMesh = getAsset('relogio');
            placeOnSurface(relogioMesh, 0.0, 2.90, 7.75, 0.40);
            relogioMesh.rotation.y = Math.PI;
            scene.add(relogioMesh);

            // 3 Armários: Alinhados no alto em Y = 2.80 (Z = 7.75)
            const armario1 = getAsset('armario-cozinha');
            placeOnSurface(armario1, -1.80, 2.80, 7.75, 0.85);
            armario1.rotation.y = Math.PI;
            scene.add(armario1);

            const armario2 = getAsset('armario-cozinha');
            placeOnSurface(armario2, 1.20, 2.80, 7.75, 0.85);
            armario2.rotation.y = Math.PI;
            scene.add(armario2);

            const armario3 = getAsset('armario-cozinha');
            placeOnSurface(armario3, 2.05, 2.80, 7.75, 0.85);
            armario3.rotation.y = Math.PI;
            scene.add(armario3);

            // 5. Mesas do Salão (4 mesas com comida pelo salão espaçoso de clientes entre Z = 2.0 e Z = 5.0)
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

# 3. Painel de Receitas (TV) encostado no centro da parede de fundo (Z = -2.18)
recipe_board_pattern = r'recipeBoardMesh\.position\.set\(0\.00,\s*[0-9\.]+,\s*-[0-9\.]+\);'
assert re.search(recipe_board_pattern, text), 'recipeBoardMesh pattern not found'
text = re.sub(recipe_board_pattern, 'recipeBoardMesh.position.set(0.00, 2.00, -2.18);', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success! Restored and fixed large diner environment.')
