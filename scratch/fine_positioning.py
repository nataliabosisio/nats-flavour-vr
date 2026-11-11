import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the decor and walls section 3.D
decor_pattern = r'// 3\.D\) DECORA.*?scene\.add\(mesa4\);'

new_decor_code = """// 3.D) DECORAÇÃO E FIXAÇÃO RELATIVA ÀS PAREDES REAIS
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

            // 2. Janelas 100% planas e coladas nas paredes laterais em altura padrão (Y = 1.70)
            // Janela Esquerda: Encostada na parede esquerda em X = leftWall.position.x + 0.02, Y = 1.70, Z = 0.0, rotation.y = Math.PI / 2
            const janela1 = getAsset('janela');
            placeOnSurface(janela1, leftWall.position.x + 0.02, 1.70, 0.0, 1.3);
            janela1.rotation.y = Math.PI / 2;
            scene.add(janela1);

            // Janela Direita: Encostada na parede direita em X = rightWall.position.x - 0.02, Y = 1.70, Z = 0.0, rotation.y = -Math.PI / 2
            const janela2 = getAsset('janela');
            placeOnSurface(janela2, rightWall.position.x - 0.02, 1.70, 0.0, 1.3);
            janela2.rotation.y = -Math.PI / 2;
            scene.add(janela2);

            // 3. Porta assentada exatamente no chão (Y = 0.0) e colada à parede lateral (X = rightWall.position.x - 0.02, Z = 2.5)
            const portaMesh = getAsset('porta');
            placeOnSurface(portaMesh, rightWall.position.x - 0.02, 0.0, 2.5, 2.2);
            portaMesh.rotation.y = -Math.PI / 2;
            scene.add(portaMesh);

            const portaBox = new THREE.Box3().setFromObject(portaMesh);
            const portaHeight = isFinite(portaBox.max.y) ? portaBox.max.y : 2.20;

            // Placa "SAÍDA / EXIT" centralizada sobre o batente superior da porta (Y = portaHeight + 0.10)
            const exitSign = createExitSignMesh();
            placeOnSurface(exitSign, rightWall.position.x - 0.02, portaHeight + 0.10, 2.5);
            exitSign.rotation.y = -Math.PI / 2;
            scene.add(exitSign);

            // 4. Reorganização da Parede Frontal (Alturas Proporcionais e 2 Armários)
            // Lousa / Quadro Negro na altura normal dos olhos (Y = 1.55), centralizada em X = 0.0
            const quadroMesh = getAsset('quadro-negro');
            placeOnSurface(quadroMesh, 0.0, 1.55, frontWall.position.z - 0.05, 1.60);
            quadroMesh.rotation.y = Math.PI;
            scene.add(quadroMesh);

            // Armários Suspensos: 2 armários simétricos posicionados em Y = 2.20 logo acima da lousa
            const armario1 = getAsset('armario-cozinha');
            placeOnSurface(armario1, -0.60, 2.20, frontWall.position.z - 0.15, 0.85);
            armario1.rotation.y = Math.PI;
            scene.add(armario1);

            const armario2 = getAsset('armario-cozinha');
            placeOnSurface(armario2, 0.60, 2.20, frontWall.position.z - 0.15, 0.85);
            armario2.rotation.y = Math.PI;
            scene.add(armario2);

            // Relógio de Parede baixado para Y = 2.65, centralizado acima dos armários
            const relogioMesh = getAsset('relogio');
            placeOnSurface(relogioMesh, 0.0, 2.65, frontWall.position.z - 0.05, 0.40);
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

text, count = re.subn(decor_pattern, new_decor_code, text, count=1, flags=re.DOTALL)
assert count == 1, 'Failed to replace decor code'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success! Fine positioning adjustment applied.')
