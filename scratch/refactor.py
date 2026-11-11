import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Helper functions createExitSignMesh, createPottedPlantMesh, createCupMesh
helpers_marker = """function createUtensilJarMesh() {
            const group = new THREE.Group();
            const jarMat = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.3, flatShading: true });
            const jarGeo = new THREE.CylinderGeometry(0.045, 0.04, 0.11, 12);
            const jar = new THREE.Mesh(jarGeo, jarMat);
            jar.position.y = 0.055;
            jar.castShadow = true;
            jar.receiveShadow = true;
            group.add(jar);
            return group;
        }"""

new_helpers = """function createUtensilJarMesh() {
            const group = new THREE.Group();
            const jarMat = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.3, flatShading: true });
            const jarGeo = new THREE.CylinderGeometry(0.045, 0.04, 0.11, 12);
            const jar = new THREE.Mesh(jarGeo, jarMat);
            jar.position.y = 0.055;
            jar.castShadow = true;
            jar.receiveShadow = true;
            group.add(jar);
            return group;
        }

        function createExitSignMesh() {
            const group = new THREE.Group();
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 96;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#0F5132';
            ctx.fillRect(0, 0, 256, 96);
            ctx.strokeStyle = '#D1E7DD';
            ctx.lineWidth = 4;
            ctx.strokeRect(4, 4, 248, 88);
            ctx.fillStyle = '#FFFFFF';
            ctx.font = 'bold 36px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('SAÍDA / EXIT', 128, 48);

            const texture = new THREE.CanvasTexture(canvas);
            const signMat = new THREE.MeshStandardMaterial({ map: texture, roughness: 0.3 });
            const boxGeo = new THREE.BoxGeometry(0.48, 0.18, 0.04);
            const signMesh = new THREE.Mesh(boxGeo, signMat);
            signMesh.castShadow = true;
            group.add(signMesh);
            return group;
        }

        function createPottedPlantMesh() {
            const group = new THREE.Group();
            const potMat = new THREE.MeshStandardMaterial({ color: 0xD97736, roughness: 0.6 });
            const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.12, 0.32, 16), potMat);
            pot.position.y = 0.16;
            pot.castShadow = true;
            pot.receiveShadow = true;
            group.add(pot);

            const soilMat = new THREE.MeshStandardMaterial({ color: 0x3E2723, roughness: 0.9 });
            const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.155, 0.155, 0.02, 16), soilMat);
            soil.position.y = 0.31;
            group.add(soil);

            const leafMat = new THREE.MeshStandardMaterial({ color: 0x2E7D32, roughness: 0.5, flatShading: true });
            const foliage = new THREE.Mesh(new THREE.DodecahedronGeometry(0.22, 1), leafMat);
            foliage.position.y = 0.46;
            foliage.castShadow = true;
            group.add(foliage);
            return group;
        }

        function createCupMesh() {
            const group = new THREE.Group();
            const cupMat = new THREE.MeshStandardMaterial({ color: 0xE63946, roughness: 0.3 });
            const cupGeo = new THREE.CylinderGeometry(0.04, 0.03, 0.10, 16);
            const cup = new THREE.Mesh(cupGeo, cupMat);
            cup.position.y = 0.05;
            cup.castShadow = true;
            cup.receiveShadow = true;
            group.add(cup);

            const rimMat = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.4 });
            const rim = new THREE.Mesh(new THREE.TorusGeometry(0.04, 0.004, 8, 16), rimMat);
            rim.rotation.x = Math.PI / 2;
            rim.position.y = 0.10;
            group.add(rim);
            return group;
        }"""

assert helpers_marker in text, 'helpers_marker not found'
text = text.replace(helpers_marker, new_helpers)

