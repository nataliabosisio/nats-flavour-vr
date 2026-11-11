
        import * as THREE from 'three';
        import { VRButton } from 'three/addons/webxr/VRButton.js';
        import { XRControllerModelFactory } from 'three/addons/webxr/XRControllerModelFactory.js';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

        // ==========================================
        // 1. SISTEMA DE ÁUDIO PROCEDURAL (Web Audio API)
        // ==========================================
        class AudioManager {
            constructor() {
                this.ctx = null;
                this.masterGain = null;
                this.sizzleSource = null;
                this.sizzleGain = null;
                this.isMuted = false;
                this.isSizzling = false;
            }

            init() {
                if (this.ctx) return;
                const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                this.ctx = new AudioContextClass();
                this.masterGain = this.ctx.createGain();
                this.masterGain.connect(this.ctx.destination);
            }

            toggleMute() {
                this.init();
                this.isMuted = !this.isMuted;
                if (this.masterGain && this.ctx) {
                    this.masterGain.gain.setValueAtTime(this.isMuted ? 0 : 1, this.ctx.currentTime);
                }
                return this.isMuted;
            }

            playPop() {
                this.init();
                if (this.ctx.state === 'suspended') this.ctx.resume();

                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = 'sine';
                const now = this.ctx.currentTime;
                osc.frequency.setValueAtTime(180, now);
                osc.frequency.exponentialRampToValueAtTime(520, now + 0.08);

                gain.gain.setValueAtTime(0.35, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

                osc.connect(gain);
                gain.connect(this.masterGain);

                osc.start(now);
                osc.stop(now + 0.09);
            }

            startSizzle() {
                this.init();
                if (this.ctx.state === 'suspended') this.ctx.resume();
                if (this.isSizzling) return;

                const bufferSize = this.ctx.sampleRate * 2;
                const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
                const output = noiseBuffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    output[i] = Math.random() * 2 - 1;
                }

                this.sizzleSource = this.ctx.createBufferSource();
                this.sizzleSource.buffer = noiseBuffer;
                this.sizzleSource.loop = true;

                const bandpass = this.ctx.createBiquadFilter();
                bandpass.type = 'bandpass';
                bandpass.frequency.value = 1500;
                bandpass.Q.value = 1.2;

                const highpass = this.ctx.createBiquadFilter();
                highpass.type = 'highpass';
                highpass.frequency.value = 700;

                this.sizzleGain = this.ctx.createGain();
                this.sizzleGain.gain.setValueAtTime(0.18, this.ctx.currentTime);

                this.sizzleSource.connect(bandpass);
                bandpass.connect(highpass);
                highpass.connect(this.sizzleGain);
                this.sizzleGain.connect(this.masterGain);

                this.sizzleSource.start();
                this.isSizzling = true;
            }

            stopSizzle() {
                if (this.sizzleSource && this.isSizzling) {
                    try {
                        this.sizzleGain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.1);
                        setTimeout(() => {
                            if (this.sizzleSource) {
                                this.sizzleSource.stop();
                                this.sizzleSource.disconnect();
                                this.sizzleSource = null;
                            }
                        }, 120);
                    } catch(e) {}
                    this.isSizzling = false;
                }
            }

            playVictoryFanfare() {
                this.init();
                if (this.ctx.state === 'suspended') this.ctx.resume();

                const notes = [523.25, 659.25, 783.99, 1046.50];
                const times = [0, 0.12, 0.24, 0.36];
                const durations = [0.15, 0.15, 0.15, 0.6];

                notes.forEach((freq, idx) => {
                    const startTime = this.ctx.currentTime + times[idx];
                    const osc = this.ctx.createOscillator();
                    const gain = this.ctx.createGain();

                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, startTime);

                    gain.gain.setValueAtTime(0.3, startTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, startTime + durations[idx]);

                    osc.connect(gain);
                    gain.connect(this.masterGain);

                    osc.start(startTime);
                    osc.stop(startTime + durations[idx] + 0.05);
                });
            }
        }

        const audioManager = new AudioManager();

        // ==========================================
        // 2. SISTEMA DE EFEITOS VISUAIS E PARTICULAS (VFX)
        // ==========================================
        class VFXManager {
            constructor(scene) {
                this.scene = scene;
                this.smokeParticles = [];
                this.confettiParticles = [];
                this.lerpQueue = [];
                this.isSmoking = false;
                this.isConfettiActive = false;
                this.smokeEmitterPos = new THREE.Vector3(-1.15, 0.9300, -0.55);

                this.initSmokePool();
            }

            initSmokePool() {
                const geo = new THREE.DodecahedronGeometry(0.025, 0);
                const mat = new THREE.MeshStandardMaterial({
                    color: 0xE2E8F0,
                    transparent: true,
                    opacity: 0,
                    flatShading: true
                });

                for (let i = 0; i < 22; i++) {
                    const mesh = new THREE.Mesh(geo, mat.clone());
                    mesh.visible = false;
                    this.scene.add(mesh);
                    this.smokeParticles.push({
                        mesh: mesh,
                        vy: 0.0035 + Math.random() * 0.003,
                        vx: (Math.random() - 0.5) * 0.001,
                        vz: (Math.random() - 0.5) * 0.001,
                        growth: 0.001 + Math.random() * 0.0005,
                        life: 0
                    });
                }
            }

            startSmoke() {
                this.isSmoking = true;
                this.smokeParticles.forEach((p, idx) => {
                    p.mesh.visible = true;
                    p.mesh.position.copy(this.smokeEmitterPos).add(new THREE.Vector3(
                        (Math.random() - 0.5) * 0.08,
                        idx * 0.015,
                        (Math.random() - 0.5) * 0.08
                    ));
                    p.mesh.scale.set(1, 1, 1);
                    p.mesh.material.opacity = 0.5;
                    p.life = Math.random();
                });
            }

            stopSmoke() {
                this.isSmoking = false;
                this.smokeParticles.forEach(p => {
                    p.mesh.material.opacity = 0;
                    p.mesh.visible = false;
                });
            }

            spawnConfetti() {
                this.clearConfetti();
                this.isConfettiActive = true;

                const colors = [0xFFD700, 0xEF476F, 0x06D6A0, 0x118AB2, 0x20B2AA, 0xF26419];
                const geo = new THREE.BoxGeometry(0.025, 0.005, 0.035);

                for (let i = 0; i < 140; i++) {
                    const mat = new THREE.MeshStandardMaterial({
                        color: colors[Math.floor(Math.random() * colors.length)],
                        flatShading: true
                    });
                    const mesh = new THREE.Mesh(geo, mat);
                    mesh.castShadow = true;

                    mesh.position.set(
                        (Math.random() - 0.5) * 2.2,
                        2.2 + Math.random() * 0.8,
                        -0.4 + (Math.random() - 0.5) * 1.2
                    );

                    mesh.rotation.set(
                        Math.random() * Math.PI,
                        Math.random() * Math.PI,
                        Math.random() * Math.PI
                    );

                    this.scene.add(mesh);

                    this.confettiParticles.push({
                        mesh: mesh,
                        vy: -0.008 - Math.random() * 0.008,
                        vx: (Math.random() - 0.5) * 0.004,
                        vz: (Math.random() - 0.5) * 0.004,
                        rotX: (Math.random() - 0.5) * 0.1,
                        rotY: (Math.random() - 0.5) * 0.1
                    });
                }

                setTimeout(() => this.clearConfetti(), 5500);
            }

            clearConfetti() {
                this.isConfettiActive = false;
                this.confettiParticles.forEach(p => {
                    this.scene.remove(p.mesh);
                    p.mesh.geometry.dispose();
                    p.mesh.material.dispose();
                });
                this.confettiParticles = [];
            }

            addLerp(object, targetPos, targetRot = null, speed = 0.22, onComplete = null) {
                this.lerpQueue.push({
                    object,
                    targetPos: targetPos.clone(),
                    targetRot: targetRot ? targetRot.clone() : object.quaternion.clone(),
                    speed,
                    onComplete
                });
            }

            update() {
                if (this.isSmoking) {
                    this.smokeParticles.forEach(p => {
                        p.mesh.position.y += p.vy;
                        p.mesh.position.x += p.vx;
                        p.mesh.position.z += p.vz;
                        p.mesh.scale.addScalar(p.growth);
                        p.mesh.material.opacity -= 0.006;

                        if (p.mesh.material.opacity <= 0 || p.mesh.position.y > 1.4) {
                            p.mesh.position.copy(this.smokeEmitterPos).add(new THREE.Vector3(
                                (Math.random() - 0.5) * 0.08,
                                0,
                                (Math.random() - 0.5) * 0.08
                            ));
                            p.mesh.scale.set(1, 1, 1);
                            p.mesh.material.opacity = 0.45;
                        }
                    });
                }

                if (this.isConfettiActive) {
                    this.confettiParticles.forEach(p => {
                        p.mesh.position.y += p.vy;
                        p.mesh.position.x += p.vx;
                        p.mesh.position.z += p.vz;
                        p.mesh.rotation.x += p.rotX;
                        p.mesh.rotation.y += p.rotY;
                    });
                }

                for (let i = this.lerpQueue.length - 1; i >= 0; i--) {
                    const item = this.lerpQueue[i];
                    item.object.position.lerp(item.targetPos, item.speed);
                    item.object.quaternion.slerp(item.targetRot, item.speed);

                    if (item.object.position.distanceTo(item.targetPos) < 0.002) {
                        item.object.position.copy(item.targetPos);
                        item.object.quaternion.copy(item.targetRot);
                        if (item.onComplete) item.onComplete();
                        this.lerpQueue.splice(i, 1);
                    }
                }
            }
        }

        // ==========================================
        // 3. CENA, CÂMERA E RENDERER
        // ==========================================
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1B2A4A);

        const cameraGroup = new THREE.Group();
        scene.add(cameraGroup);

        const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 30);
        camera.position.set(0, 1.52, 0.75);
        cameraGroup.add(camera);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.15;
        renderer.xr.enabled = true;
        document.body.appendChild(renderer.domElement);

        document.body.appendChild(VRButton.createButton(renderer));

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.target.set(0, 0.98, -0.65);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 0.3;
        controls.maxDistance = 2.0;
        controls.minPolarAngle = 0.2;
        controls.maxPolarAngle = Math.PI / 2 - 0.02;
        controls.update();
            updateVRTeleportPointer();

        const vfxManager = new VFXManager(scene);

        // ==========================================
        // 4. ILUMINAÇÃO DE ESTÚDIO E SOMBRAS SUAVES
        // ==========================================
        // HemisphereLight: Tom quente no topo (#FFF4E0), tom frio suave na base (#3A4B6E)
        const hemiLight = new THREE.HemisphereLight(0xFFF4E0, 0x3A4B6E, 1.1);
        scene.add(hemiLight);

        // DirectionalLight principal de estúdio com sombras suaves
        const mainSun = new THREE.DirectionalLight(0xFFFAED, 1.2);
        mainSun.position.set(2.5, 6.0, 3.0);
        mainSun.target.position.set(0.0, 0.9, -0.65);
        mainSun.castShadow = true;
        mainSun.shadow.mapSize.width = 2048;
        mainSun.shadow.mapSize.height = 2048;
        mainSun.shadow.camera.near = 0.5;
        mainSun.shadow.camera.far = 10;
        mainSun.shadow.bias = -0.0001;
        scene.add(mainSun);
        scene.add(mainSun.target);

        // SpotLight 1: Foco suave direcionado à Estação de Cocção (Fogão/Frigideira)
        const spotCooking = new THREE.SpotLight(0xFFE8D6, 2.5);
        spotCooking.position.set(-1.15, 3.0, -0.2);
        spotCooking.target.position.set(-1.15, 0.91, -0.55);
        spotCooking.angle = Math.PI / 5;
        spotCooking.penumbra = 0.6;
        spotCooking.decay = 1.5;
        spotCooking.distance = 6;
        spotCooking.castShadow = true;
        spotCooking.shadow.mapSize.width = 1024;
        spotCooking.shadow.mapSize.height = 1024;
        scene.add(spotCooking);
        scene.add(spotCooking.target);

        // SpotLight 2: Foco suave direcionado à Estação de Montagem (Prato Central)
        const spotAssembly = new THREE.SpotLight(0xFFF8E7, 2.8);
        spotAssembly.position.set(0.0, 3.0, -0.2);
        spotAssembly.target.position.set(0.0, 0.91, -0.65);
        spotAssembly.angle = Math.PI / 5;
        spotAssembly.penumbra = 0.6;
        spotAssembly.decay = 1.5;
        spotAssembly.distance = 6;
        spotAssembly.castShadow = true;
        spotAssembly.shadow.mapSize.width = 1024;
        spotAssembly.shadow.mapSize.height = 1024;
        scene.add(spotAssembly);
        scene.add(spotAssembly.target);

        // ==========================================
        // 5. TEXTURAS PROCEDURAIS: AZULEJOS E MADEIRA CLARA
        // ==========================================
        function createTileTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#FAFAFA';
            ctx.fillRect(0, 0, 512, 512);

            ctx.strokeStyle = '#D5D0C8';
            ctx.lineWidth = 4;

            const tileSize = 64;
            for (let x = 0; x <= 512; x += tileSize) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 512); ctx.stroke();
            }
            for (let y = 0; y <= 512; y += tileSize) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(512, y); ctx.stroke();
            }

            const texture = new THREE.CanvasTexture(canvas);
            texture.wrapS = THREE.RepeatWrapping;
            texture.wrapT = THREE.RepeatWrapping;
            texture.repeat.set(10, 2.5);
            return texture;
        }

        function createWoodTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#D4AC6E';
            ctx.fillRect(0, 0, 512, 512);

            for (let i = 0; i < 70; i++) {
                const y = Math.random() * 512;
                ctx.strokeStyle = Math.random() > 0.5 ? 'rgba(140, 95, 40, 0.15)' : 'rgba(235, 195, 130, 0.20)';
                ctx.lineWidth = 1 + Math.random() * 3.5;
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.bezierCurveTo(170, y + (Math.random() - 0.5) * 25, 340, y + (Math.random() - 0.5) * 25, 512, y);
                ctx.stroke();
            }

            const texture = new THREE.CanvasTexture(canvas);
            texture.wrapS = THREE.RepeatWrapping;
            texture.wrapT = THREE.RepeatWrapping;
            texture.repeat.set(4, 1.5);
            return texture;
        }

        // ==========================================
        // 6. MÃOS DO JOGADOR NO POV
        // ==========================================
        function createPOVHand(isRight) {
            const handGroup = new THREE.Group();
            const gloveMat = new THREE.MeshStandardMaterial({ color: 0x1B2A4A, roughness: 0.5, flatShading: true });
            const accentMat = new THREE.MeshStandardMaterial({ color: 0x20B2AA, roughness: 0.3, flatShading: true });

            const palmGeo = new THREE.BoxGeometry(0.08, 0.04, 0.11);
            const palm = new THREE.Mesh(palmGeo, gloveMat);
            palm.castShadow = true;
            handGroup.add(palm);

            const trimGeo = new THREE.BoxGeometry(0.084, 0.015, 0.03);
            const trim = new THREE.Mesh(trimGeo, accentMat);
            trim.position.set(0, 0, 0.045);
            handGroup.add(trim);

            const fingerGeo = new THREE.BoxGeometry(0.018, 0.016, 0.05);
            for (let f = 0; f < 4; f++) {
                const finger = new THREE.Mesh(fingerGeo, gloveMat);
                finger.position.set(-0.03 + f * 0.02, -0.005, -0.075);
                finger.rotation.x = 0.2;
                handGroup.add(finger);
            }

            const thumbGeo = new THREE.BoxGeometry(0.018, 0.016, 0.045);
            const thumb = new THREE.Mesh(thumbGeo, gloveMat);
            thumb.position.set(isRight ? -0.048 : 0.048, 0, -0.03);
            thumb.rotation.y = isRight ? 0.6 : -0.6;
            handGroup.add(thumb);

            if (isRight) {
                const spatHandle = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.01, 0.22), new THREE.MeshStandardMaterial({ color: 0xF26419, flatShading: true }));
                const spatBlade = new THREE.Mesh(new THREE.BoxGeometry(0.065, 0.004, 0.09), new THREE.MeshStandardMaterial({ color: 0xB0B8C0, metalness: 0.8, flatShading: true }));
                spatBlade.position.set(0, 0, -0.13);
                spatHandle.add(spatBlade);

                spatHandle.position.set(0, 0, -0.08);
                spatHandle.rotation.x = -0.3;
                handGroup.add(spatHandle);
            }

            return handGroup;
        }

        const leftPOVHand = createPOVHand(false);
        leftPOVHand.position.set(-0.35, -0.18, -0.45);
        leftPOVHand.rotation.set(0.15, 0.25, -0.1);
        camera.add(leftPOVHand);

        const rightPOVHand = createPOVHand(true);
        rightPOVHand.position.set(0.35, -0.18, -0.45);
        rightPOVHand.rotation.set(0.15, -0.25, 0.1);
        camera.add(rightPOVHand);

        // ==========================================
        // 7. GLTFLOADER ROBUSTO & NORMALIZAÇÃO POR BOUNDING BOX
        // ==========================================
        const gltfLoader = new GLTFLoader();
        const loadedAssets = {};

                const ASSET_LIST = [
            'cooktop.glb', 'frigideira.glb', 'geladeira.glb', 'torradeira.glb',
            'prato-quadrado.glb', 'espatula.glb', 'faca-de-cozinhar.glb', 'faca.glb',
            'colher.glb', 'fuet.glb', 'bottom-pao.glb', 'burger-top.glb',
            'pao-burger.glb', 'fatia-queijo.glb', 'carne-crua-burger.glb',
            'carne-burger.glb', 'tomate.glb', 'tomate-cortado.glb',
            'assadeira.glb', 'saleiro.glb', 'pimenta-do-reino.glb',
            'pote-de-geleia.glb', 'manteiga-de-amendoim.glb', 'garrafa.glb',
            'papel-toalha.glb', 'lixeira.glb'
        ];

                function fitModelToSize(model, targetSize) {
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

        function placeStoveOnFloor(stoveMesh, x, z, targetTopY) {
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
        }

        function fitAndPlaceOnSurface(model, x, surfaceY, z, targetSize = null) {
            return placeOnSurface(model, x, surfaceY, z, targetSize);
        }

        async function loadModel(path) {
            const gltf = await gltfLoader.loadAsync(path);
            const model = gltf.scene;
            model.traverse(child => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                    if (child.material) {
                        const pLower = path.toLowerCase();
                        if (pLower.includes('frigideira') || pLower.includes('fogao') || pLower.includes('espatula') || pLower.includes('faca') || pLower.includes('colher') || pLower.includes('fuet') || pLower.includes('torradeira')) {
                            child.material.metalness = 0.75;
                            child.material.roughness = 0.25;
                        } else if (pLower.includes('prato') || pLower.includes('geladeira')) {
                            child.material.metalness = 0.1;
                            child.material.roughness = 0.18;
                        } else if (pLower.includes('carne') || pLower.includes('pao') || pLower.includes('tomate') || pLower.includes('queijo')) {
                            child.material.metalness = 0.05;
                            child.material.roughness = 0.55;
                        }
                        child.material.needsUpdate = true;
                    }
                }
            });
            model.updateMatrixWorld(true);
            return model;
        }

        async function loadAllAssetsAsync() {
            const textEl = document.getElementById('loading-text');
            let loadedCount = 0;
            const total = ASSET_LIST.length;

            const updateProgress = () => {
                loadedCount += 1;
                if (textEl) {
                    textEl.innerText = `Carregando modelos 3D (${Math.round((loadedCount / total) * 100)}%)...`;
                }
            };

            await Promise.all(ASSET_LIST.map(async (file) => {
                const key = file.replace('.glb', '');
                const path = `./assets/${file}`;
                try {
                    const model = await loadModel(path);
                    loadedAssets[key] = model;
                } catch (error) {
                    console.error(`Erro ao carregar modelo em ${path}:`, error);
                    console.warn(`Ativando modelo procedural de segurança para '${key}'.`);
                } finally {
                    updateProgress();
                }
            }));
        }

        function getAsset(key) {
            let mesh;
            if (loadedAssets[key]) {
                mesh = loadedAssets[key].clone(true);
                mesh.traverse(child => {
                    if (child.isMesh) {
                        child.material = child.material.clone();
                        child.castShadow = true;
                        child.receiveShadow = true;
                    }
                });
            } else {
                mesh = createFallbackMesh(key);
            }
            return mesh;
        }

                function createFallbackMesh(key) {
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
        }

        function createSqueezeBottleMesh(colorHex) {
            const group = new THREE.Group();
            const bottleMat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.4, flatShading: true });
            const capMat = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.3, flatShading: true });

            const bodyGeo = new THREE.CylinderGeometry(0.025, 0.025, 0.12, 10);
            const body = new THREE.Mesh(bodyGeo, bottleMat);
            body.position.y = 0.06;
            body.castShadow = true;
            body.receiveShadow = true;
            group.add(body);

            const coneGeo = new THREE.ConeGeometry(0.025, 0.03, 10);
            const cone = new THREE.Mesh(coneGeo, bottleMat);
            cone.position.y = 0.135;
            cone.castShadow = true;
            group.add(cone);

            const tipGeo = new THREE.CylinderGeometry(0.004, 0.008, 0.025, 8);
            const tip = new THREE.Mesh(tipGeo, capMat);
            tip.position.y = 0.15;
            tip.castShadow = true;
            group.add(tip);

            return group;
        }

        function createBowlMesh(contentColorHex, contentType = 'sauce') {
            const group = new THREE.Group();
            const bowlMat = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.3, flatShading: true });

            const bowlGeo = new THREE.CylinderGeometry(0.06, 0.04, 0.045, 12);
            const bowl = new THREE.Mesh(bowlGeo, bowlMat);
            bowl.position.y = 0.0225;
            bowl.castShadow = true;
            bowl.receiveShadow = true;
            group.add(bowl);

            if (contentType === 'sauce') {
                const fillGeo = new THREE.CylinderGeometry(0.055, 0.05, 0.01, 12);
                const fillMat = new THREE.MeshStandardMaterial({ color: contentColorHex, roughness: 0.2, flatShading: true });
                const fill = new THREE.Mesh(fillGeo, fillMat);
                fill.position.y = 0.038;
                group.add(fill);
            }

            return group;
        }

        function createKnifeBlockMesh() {
            const group = new THREE.Group();
            const woodMat = new THREE.MeshStandardMaterial({ color: 0x8B4513, roughness: 0.5, flatShading: true });
            const blockGeo = new THREE.BoxGeometry(0.08, 0.14, 0.12);
            const block = new THREE.Mesh(blockGeo, woodMat);
            block.rotation.x = -0.3;
            block.position.y = 0.06;
            block.castShadow = true;
            block.receiveShadow = true;
            group.add(block);
            return group;
        }

        function createUtensilJarMesh() {
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

        // ==========================================
        // 8. CENÁRIO DA COZINHA E ORGANIZAÇÃO SIMÉTRICA DAS 3 ESTAÇÕES
        // ==========================================
        function buildKitchen() {
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
}

        // 9. PAINEL DE RECEITA ESTILO TV FIXADO NA PAREDE
// ==========================================
let recipeBoardMesh = null;
let recipeCanvasCtx = null;
let recipeTexture = null;

function createRecipeBoard() {
const canvas = document.createElement('canvas');
canvas.width = 600;
canvas.height = 360;
recipeCanvasCtx = canvas.getContext('2d');

recipeTexture = new THREE.CanvasTexture(canvas);
const boardGeo = new THREE.PlaneGeometry(0.90, 0.54);
const boardMat = new THREE.MeshBasicMaterial({ map: recipeTexture, transparent: true });
recipeBoardMesh = new THREE.Mesh(boardGeo, boardMat);
recipeBoardMesh.position.set(0.0, 1.75, -1.87);
scene.add(recipeBoardMesh);

updateRecipeBoard();
}

function updateRecipeBoard() {
if (!recipeCanvasCtx) return;

const ctx = recipeCanvasCtx;
ctx.clearRect(0, 0, 600, 360);

ctx.fillStyle = '#1B2A4A';
ctx.roundRect(10, 10, 580, 340, 18);
ctx.fill();

ctx.lineWidth = 8;
ctx.strokeStyle = '#20B2AA';
ctx.roundRect(10, 10, 580, 340, 18);
ctx.stroke();

const recipe = gameEngine.getCurrentRecipe();

ctx.fillStyle = '#FFD700';
ctx.font = 'bold 26px "Outfit", sans-serif';
ctx.fillText(`RECEITA: ${recipe.name.toUpperCase()}`, 30, 55);

ctx.font = '20px "Outfit", sans-serif';

let yOffset = 110;
recipe.steps.forEach((step, idx) => {
const isCompleted = gameEngine.stackedItems.length > idx;
const isCurrent = gameEngine.stackedItems.length === idx;

if (isCompleted) {
ctx.fillStyle = '#06D6A0';
ctx.fillText(`✓ ${idx + 1}. ${step.label}`, 30, yOffset);
} else if (isCurrent) {
ctx.fillStyle = '#FFD700';
ctx.fillText(`▶ ${idx + 1}. ${step.label}`, 30, yOffset);
} else {
ctx.fillStyle = '#A0AEC0';
ctx.fillText(`  ${idx + 1}. ${step.label}`, 30, yOffset);
}
yOffset += 42;
});

recipeTexture.needsUpdate = true;
}

// ==========================================
// 10. GERENCIADOR DE JOGABILIDADE E RECEITAS
// ==========================================
const RECIPES = {
classic: {
name: "Hambúrguer Clássico",
steps: [
{ type: 'bottom-pao', label: 'Pão de Baixo' },
{ type: 'carne-burger', label: 'Carne Grelhada' },
{ type: 'fatia-queijo', label: 'Queijo Fatiado' },
{ type: 'burger-top', label: 'Pão de Cima' }
]
},
double: {
name: "Cheeseburger Duplo",
steps: [
{ type: 'bottom-pao', label: 'Pão de Baixo' },
{ type: 'carne-burger', label: 'Carne Grelhada (1ª)' },
{ type: 'fatia-queijo', label: 'Queijo Fatiado (1º)' },
{ type: 'carne-burger', label: 'Carne Grelhada (2ª)' },
{ type: 'fatia-queijo', label: 'Queijo Fatiado (2º)' },
{ type: 'burger-top', label: 'Pão de Cima' }
]
}
};

class GameEngine {
constructor() {
this.currentRecipeKey = 'classic';
this.score = 0;
this.timeLeft = 60;
this.timerInterval = null;
this.stackedItems = [];
this.assemblyHeight = 0.9320; // Base do prato central em Y = 0.9220 + 0.010 = 0.9320
this.isPlaying = true;

this.initTimer();
}

getCurrentRecipe() {
return RECIPES[this.currentRecipeKey];
}

setRecipe(key) {
this.currentRecipeKey = key;
this.resetAssembly();
updateRecipeBoard();
}

initTimer() {
if (this.timerInterval) clearInterval(this.timerInterval);
this.timeLeft = 60;
this.updateTimerUI();

this.timerInterval = setInterval(() => {
if (!this.isPlaying) return;
this.timeLeft--;
this.updateTimerUI();

if (this.timeLeft <= 0) {
this.handleTimeOut();
}
}, 1000);
}

startTimer() {
this.initTimer();
}

updateTimerUI() {
const el = document.getElementById('timer-val');
const box = document.getElementById('timer-box');
if (el) el.innerText = this.timeLeft;

if (this.timeLeft <= 15) {
box.classList.add('warning');
} else {
box.classList.remove('warning');
}
}

addScore(pts) {
this.score += pts;
document.getElementById('score-val').innerText = this.score;
}

resetAssembly() {
this.stackedItems.forEach(item => {
scene.remove(item.mesh);
});
this.stackedItems = [];
this.assemblyHeight = 0.9320;

if (pattyController) pattyController.reset();

resetAllTrayIngredients();
updateRecipeBoard();
}

trySnapToPlate(itemObj) {
const recipe = this.getCurrentRecipe();
const nextStepIdx = this.stackedItems.length;

if (nextStepIdx >= recipe.steps.length) return false;

const expectedType = recipe.steps[nextStepIdx].type;

if (itemObj.type === expectedType) {
audioManager.playPop();

const platePos = new THREE.Vector3(0.0, this.assemblyHeight, -0.65);
vfxManager.addLerp(itemObj.mesh, platePos);

const heights = {
'bottom-pao': 0.032,
'carne-burger': 0.024,
'fatia-queijo': 0.008,
'burger-top': 0.045
};
this.assemblyHeight += (heights[itemObj.type] || 0.02);

this.stackedItems.push(itemObj);

const idx = interactiveItems.indexOf(itemObj);
if (idx !== -1) interactiveItems.splice(idx, 1);

updateRecipeBoard();

if (itemObj.type === 'carne-burger' && pattyController) {
pattyController.onPattyPlacedOnPlate();
} else {
spawnSingleTrayReplacement(itemObj.type);
}

if (this.stackedItems.length === recipe.steps.length) {
this.handleVictory();
}
return true;
} else {
return false;
}
}

verifyOrder() {
const recipe = this.getCurrentRecipe();
if (!recipe) return false;
const isComplete = this.stackedItems.length === recipe.steps.length;
if (isComplete) {
this.handleVictory();
}
return isComplete;
}

handleVictory() {
this.isPlaying = false;
audioManager.playVictoryFanfare();
vfxManager.spawnConfetti();

const bonusPoints = 1000 + (this.timeLeft * 25);
this.addScore(bonusPoints);

document.getElementById('victory-score-val').innerText = `+${bonusPoints} pts`;
document.getElementById('victory-modal').classList.add('active');
}

handleTimeOut() {
this.isPlaying = false;
if (pattyController && pattyController.state === 1) {
audioManager.stopSizzle();
vfxManager.stopSmoke();
}
document.getElementById('fail-modal').classList.add('active');
}

restartOrder() {
this.resetAssembly();
this.isPlaying = true;
this.initTimer();
document.getElementById('victory-modal').classList.remove('active');
document.getElementById('fail-modal').classList.remove('active');
}
}

// ==========================================


        // ==========================================
        // 11. MÁQUINA DE ESTADOS DA CARNE
        // ==========================================
        class PattyController {
            constructor() {
                this.state = 0; // 0: CRUA, 1: FRITANDO, 2: PRONTA
                this.mesh = null;
                this.cookStartTime = 0;
                this.cookDuration = 3000;
                this.skilletPos = window.skilletCenter || new THREE.Vector3(-1.15, 0.9250, -0.55);
                this.trayPos = window.meatTrayCenter || new THREE.Vector3(-1.55, 0.9280, -0.50);

                this.rawColor = new THREE.Color(0xA03333);
                this.cookedColor = new THREE.Color(0x4A2511);

                this.spawnRawPatty();
            }

            spawnRawPatty() {
                if (this.mesh) {
                    scene.remove(this.mesh);
                    const idx = interactiveItems.findIndex(i => i.mesh === this.mesh);
                    if (idx !== -1) interactiveItems.splice(idx, 1);
                }

                this.mesh = getAsset('carne-crua-burger');
                fitAndPlaceOnSurface(this.mesh, this.trayPos.x, this.trayPos.y, this.trayPos.z, 0.15);
                scene.add(this.mesh);

                this.state = 0;

                const interactiveObj = {
                    mesh: this.mesh,
                    type: 'carne-crua',
                    controller: this,
                    originalPos: this.mesh.position.clone()
                };

                interactiveItems.push(interactiveObj);
            }

            startCooking() {
                if (this.state !== 0) return;

                this.state = 1;
                audioManager.startSizzle();
                vfxManager.startSmoke();

                vfxManager.addLerp(this.mesh, this.skilletPos);
                this.cookStartTime = performance.now();
            }

            updateCookingProgress(now) {
                if (this.state !== 1) return;

                const elapsed = now - this.cookStartTime;
                const progress = Math.min(elapsed / this.cookDuration, 1.0);

                this.mesh.traverse(child => {
                    if (child.isMesh && child.material && child.material.color) {
                        child.material.color.lerpColors(this.rawColor, this.cookedColor, progress);
                    }
                });

                if (progress >= 1.0) {
                    this.finishCooking();
                }
            }

            finishCooking() {
                this.state = 2;
                audioManager.stopSizzle();
                vfxManager.stopSmoke();
                audioManager.playPop();

                const oldMesh = this.mesh;
                const targetPos = this.skilletPos.clone();

                const cookedMesh = getAsset('carne-burger');
                fitAndPlaceOnSurface(cookedMesh, targetPos.x, targetPos.y, targetPos.z, 0.15);
                scene.add(cookedMesh);

                scene.remove(oldMesh);
                this.mesh = cookedMesh;

                const itemObj = interactiveItems.find(i => i.mesh === oldMesh);
                if (itemObj) {
                    itemObj.mesh = cookedMesh;
                    itemObj.type = 'carne-burger';
                    itemObj.isCooked = true;
                    itemObj.originalPos = cookedMesh.position.clone();
                }
            }

            onPattyPlacedOnPlate() {
                this.mesh = null;
                this.state = 0;
                this.spawnRawPatty();
            }

            reset() {
                audioManager.stopSizzle();
                vfxManager.stopSmoke();
                this.spawnRawPatty();
            }
        }

        // ==========================================
        // 12. POSICIONAMENTO ORGANIZADO DOS INGREDIENTES DE PREPARO (Estação 3)
        // ==========================================
        const ANCHORS = {
            'bottom-pao': { x: 0.68, z: -0.60, size: 0.15 },
            'fatia-queijo': { x: 0.85, z: -0.60, size: 0.14 },
            'burger-top': { x: 1.02, z: -0.60, size: 0.15 }
        };

        const interactiveItems = [];
        let pattyController = null;
        let gameEngine = null;

        function resetAllTrayIngredients() {
            for (let i = interactiveItems.length - 1; i >= 0; i--) {
                if (interactiveItems[i].type !== 'carne-crua' && interactiveItems[i].type !== 'carne-burger') {
                    scene.remove(interactiveItems[i].mesh);
                    interactiveItems.splice(i, 1);
                }
            }

            ['bottom-pao', 'burger-top', 'fatia-queijo'].forEach(type => {
                spawnSingleTrayReplacement(type);
            });
        }

        function spawnSingleTrayReplacement(type) {
            const anchor = ANCHORS[type];
            if (!anchor) return;

            const targetY = window.boardTopY ? window.boardTopY + 0.002 : 0.9360;
            const mesh = getAsset(type);
            placeOnSurface(mesh, anchor.x, targetY, anchor.z, anchor.size);
            scene.add(mesh);

            interactiveItems.push({
                mesh: mesh,
                type: type,
                originalPos: mesh.position.clone()
            });
        }

        // ==========================================
        // INICIALIZAÇÃO DA CENA APÓS PRE-CARREGAMENTO ASSÍNCRONO
        // ==========================================
        (async () => {
            try {
                await loadAllAssetsAsync();
            } catch (error) {
                console.error('Falha no pré-carregamento dos modelos .glb:', error);
            } finally {
                const overlay = document.getElementById('loading-overlay');
                if (overlay) {
                    overlay.style.opacity = '0';
                    setTimeout(() => { overlay.style.display = 'none'; }, 500);
                }

                buildKitchen();
                gameEngine = new GameEngine();
                createRecipeBoard();
                pattyController = new PattyController();
                resetAllTrayIngredients();
            }
        })();

        // ==========================================
        // 13. INTERAÇÃO DRAG & DROP / CLIQUE (DESKTOP MOUSE)
        // ==========================================
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const dragPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -0.92);
        const planeIntersect = new THREE.Vector3();

        let draggedItem = null;
        let hoveredMesh = null;

        function getIntersectedItem(e) {
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);

            const meshes = interactiveItems.map(i => i.mesh);
            const intersects = raycaster.intersectObjects(meshes, true);

            if (intersects.length > 0) {
                let hitMesh = intersects[0].object;
                while (hitMesh.parent && hitMesh.parent !== scene) {
                    hitMesh = hitMesh.parent;
                }
                return interactiveItems.find(i => i.mesh === hitMesh);
            }
            return null;
        }

        window.addEventListener('pointermove', (e) => {
            if (draggedItem) {
                mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
                mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
                raycaster.setFromCamera(mouse, camera);

                if (raycaster.ray.intersectPlane(dragPlane, planeIntersect)) {
                    draggedItem.mesh.position.copy(planeIntersect);
                    draggedItem.mesh.position.y = 0.96;
                }
            } else if (gameEngine && gameEngine.isPlaying) {
                const item = getIntersectedItem(e);
                if (item && (item.type !== 'carne-crua' || pattyController.state === 0)) {
                    if (hoveredMesh !== item.mesh) {
                        clearHighlight();
                        hoveredMesh = item.mesh;
                        setHighlight(hoveredMesh, true);
                    }
                } else {
                    clearHighlight();
                }
            }
        });

        window.addEventListener('pointerdown', (e) => {
            if (e.button !== 0 || !gameEngine || !gameEngine.isPlaying) return;

            const item = getIntersectedItem(e);
            if (!item) return;

            audioManager.init();

            if (item.type === 'carne-crua') {
                if (pattyController.state === 0) {
                    pattyController.startCooking();
                }
                return;
            }

            if (pattyController.mesh === item.mesh && pattyController.state === 1) {
                return;
            }

            draggedItem = item;
            controls.enabled = false;
            audioManager.playPop();
        });

        window.addEventListener('pointerup', () => {
            if (!draggedItem) return;

            controls.enabled = true;
            const item = draggedItem;
            draggedItem = null;

            const pos = item.mesh.position;

            const plateDist = pos.distanceTo(new THREE.Vector3(0.0, 0.9220, -0.65));
            if (plateDist < 0.28) {
                const snapped = gameEngine.trySnapToPlate(item);
                if (snapped) return;
            }

            vfxManager.addLerp(item.mesh, item.originalPos);
        });

        function setHighlight(obj, enable) {
            obj.traverse(child => {
                if (child.isMesh && child.material) {
                    if (enable) {
                        child.userData.origEmissive = child.material.emissive ? child.material.emissive.getHex() : 0;
                        if (child.material.emissive) child.material.emissive.setHex(0x20B2AA);
                    } else if (child.userData.origEmissive !== undefined) {
                        if (child.material.emissive) child.material.emissive.setHex(child.userData.origEmissive);
                    }
                }
            });
        }

        function clearHighlight() {
            if (hoveredMesh) {
                setHighlight(hoveredMesh, false);
                hoveredMesh = null;
            }
        }

        // ==========================================
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
        }

        // ==========================================
        // 15. EVENTOS DE UI (Menu, Receitas, Mute & Modais)
        // ==========================================
        document.querySelectorAll('.recipe-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.recipe-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                if (gameEngine) gameEngine.setRecipe(e.target.dataset.recipe);
                audioManager.playPop();
            });
        });

        const muteBtn = document.getElementById('mute-btn');
        muteBtn.addEventListener('click', () => {
            const isMuted = audioManager.toggleMute();
            muteBtn.innerText = isMuted ? '🔇' : '🔊';
            if (isMuted) muteBtn.classList.add('muted');
            else muteBtn.classList.remove('muted');
        });

        document.getElementById('next-order-btn').addEventListener('click', () => {
            if (gameEngine) gameEngine.restartOrder();
            audioManager.playPop();
        });

        document.getElementById('retry-btn').addEventListener('click', () => {
            if (gameEngine) gameEngine.restartOrder();
            audioManager.playPop();
        });

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // ==========================================
        // 16. LOOP PRINCIPAL DE RENDERIZAÇÃO
        // ==========================================
        renderer.setAnimationLoop((timestamp) => {
            controls.update();
            updateVRTeleportPointer();
            vfxManager.update();

            if (pattyController) {
                pattyController.updateCookingProgress(timestamp);
            }

            if (renderer.xr.isPresenting) {
                leftPOVHand.visible = false;
                rightPOVHand.visible = false;
            } else {
                leftPOVHand.visible = true;
                rightPOVHand.visible = true;
            }

            controllers.forEach(controller => {
                if (controller.userData.selectedItem) {
                    const item = controller.userData.selectedItem;
                    const p = new THREE.Vector3();
                    controller.getWorldPosition(p);
                    item.mesh.position.copy(p);
                }
            });

            renderer.render(scene, camera);
        });
    