// Production-Grade 3D CPU Visualization
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();

// Camera setup for "Product Reveal" angle
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(4, 3, 6); // Angled View
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

const cpuGroup = new THREE.Group();
scene.add(cpuGroup);

// --- MATERIALS ---
// --- MATERIALS (STEALTH MODE) ---
// 1. PCB - Deep Matte Black
const matPCB = new THREE.MeshPhysicalMaterial({
    color: 0x050505,
    roughness: 0.9,
    metalness: 0.1,
    clearcoat: 0.0,
});

// 2. Heat Spreader/Sync - Dark Brushed Metal (Gunmetal)
const matDarkMetal = new THREE.MeshStandardMaterial({
    color: 0x222222,
    roughness: 0.4,
    metalness: 0.9,
});

// 3. Gold Contacts (Accents)
const matGold = new THREE.MeshStandardMaterial({
    color: 0xffd700,
    roughness: 0.2,
    metalness: 1.0,
});

// 4. Accent Light (LEDs or Capacitors)
const matAccent = new THREE.MeshStandardMaterial({
    color: 0x333333,
    emissive: 0x000000,
});


// --- CPU GEOMETRY ---
// 1. Base PCB
const pcbGeo = new THREE.BoxGeometry(2.5, 0.1, 2.5);
const pcb = new THREE.Mesh(pcbGeo, matPCB);
cpuGroup.add(pcb);

// 2. Heat Spreader (The visible metal top) with BRANDING
const canvas = document.createElement('canvas');
canvas.width = 512;
canvas.height = 512;
const ctx = canvas.getContext('2d');

// Dark metal background
ctx.fillStyle = '#1a1a1a';
ctx.fillRect(0, 0, 512, 512);

// Text - Gold for contrast
ctx.font = 'bold 48px Arial';
ctx.fillStyle = '#d4af37'; // Metallic Gold
ctx.textAlign = 'center';
ctx.translate(256, 256);
ctx.rotate(-Math.PI / 2);
ctx.rotate(Math.PI / 2);
ctx.fillText('WasteCompute', 0, 0);
ctx.font = '24px Arial';
ctx.fillStyle = '#888';
ctx.fillText('E PYC 9004', 0, 40);

const brandTexture = new THREE.CanvasTexture(canvas);

const ihsMat = new THREE.MeshStandardMaterial({
    map: brandTexture,
    color: 0xffffff,
    roughness: 0.4,
    metalness: 0.6,
});

const ihsBaseGeo = new THREE.BoxGeometry(1.8, 0.1, 1.8);
const ihsBase = new THREE.Mesh(ihsBaseGeo, matDarkMetal);
ihsBase.position.y = 0.1;
cpuGroup.add(ihsBase);

const ihsTopGeo = new THREE.BoxGeometry(1.4, 0.05, 1.4);
const ihsTop = new THREE.Mesh(ihsTopGeo, ihsMat);
ihsTop.position.y = 0.175;
cpuGroup.add(ihsTop);

// 3. Gold Pins
const pinsGeo = new THREE.BoxGeometry(2.4, 0.05, 2.4);
const pins = new THREE.Mesh(pinsGeo, matGold);
pins.position.y = -0.075;
cpuGroup.add(pins);

// 4. Capacitors (Stealth Brown/Grey)
const capGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.15, 8);
for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    const cap = new THREE.Mesh(capGeo, matAccent);
    cap.rotation.x = Math.PI / 2;
    cap.position.set(Math.cos(angle) * 1.0, 0.06, Math.sin(angle) * 1.0);
    cpuGroup.add(cap);
}

// 5. Alignment Notch
const notchGeo = new THREE.BoxGeometry(0.2, 0.12, 0.1);
const notch = new THREE.Mesh(notchGeo, new THREE.MeshBasicMaterial({ color: 0x000000 }));
notch.position.set(0, 0.05, 1.25);
cpuGroup.add(notch);

// Socket Retention Frame (Silver rim around IHS) - NEW DETAIL
const frameGeo = new THREE.BoxGeometry(2.0, 0.08, 2.0);
const frame = new THREE.Mesh(frameGeo, matDarkMetal);
frame.position.y = 0.08;
cpuGroup.add(frame);


// --- GPU GEOMETRY (RTX 5090 "VANGUARD" SOC Edition) ---
const gpuGroup = new THREE.Group();
// Added to hardwareGroup later

// 0. Dimensions (Massive 4-Slot Card)
const cardLength = 4.5;
const cardWidth = 1.6;
const cardThick = 0.9;