# 2. Room Dimensions & Walls
room_pattern = r'// DIMENS.*?scene\.add\(tilesFront\);'
new_room_code = """// DIMENSÕES EXPANDIDAS E ANCORADAS DA LANCHONETE
            // ==========================================
            const ROOM_WIDTH = 6.40;
            const ROOM_HEIGHT = 3.80;
            const WALL_BACK_Z = -1.90;
            const WALL_FRONT_Z = 3.20;
            const ROOM_DEPTH = WALL_FRONT_Z - WALL_BACK_Z; // 5.10
            const CENTER_Z = (WALL_BACK_Z + WALL_FRONT_Z) / 2; // 0.65
            const HALF_W = ROOM_WIDTH / 2; // 3.20
            const WALL_LEFT_X = -HALF_W; // -3.20
            const WALL_RIGHT_X = HALF_W; // 3.20

            // Piso Visível (Cobrindo toda a sala de Z = -1.90 a Z = 3.20)
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

            // Parede de Fundo (Fechada em Z = -1.90)
            const backWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), wallMat);
            backWall.position.set(0, ROOM_HEIGHT / 2, WALL_BACK_Z);
            scene.add(backWall);

            // Parede Lateral Esquerda (Fechada em X = -3.20)
            const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), wallMat);
            leftWall.position.set(WALL_LEFT_X, ROOM_HEIGHT / 2, CENTER_Z);
            leftWall.rotation.y = Math.PI / 2;
            scene.add(leftWall);

            // Parede Lateral Direita (Fechada em X = 3.20)
            const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), wallMat);
            rightWall.position.set(WALL_RIGHT_X, ROOM_HEIGHT / 2, CENTER_Z);
            rightWall.rotation.y = -Math.PI / 2;
            scene.add(rightWall);

            // Parede Frontal dos Clientes (Fechada em Z = 3.20)
            const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), wallMat);
            frontWall.position.set(0, ROOM_HEIGHT / 2, WALL_FRONT_Z);
            frontWall.rotation.y = Math.PI;
            scene.add(frontWall);

            // Teto (Fechamento Superior da Lanchonete em Y = 3.80)
            const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_DEPTH), wallMat);
            ceiling.position.set(0, ROOM_HEIGHT, CENTER_Z);
            ceiling.rotation.x = Math.PI / 2;
            scene.add(ceiling);

            // Revestimento Unificado de Azulejos Brancos (Do chão ao teto em todas as 4 paredes)
            // Azulejos na Parede de Fundo (Z = -1.89)
            const tilesBack = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            tilesBack.position.set(0, ROOM_HEIGHT / 2, WALL_BACK_Z + 0.01);
            tilesBack.receiveShadow = true;
            scene.add(tilesBack);

            // Azulejos na Parede Esquerda (X = -3.19)
            const tilesLeft = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            tilesLeft.position.set(WALL_LEFT_X + 0.01, ROOM_HEIGHT / 2, CENTER_Z);
            tilesLeft.rotation.y = Math.PI / 2;
            tilesLeft.receiveShadow = true;
            scene.add(tilesLeft);

            // Azulejos na Parede Direita (X = 3.19)
            const tilesRight = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_DEPTH, ROOM_HEIGHT), tileMat);
            tilesRight.position.set(WALL_RIGHT_X - 0.01, ROOM_HEIGHT / 2, CENTER_Z);
            tilesRight.rotation.y = -Math.PI / 2;
            tilesRight.receiveShadow = true;
            scene.add(tilesRight);

            // Azulejos na Parede Frontal (Z = 3.19, de frente para o salão)
            const tilesFront = new THREE.Mesh(new THREE.PlaneGeometry(ROOM_WIDTH, ROOM_HEIGHT), tileMat);
            tilesFront.position.set(0, ROOM_HEIGHT / 2, WALL_FRONT_Z - 0.01);
            tilesFront.rotation.y = Math.PI;
            tilesFront.receiveShadow = true;
            scene.add(tilesFront);"""

