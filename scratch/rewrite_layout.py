import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Definição Prévia das Paredes (Executar PRIMEIRO):
# const ROOM_W = 14.0; const ROOM_D = 10.0; const ROOM_H = 3.8;
# backWall.position.set(0, ROOM_H / 2, -5.0);
# frontWall.position.set(0, ROOM_H / 2, 5.0);
# leftWall.position.set(-7.0, ROOM_H / 2, 0);
# rightWall.position.set(7.0, ROOM_H / 2, 0);

walls_pattern = r'// DIMENS.*?scene\.add\(ceiling\);'
new_walls_code = """// ==========================================
            // 1. DEFINIÇÃO PRÉVIA DAS PAREDES (EXECUTAR PRIMEIRO)
            // ==========================================
            const ROOM_W = 14.0;
            const ROOM_D = 10.0;
            const ROOM_H = 3.8;

            const ROOM_WIDTH = ROOM_W;
            const ROOM_DEPTH = ROOM_D;
            const ROOM_HEIGHT = ROOM_H;

            // Piso Visível Cobrindo Toda a Sala Grande
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_W, ROOM_D), new THREE.MeshStandardMaterial({ color: 0x17233B, roughness: 0.6 }));
            floor.position.set(0, 0, 0);
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);
            window.roomFloor = floor;

            // Malha de Teletransporte VR no Piso (Invisível para Raycast)
            teleportFloorMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(ROOM_W, ROOM_D),
                new THREE.MeshBasicMaterial({ visible: false })
            );
            teleportFloorMesh.position.set(0, 0, 0);
            teleportFloorMesh.rotation.x = -Math.PI / 2;
            teleportFloorMesh.name = 'teleportFloor';
            scene.add(teleportFloorMesh);
            window.teleportFloorMesh = teleportFloorMesh;

            // Paredes e Teto Revestidos Uniformemente com Azulejos Brancos (tileMat)
            // Parede de Fundo (Fixada em Z = -5.0)
            const backWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_W, ROOM_H), tileMat);
            backWall.position.set(0, ROOM_H / 2, -5.0);
            backWall.receiveShadow = true;
            scene.add(backWall);
            window.backWall = backWall;

            // Parede Frontal (Fixada em Z = 5.0)
            const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_W, ROOM_H), tileMat);
            frontWall.position.set(0, ROOM_H / 2, 5.0);
            frontWall.rotation.y = Math.PI;
            frontWall.receiveShadow = true;
            scene.add(frontWall);
            window.frontWall = frontWall;

            // Parede Lateral Esquerda (Fixada em X = -7.0)
            const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_D, ROOM_H), tileMat);
            leftWall.position.set(-7.0, ROOM_H / 2, 0);
            leftWall.rotation.y = Math.PI / 2;
            leftWall.receiveShadow = true;
            scene.add(leftWall);
            window.leftWall = leftWall;

            // Parede Lateral Direita (Fixada em X = 7.0)
            const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_D, ROOM_H), tileMat);
            rightWall.position.set(7.0, ROOM_H / 2, 0);
            rightWall.rotation.y = -Math.PI / 2;
            rightWall.receiveShadow = true;
            scene.add(rightWall);
            window.rightWall = rightWall;

            // Teto (Fechamento Superior da Lanchonete em Y = 3.8 com azulejos brancos)
            const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_W, ROOM_D), tileMat);
            ceiling.position.set(0, ROOM_H, 0);
            ceiling.rotation.x = Math.PI / 2;
            scene.add(ceiling);
            window.roomCeiling = ceiling;"""