// Materials
const matShroud = new THREE.MeshStandardMaterial({
    color: 0x111111,
    roughness: 0.2,
    metalness: 0.8
});
const matCarbon = new THREE.MeshStandardMaterial({
    color: 0x050505,
    roughness: 0.8,
    metalness: 0.2, // Carbon fiber-ish
});
const matRGB_Pink = new THREE.MeshStandardMaterial({
    color: 0xff00ff,
    emissive: 0xff00ff,
    emissiveIntensity: 2.0
});
const matRGB_Cyan = new THREE.MeshStandardMaterial({
    color: 0x00ffff,
    emissive: 0x00ffff,
    emissiveIntensity: 2.0
});


// 1. Backplate / PCB (Unibody Base)
const baseGeo = new THREE.BoxGeometry(cardLength, cardWidth, 0.1);
const base = new THREE.Mesh(baseGeo, matDarkMetal);
base.position.z = -cardThick / 2;
gpuGroup.add(base);

// 2. Main Shroud (Angled & Aggressive)
const shroudGeo = new THREE.BoxGeometry(cardLength, cardWidth, cardThick * 0.8);
const shroud = new THREE.Mesh(shroudGeo, matShroud);
// Cutouts would be complex, so we layer "Armor Plates"
gpuGroup.add(shroud);

// Decorative Dividers (Between Fans)
// Midpoint between -1.5 and 0 is -0.75
// Midpoint between 0 and 1.5 is 0.75
// Gap is approx 0.3 wide.
const dividerGeo = new THREE.BoxGeometry(0.15, 1.3, 0.95); // Vertical bars
const divider1 = new THREE.Mesh(dividerGeo, matCarbon);
divider1.position.set(-0.75, 0, 0);
gpuGroup.add(divider1);

const divider2 = new THREE.Mesh(dividerGeo, matCarbon);
divider2.position.set(0.75, 0, 0);
gpuGroup.add(divider2);

// 3. RGB Accents (The "Vanguard" Look)
// Angled Slashes
const slashGeo = new THREE.BoxGeometry(0.8, 0.1, 0.92);
const slash1 = new THREE.Mesh(slashGeo, matRGB_Pink);
slash1.rotation.z = 0.5;
slash1.position.set(-1.8, -0.5, 0);
gpuGroup.add(slash1);

const slash2 = new THREE.Mesh(slashGeo, matRGB_Cyan);
slash2.rotation.z = -0.5;
slash2.position.set(1.8, 0.5, 0);
gpuGroup.add(slash2);


// 4. Triple Fans (Massive)
const fanBladeMat = new THREE.MeshStandardMaterial({ color: 0x444444, roughness: 0.5, metalness: 0.6 });
const fans = [];

for (let i = 0; i < 3; i++) {
    const fanGroup = new THREE.Group();
    // Position 3 fans across the length
    const xPositions = [-1.5, 0, 1.5]; // Spacing Fix (Wider)
    const xPos = xPositions[i];
    fanGroup.position.set(xPos, 0, cardThick / 2 + 0.05);

    // Fan Rim (RGB Ring)
    const ringGeo = new THREE.RingGeometry(0.55, 0.6, 32);
    const ringMat = (i === 1) ? matRGB_Pink : matRGB_Cyan; // Middle fan different
    const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: ringMat.color }));
    fanGroup.add(ring);

    // Blades
    for (let j = 0; j < 9; j++) {
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.05), fanBladeMat);
        blade.rotation.z = (j / 9) * Math.PI * 2;
        blade.position.set(
            Math.cos(blade.rotation.z) * 0.25,
            Math.sin(blade.rotation.z) * 0.25,
            0
        );
        blade.rotation.x = 0.4;
        fanGroup.add(blade);
    }

    // Hub with MSI Dragon-like fake logo (Gold)
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.1, 16), matGold);
    hub.rotation.x = Math.PI / 2;
    fanGroup.add(hub);

    gpuGroup.add(fanGroup);
    fans.push(fanGroup);
}

// 5. Top Side Branding "WasteCompute" (Glowing Text)
const gpuCanvas = document.createElement('canvas');
gpuCanvas.width = 512;
gpuCanvas.height = 64;
const gpuCtx = gpuCanvas.getContext('2d');
gpuCtx.fillStyle = '#000000';
gpuCtx.fillRect(0, 0, 512, 64);
gpuCtx.font = 'bold 36px Arial';
gpuCtx.fillStyle = '#ffffff'; // White text
gpuCtx.textAlign = 'center';
gpuCtx.textBaseline = 'middle';
gpuCtx.fillText('WasteCompute 5090', 256, 32);