text, count = re.subn(room_pattern, new_room_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace room code'

# 3. Shelves and fridge flush against back wall (Z = -1.88)
shelves_pattern = r'// Geladeira \(Encostada na parede esquerda X = -2\.40\).*?scene\.add\(assadeiraMesh\);'
new_shelves_code = """// Geladeira (Encostada na parede esquerda e de fundo em Z = -1.88)
            const fridgeMesh = getAsset('geladeira');
            placeOnSurface(fridgeMesh, -2.40, 0.0, -1.55, 1.85);
            fridgeMesh.rotation.y = 0.15;
            scene.add(fridgeMesh);

            // Coifa de Inox (Alinhada com fogão em X = -0.80)
            const hoodGroup = new THREE.Group();
            const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.16, 0.55), stainlessMat);
            hoodCanopy.position.set(-0.80, 1.95, -0.55);
            hoodCanopy.castShadow = true;
            hoodGroup.add(hoodCanopy);

            const hoodDuct = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.8, 16), stainlessMat);
            hoodDuct.position.set(-0.80, 2.40, -0.55);
            hoodGroup.add(hoodDuct);
            scene.add(hoodGroup);

            // ==========================================
            // 3.A) PRATELEIRAS SUSPENSAS FIXADAS NA PAREDE DO FUNDO (Z = -1.88)
            // ==========================================
            const shelfMat = new THREE.MeshStandardMaterial({ map: createWoodTexture(), roughness: 0.4 });
            
            // Prateleira Esquerda (Profundidade 0.22, centro em Z = -1.77 para a face traseira encostar em Z = -1.88)
            const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf1.position.set(-0.75, 1.82, -1.77);
            shelf1.castShadow = true;
            scene.add(shelf1);

            // Prateleira Direita
            const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(1.00, 0.03, 0.22), shelfMat);
            shelf2.position.set(0.75, 1.82, -1.77);
            shelf2.castShadow = true;
            scene.add(shelf2);

            // Prateleira Esquerda: Saleiro e Pimenta-do-reino lado a lado
            const saleiroMesh = getAsset('saleiro');
            placeOnSurface(saleiroMesh, -0.90, 1.835, -1.77, 0.08);
            scene.add(saleiroMesh);

            const pimentaMesh = getAsset('pimenta-do-reino');
            placeOnSurface(pimentaMesh, -0.60, 1.835, -1.77, 0.08);
            scene.add(pimentaMesh);

            // Prateleira Direita: Pote de Geleia, Manteiga de Amendoim e Garrafa alinhados
            const geleiaMesh = getAsset('pote-de-geleia');
            placeOnSurface(geleiaMesh, 0.55, 1.835, -1.77, 0.09);
            scene.add(geleiaMesh);

            const manteigaMesh = getAsset('manteiga-de-amendoim');
            placeOnSurface(manteigaMesh, 0.75, 1.835, -1.77, 0.09);
            scene.add(manteigaMesh);

            const garrafaMesh = getAsset('garrafa');
            placeOnSurface(garrafaMesh, 0.95, 1.835, -1.77, 0.16);
            scene.add(garrafaMesh);

            // Assadeira na prateleira esquerda contendo pães reservas (estoque visual)
            const assadeiraMesh = getAsset('assadeira');
            placeOnSurface(assadeiraMesh, -0.75, 1.835, -1.77, 0.32);
            scene.add(assadeiraMesh);"""

text, count = re.subn(shelves_pattern, new_shelves_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace shelves code'

# 4. Assembly Station: Clean plate, remove snapRing, add cups row on the left
assembly_pattern = r'// 3\.B\) ESTA.*?DE MONTAGEM \(CENTRO: X = 0\.00\).*?window\.plateSurfaceTopY = plateBox\.max\.y;'
new_assembly_code = """// 3.B) ESTAÇÃO DE MONTAGEM (CENTRO: X = 0.00)
            // ==========================================
            const yellowMatMesh = new THREE.Mesh(
                new THREE.BoxGeometry(0.52, 0.006, 0.42),
                new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.3, flatShading: true })
            );
            placeOnSurface(yellowMatMesh, 0.00, LEVEL_1_Y, -0.65);
            yellowMatMesh.receiveShadow = true;
            scene.add(yellowMatMesh);

            // Prato Quadrado Central (Totalmente limpo e vazio, sem copos ou cilindros em cima)
            const plateMesh = getAsset('prato-quadrado');
            plateMesh.rotation.set(0, 0, 0);
            placeOnSurface(plateMesh, 0.00, LEVEL_1_Y + 0.008, -0.65, 0.28);
            scene.add(plateMesh);

            const plateBox = new THREE.Box3().setFromObject(plateMesh);
            window.plateSurfaceTopY = plateBox.max.y;

            // Fileira de Copos Organizados à Esquerda da Estação de Montagem (sobre pequena bandeja)
            const cupTray = new THREE.Mesh(
                new THREE.BoxGeometry(0.18, 0.008, 0.30),
                stainlessMat
            );
            placeOnSurface(cupTray, -0.36, LEVEL_1_Y, -0.65);
            cupTray.receiveShadow = true;
            scene.add(cupTray);

            const cup1 = createCupMesh(); placeOnSurface(cup1, -0.36, LEVEL_1_Y + 0.008, -0.73); scene.add(cup1);
            const cup2 = createCupMesh(); placeOnSurface(cup2, -0.36, LEVEL_1_Y + 0.008, -0.65); scene.add(cup2);
            const cup3 = createCupMesh(); placeOnSurface(cup3, -0.36, LEVEL_1_Y + 0.008, -0.57); scene.add(cup3);"""

text, count = re.subn(assembly_pattern, new_assembly_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace assembly station code'

# 5. Cutting board, knife, tomatoes, condiments, doors, windows, decor
decor_pattern = r'// Faca de Cozinha.*?scene\.add\(armario3\);'
new_decor_code = """// Faca de Cozinha (deitada horizontalmente sobre a bancada ao lado da tábua de corte)
            const facaSimples = getAsset('faca');
            placeOnSurface(facaSimples, 1.16, LEVEL_1_Y, -0.60, 0.22);
            facaSimples.rotation.x = Math.PI / 2;
            facaSimples.rotation.z = Math.PI / 6;
            scene.add(facaSimples);

            // Tomates e Molhos alinhados na parte de trás da bancada (Z = -0.88) de forma simétrica
            const ketchupBottle = createSqueezeBottleMesh(0xD32F2F); placeOnSurface(ketchupBottle, 0.45, LEVEL_1_Y, -0.88); scene.add(ketchupBottle);
            const mustardBottle = createSqueezeBottleMesh(0xFFD700); placeOnSurface(mustardBottle, 0.58, LEVEL_1_Y, -0.88); scene.add(mustardBottle);

            const tomatoMesh = getAsset('tomate');
            placeOnSurface(tomatoMesh, 0.72, LEVEL_1_Y, -0.88, 0.09);
            scene.add(tomatoMesh);

            const tomatoSlicedMesh = getAsset('tomate-cortado');
            placeOnSurface(tomatoSlicedMesh, 0.84, LEVEL_1_Y, -0.88, 0.09);
            scene.add(tomatoSlicedMesh);

            const espatulaMesh = getAsset('espatula');
            placeOnSurface(espatulaMesh, 0.98, LEVEL_1_Y, -0.88, 0.24);
            espatulaMesh.rotation.y = Math.PI / 4;
            scene.add(espatulaMesh);

            const knifeBlock = createKnifeBlockMesh(); placeOnSurface(knifeBlock, 1.15, LEVEL_1_Y, -0.88); scene.add(knifeBlock);

            const toasterMesh = getAsset('torradeira');
            placeOnSurface(toasterMesh, 1.34, LEVEL_1_Y, -0.88, 0.22);
            scene.add(toasterMesh);

            // Papel toalha no canto traseiro da bancada
            const papelToalhaMesh = getAsset('papel-toalha');
            placeOnSurface(papelToalhaMesh, 1.54, LEVEL_1_Y, -0.88, 0.22);
            scene.add(papelToalhaMesh);

            // ==========================================
            // 3.C) CHÃO E PISO (Lixeira encostada à lateral)
            // ==========================================
            const lixeiraMesh = getAsset('lixeira');
            placeOnSurface(lixeiraMesh, 2.50, 0.0, -0.50, 0.45);
            scene.add(lixeiraMesh);

            // ==========================================
            // 3.D) ELEMENTOS DECORATIVOS ADICIONAIS & PORTA / JANELAS / SALÃO
            // ==========================================
            // 1. Lâmpadas Pendentes (Penduradas a Y = 1.75 diretamente sobre a bancada de trabalho)
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

            // 2. Janelas nas Paredes Laterais (Sem sobreposições com armários)
            // Janela Esquerda (X = -3.18, Y = 1.80, Z = 0.50, rotation.y = Math.PI / 2)
            const janelaEsq = getAsset('janela');
            placeOnSurface(janelaEsq, -3.18, 1.80, 0.50, 1.2);
            janelaEsq.rotation.y = Math.PI / 2;
            scene.add(janelaEsq);

            // Janela Direita (X = 3.18, Y = 1.80, Z = 0.50, rotation.y = -Math.PI / 2)
            const janelaDir = getAsset('janela');
            placeOnSurface(janelaDir, 3.18, 1.80, 0.50, 1.2);
            janelaDir.rotation.y = -Math.PI / 2;
            scene.add(janelaDir);

            // 3. Porta de Entrada (Fixada na parede lateral direita em X = 3.18, Y = 0.0, Z = 2.0)
            const portaMesh = getAsset('porta');
            placeOnSurface(portaMesh, 3.18, 0.0, 2.0, 2.2);
            portaMesh.rotation.y = -Math.PI / 2;
            scene.add(portaMesh);

            // Placa "SAÍDA / EXIT" acima da porta
            const exitSign = createExitSignMesh();
            placeOnSurface(exitSign, 3.18, 2.28, 2.0);
            exitSign.rotation.y = -Math.PI / 2;
            scene.add(exitSign);

            // Vaso com planta/arbusto ao lado da porta no chão
            const plantaMesh = createPottedPlantMesh();
            placeOnSurface(plantaMesh, 2.90, 0.0, 2.90);
            scene.add(plantaMesh);

            // 4. Lousa / Quadro Negro (Na altura dos olhos na Parede Frontal Z = 3.18)
            const quadroMesh = getAsset('quadro-negro');
            placeOnSurface(quadroMesh, 0.0, 1.75, 3.18, 1.80);
            quadroMesh.rotation.y = Math.PI;
            scene.add(quadroMesh);

            // 5. Relógio de Parede (Fixado acima do quadro negro em Z = 3.18)
            const relogioMesh = getAsset('relogio');
            placeOnSurface(relogioMesh, 0.0, 2.85, 3.18, 0.40);
            relogioMesh.rotation.y = Math.PI;
            scene.add(relogioMesh);

            // 6. Fileira de 3 Armários de Cozinha no alto da parede frontal (Y = 2.70, Z = 3.18)
            const armario1 = getAsset('armario-cozinha');
            placeOnSurface(armario1, -1.80, 2.70, 3.18, 0.85);
            armario1.rotation.y = Math.PI;
            scene.add(armario1);

            const armario2 = getAsset('armario-cozinha');
            placeOnSurface(armario2, 1.30, 2.70, 3.18, 0.85);
            armario2.rotation.y = Math.PI;
            scene.add(armario2);

            const armario3 = getAsset('armario-cozinha');
            placeOnSurface(armario3, 2.15, 2.70, 3.18, 0.85);
            armario3.rotation.y = Math.PI;
            scene.add(armario3);

            // 7. Mesas de Clientes no Salão
            const mesa1 = getAsset('mesa-com-comida');
            placeOnSurface(mesa1, -1.80, 0.0, 1.60, 1.05);
            scene.add(mesa1);

            const mesa2 = getAsset('mesa-com-comida');
            placeOnSurface(mesa2, -1.80, 0.0, 2.50, 1.05);
            scene.add(mesa2);

            const mesa3 = getAsset('mesa-com-comida');
            placeOnSurface(mesa3, 1.60, 0.0, 1.50, 1.05);
            scene.add(mesa3);"""

text, count = re.subn(decor_pattern, new_decor_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace decor code'

# 6. Recipe TV Board fixado na parede de fundo em Z = -1.88
recipe_board_pattern = r'recipeBoardMesh\.position\.set\(0\.00, 1\.75, -1\.87\);'
assert re.search(recipe_board_pattern, text), 'recipeBoardMesh pattern not found'
text = re.sub(recipe_board_pattern, 'recipeBoardMesh.position.set(0.00, 1.75, -1.88);', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully applied all refactoring modifications!')