text, count = re.subn(walls_pattern, new_walls_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace walls code'

# 2. Geladeira e Prateleiras no fundo
shelves_pattern = r'// Geladeira: 100% no chão.*?scene\.add\(assadeiraMesh\);'
new_shelves_code = """// Geladeira encostada 100% no chão e na parede de fundo
            const fridgeMesh = getAsset('geladeira');
            fridgeMesh.position.set(-3.20, 0.0, -4.65);
            fridgeMesh.rotation.set(0, 0, 0);
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
            // 3.A) PRATELEIRAS DE MADEIRA NA PAREDE DO FUNDO
            // ==========================================
            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            
            // Prateleira Esquerda
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf1.position.set(-1.00, 1.82, -4.85);
            shelf1.castShadow = true;
            scene.add(shelf1);

            // Prateleira Direita
            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf2.position.set(1.00, 1.82, -4.85);
            shelf2.castShadow = true;
            scene.add(shelf2);

            // Saleiro e Pimenta-do-reino sobre a prateleira esquerda
            const saleiroMesh = getAsset('saleiro');
            placeOnSurface(saleiroMesh, -1.20, 1.835, -4.85, 0.08);
            scene.add(saleiroMesh);

            const pimentaMesh = getAsset('pimenta-do-reino');
            placeOnSurface(pimentaMesh, -0.80, 1.835, -4.85, 0.08);
            scene.add(pimentaMesh);

            // Pote de Geleia, Manteiga de Amendoim e Garrafa sobre a prateleira direita
            const geleiaMesh = getAsset('pote-de-geleia');
            placeOnSurface(geleiaMesh, 0.70, 1.835, -4.85, 0.09);
            scene.add(geleiaMesh);

            const manteigaMesh = getAsset('manteiga-de-amendoim');
            placeOnSurface(manteigaMesh, 0.95, 1.835, -4.85, 0.09);
            scene.add(manteigaMesh);

            const garrafaMesh = getAsset('garrafa');
            placeOnSurface(garrafaMesh, 1.20, 1.835, -4.85, 0.16);
            scene.add(garrafaMesh);

            // Assadeira na prateleira esquerda com pães reservas
            const assadeiraMesh = getAsset('assadeira');
            placeOnSurface(assadeiraMesh, -1.00, 1.835, -4.85, 0.32);
            scene.add(assadeiraMesh);"""

text, count = re.subn(shelves_pattern, new_shelves_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace shelves code'

# 3. Bancada de Preparo, Faca, Copos isolados
prep_pattern = r'// Faca deitada de lado sobre a bancada.*?scene\.add\(papelToalhaMesh\);'
new_prep_code = """// Faca de Cozinha (deitada no tampo com rotation.x = Math.PI / 2)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.12, LEVEL_1_Y, -0.60, 0.22);
            facaSimples.rotation.x = Math.PI / 2;
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

            // Copos vermelhos isolados no canto da bancada em position.set(1.50, COUNTER_Y, -0.60)
            const cup1 = createCupMesh(); cup1.position.set(1.50, LEVEL_1_Y, -0.60); scene.add(cup1);
            const cup2 = createCupMesh(); cup2.position.set(1.58, LEVEL_1_Y, -0.60); scene.add(cup2);
            const cup3 = createCupMesh(); cup3.position.set(1.54, LEVEL_1_Y, -0.52); scene.add(cup3);

            const toasterMesh = getAsset('torradeira');
            placeOnSurface(toasterMesh, 1.35, LEVEL_1_Y, -0.85, 0.22);
            scene.add(toasterMesh);

            const papelToalhaMesh = getAsset('papel-toalha');
            placeOnSurface(papelToalhaMesh, 1.50, LEVEL_1_Y, -0.85, 0.22);
            scene.add(papelToalhaMesh);"""

text, count = re.subn(prep_pattern, new_prep_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace prep and cups code'

# 4. Decoração 3.D: Atribuições diretas de position.set e rotation.y
decor_pattern = r'// 3\.D\) DECORA.*?scene\.add\(mesa4\);'

new_decor_code = """// ==========================================
            // 3.D) ATRIBUIÇÕES DIRETAS DE DECORAÇÃO, JANELAS, PORTA E PAREDE FRONTAL
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

            // 2. Janelas e Porta (Fixação nas Paredes Laterais)
            // Janela Esquerda (janela.glb):
            const janelaEsq = getAsset('janela');
            janelaEsq.position.set(-6.95, 1.70, 0.0);
            janelaEsq.rotation.y = Math.PI / 2;
            scene.add(janelaEsq);

            // Janela Direita (janela.glb):
            const janelaDir = getAsset('janela');
            janelaDir.position.set(6.95, 1.70, -1.5);
            janelaDir.rotation.y = -Math.PI / 2;
            scene.add(janelaDir);

            // Porta (porta.glb) - base encostada no chão Y = 0:
            const portaMesh = getAsset('porta');
            portaMesh.position.set(6.95, 0.0, 2.5);
            portaMesh.rotation.y = -Math.PI / 2;
            scene.add(portaMesh);

            // Placa "SAÍDA / EXIT" acima da porta:
            const placaSaida = createExitSignMesh();
            placaSaida.position.set(6.95, 2.25, 2.5);
            placaSaida.rotation.y = -Math.PI / 2;
            scene.add(placaSaida);

            // 3. Parede Frontal dos Clientes (Fixação em Z = 4.95, virados para Y = Math.PI)
            // Lousa / Quadro Negro (quadro-negro.glb):
            const quadroMesh = getAsset('quadro-negro');
            quadroMesh.position.set(0.0, 1.40, 4.95);
            quadroMesh.rotation.y = Math.PI;
            quadroMesh.scale.setScalar(1.6);
            scene.add(quadroMesh);

            // Apenas 2 Armários (armario-cozinha.glb):
            const armario1 = getAsset('armario-cozinha');
            armario1.position.set(-1.20, 2.30, 4.95);
            armario1.rotation.y = Math.PI;
            scene.add(armario1);

            const armario2 = getAsset('armario-cozinha');
            armario2.position.set(1.20, 2.30, 4.95);
            armario2.rotation.y = Math.PI;
            scene.add(armario2);

            // Relógio (relogio.glb):
            const relogioMesh = getAsset('relogio');
            relogioMesh.position.set(0.0, 2.85, 4.95);
            relogioMesh.rotation.y = Math.PI;
            scene.add(relogioMesh);

            // 4. Mesas de Clientes no Salão
            const mesa1 = getAsset('mesa-com-comida');
            placeOnSurface(mesa1, -3.20, 0.0, 2.50, 1.10);
            scene.add(mesa1);

            const mesa2 = getAsset('mesa-com-comida');
            placeOnSurface(mesa2, 3.20, 0.0, 2.50, 1.10);
            scene.add(mesa2);

            const mesa3 = getAsset('mesa-com-comida');
            placeOnSurface(mesa3, -3.20, 0.0, 4.20, 1.10);
            scene.add(mesa3);

            const mesa4 = getAsset('mesa-com-comida');
            placeOnSurface(mesa4, 3.20, 0.0, 4.20, 1.10);
            scene.add(mesa4);"""

text, count = re.subn(decor_pattern, new_decor_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace decor code'

# 5. Painel de TV na parede de fundo
recipe_board_pattern = r'const targetBackWallZ = \(window\.backWall \? window\.backWall\.position\.z : -2\.20\);\s*recipeBoardMesh\.position\.set\(0\.00, 2\.10, targetBackWallZ \+ 0\.02\);'
new_recipe_board_set = """recipeBoardMesh.position.set(0.00, 2.10, -4.95);"""
text = re.sub(recipe_board_pattern, new_recipe_board_set, text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success! Complete rewrite applied with direct position.set and rotation assignments.')