const gpuTextTexture = new THREE.CanvasTexture(gpuCanvas);
const gpuTextMat = new THREE.MeshStandardMaterial({
    map: gpuTextTexture,
    emissive: 0xffffff,
    emissiveMap: gpuTextTexture,
    emissiveIntensity: 1.0
});

const textStripGeo = new THREE.BoxGeometry(2.5, 0.3, 0.02); // Slightly wider and taller for text
const textStrip = new THREE.Mesh(textStripGeo, gpuTextMat);
textStrip.position.set(0, cardWidth / 2 + 0.01, 0); // Just on top edge
textStrip.rotation.x = -Math.PI / 2;
gpuGroup.add(textStrip);

// 6. PCIe Connector
const pcieGeo = new THREE.BoxGeometry(1.2, 0.1, 0.1);
const pcie = new THREE.Mesh(pcieGeo, matGold);
pcie.position.y = -cardWidth / 2 - 0.05;
gpuGroup.add(pcie);

// 7. IO Bracket
const bracketGeo = new THREE.BoxGeometry(0.1, cardWidth * 0.9, cardThick * 1.2);
const bracket = new THREE.Mesh(bracketGeo, new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.6 }));
bracket.position.x = -cardLength / 2 - 0.1;
gpuGroup.add(bracket);


// --- POSITIONING (ENTERPRISE STACK) ---
const hardwareGroup = new THREE.Group();
scene.add(hardwareGroup);

// Shared alignment settings
const angleX = 0.3; // Calmer tilt
const angleY = -0.3; // Subtler face towards text

// CPU (Upper Right - Red Zone)
cpuGroup.position.set(1.8, 1.8, -0.9); // Upper right position
cpuGroup.rotation.set(angleX, angleY, 0);
hardwareGroup.add(cpuGroup);

// GPU (Lower Center - Green Zone)
gpuGroup.position.set(-0.5, -0.9, 0.3); // Lower center position
gpuGroup.rotation.set(angleX, angleY, 0);
gpuGroup.scale.set(0.8, 0.8, 0.8); // Reduced scale
hardwareGroup.add(gpuGroup);


// Positioning based on screen size
if (window.innerWidth > 800) {
    hardwareGroup.position.x = 1.5; // Anchored position (was 2.5)
} else {
    hardwareGroup.position.x = 0;
}


// --- LIGHTING (DRAMATIC STUDIO) ---
// --- LIGHTING ---
const ambientLight = new THREE.AmbientLight(0xffffff, 0.3); // Slightly brighter ambient
scene.add(ambientLight);

// 2. Key Light (Cool White vs Warm Gold)
const keyLight = new THREE.DirectionalLight(0xffffff, 2.0);
keyLight.position.set(5, 5, 5);
scene.add(keyLight);

// 3. Rim Light (Slight Blue for tech)
const rimLight = new THREE.PointLight(0x4488ff, 3.0);
rimLight.position.set(-5, 0, -5);
scene.add(rimLight);

// 4. Under-glow (Gold reflection)
const fillLight = new THREE.PointLight(0xffaa00, 0.8);
fillLight.position.set(0, -5, 0);
scene.add(fillLight);

// --- ANIMATION ---
function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // Spin Fans
    fans.forEach(fan => {
        fan.rotation.z -= 0.15; // Spin on Z axis (axial fan)
    });

    // GLOBAL ROTATION (Slow Turn)
    hardwareGroup.rotation.y = Math.sin(time * 0.1) * 0.1;

    // INDEPENDENT FLOATING (Breathing)
    // CPU bob
    cpuGroup.position.y = 0.5 + Math.sin(time * 0.5) * 0.1;
    // GPU bob (Offset phase)
    gpuGroup.position.y = -0.8 + Math.sin(time * 0.5 + 2.0) * 0.1;

    // Subtle independent tilts
    cpuGroup.rotation.z = Math.sin(time * 0.3) * 0.05;
    gpuGroup.rotation.z = 0.2 + Math.cos(time * 0.4) * 0.05;

    renderer.render(scene, camera);
}

// Responsive
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);

    if (window.innerWidth > 800) {
        cpuGroup.position.x = 2.5;
    } else {
        cpuGroup.position.x = 0;
    }
});

animate();
