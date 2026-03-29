/**
 * OpenClaw 3D Model Viewer
 * Reusable Three.js viewer for all 3D models
 * 
 * Usage:
 * const viewer = new ModelViewer({
 *   container: '#viewer-container',
 *   modelPath: 'models/starfighter.gltf',
 *   autoRotate: true,
 *   enableBloom: true
 * });
 * viewer.load();
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

export class ModelViewer {
  constructor(options = {}) {
    this.container = document.querySelector(options.container || '#viewer-container');
    this.canvas = this.container?.querySelector('canvas') || document.createElement('canvas');
    this.modelPath = options.modelPath || 'model.gltf';
    this.autoRotate = options.autoRotate !== false;
    this.enableBloom = options.enableBloom !== false;
    this.bloomStrength = options.bloomStrength || 0.5;
    this.bloomRadius = options.bloomRadius || 0.4;
    this.bloomThreshold = options.bloomThreshold || 0.85;
    this.cameraPosition = options.cameraPosition || [8, 6, 8];
    this.modelScale = options.modelScale || null; // Auto-scale if null
    this.bgColor = options.bgColor || 0x0a0e17;
    this.gridColor = options.gridColor || 0x1a3a5c;
    
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.composer = null;
    this.controls = null;
    this.model = null;
    this.wireframeMode = false;
    this.animationId = null;
  }

  init() {
    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.bgColor);
    this.scene.fog = new THREE.Fog(this.bgColor, 10, 50);

    // Camera
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
    this.camera.position.set(...this.cameraPosition);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance"
    });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;

    // Post-processing
    if (this.enableBloom) {
      this.composer = new EffectComposer(this.renderer);
      const renderPass = new RenderPass(this.scene, this.camera);
      this.composer.addPass(renderPass);

      const bloomPass = new UnrealBloomPass(
        new THREE.Vector2(this.container.clientWidth, this.container.clientHeight),
        this.bloomStrength,
        this.bloomRadius,
        this.bloomThreshold
      );
      this.composer.addPass(bloomPass);
    }

    // Controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.autoRotate = this.autoRotate;
    this.controls.autoRotateSpeed = 2.0;
    this.controls.minDistance = 3;
    this.controls.maxDistance = 20;
    this.controls.target.set(0, 0, 0);

    // Default lighting
    this.addDefaultLighting();

    // Grid
    const gridHelper = new THREE.GridHelper(20, 20, this.gridColor, this.bgColor + 0x050505);
    gridHelper.position.y = -3;
    this.scene.add(gridHelper);

    // Resize handler
    window.addEventListener('resize', () => this.onResize());

    if (!this.canvas.parentNode) {
      this.container.appendChild(this.canvas);
    }
  }

  addDefaultLighting() {
    // Ambient
    const ambient = new THREE.AmbientLight(0x404040, 0.5);
    this.scene.add(ambient);

    // Key light
    const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
    keyLight.position.set(5, -5, 5);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    this.scene.add(keyLight);

    // Fill light
    const fillLight = new THREE.DirectionalLight(0x88ccff, 0.8);
    fillLight.position.set(-5, 3, 2);
    this.scene.add(fillLight);

    // Rim light
    const rimLight = new THREE.DirectionalLight(0xffaa77, 0.8);
    rimLight.position.set(0, 5, -3);
    this.scene.add(rimLight);
  }

  addPointLight(color, intensity, distance, position) {
    const light = new THREE.PointLight(color, intensity, distance);
    light.position.set(...position);
    this.scene.add(light);
    return light;
  }

  load() {
    this.init();
    
    const loading = this.container.querySelector('#loading');
    if (loading) loading.style.display = 'block';

    const loader = new GLTFLoader();
    loader.load(
      this.modelPath,
      (gltf) => {
        this.onModelLoaded(gltf);
        if (loading) loading.style.display = 'none';
      },
      (xhr) => {
        const progress = (xhr.loaded / xhr.total * 100).toFixed(0);
        console.log(`${progress}% loaded`);
        if (loading) {
          loading.innerHTML = `
            <div class="spinner"></div>
            Loading 3D Model... ${progress}%
          `;
        }
      },
      (error) => {
        console.error('Error loading model:', error);
        if (loading) {
          loading.innerHTML = '<p style="color: #ff6666;">Error loading model</p>';
        }
      }
    );

    this.animate();
  }

  onModelLoaded(gltf) {
    this.model = gltf.scene;

    // Center and scale
    const box = new THREE.Box3().setFromObject(this.model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    
    const scale = this.modelScale || (3 / maxDim);
    this.model.scale.setScalar(scale);
    this.model.position.sub(center.multiplyScalar(scale));

    // Enable shadows and store materials
    this.model.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
        child.userData.originalMaterial = child.material?.clone();
      }
    });

    this.scene.add(this.model);
    
    // Dispatch custom event
    this.container.dispatchEvent(new CustomEvent('modelLoaded', { detail: { model: this.model } }));
  }

  toggleAutoRotate() {
    this.controls.autoRotate = !this.controls.autoRotate;
    return this.controls.autoRotate;
  }

  toggleWireframe() {
    this.wireframeMode = !this.wireframeMode;
    
    if (this.model) {
      this.model.traverse((child) => {
        if (child.isMesh) {
          if (this.wireframeMode) {
            child.material = new THREE.MeshBasicMaterial({
              color: 0x4fc3f7,
              wireframe: true
            });
          } else {
            child.material = child.userData.originalMaterial;
          }
        }
      });
    }
    return this.wireframeMode;
  }

  resetView() {
    this.camera.position.set(...this.cameraPosition);
    this.controls.target.set(0, 0, 0);
    this.controls.update();
  }

  onResize() {
    if (!this.camera || !this.renderer) return;
    
    this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    
    if (this.composer) {
      this.composer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
  }

  animate() {
    this.animationId = requestAnimationFrame(() => this.animate());
    this.controls.update();
    
    if (this.composer) {
      this.composer.render();
    } else {
      this.renderer.render(this.scene, this.camera);
    }
  }

  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    window.removeEventListener('resize', () => this.onResize());
    
    // Cleanup Three.js resources
    this.scene?.traverse((obj) => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) {
          obj.material.forEach(m => m.dispose());
        } else {
          obj.material.dispose();
        }
      }
    });
    
    this.renderer?.dispose();
    this.composer?.dispose();
  }
}

// Auto-initialize if data attributes are present
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('[data-model-viewer]');
  if (container) {
    const options = {
      container: container,
      modelPath: container.dataset.modelPath || 'model.gltf',
      autoRotate: container.dataset.autoRotate !== 'false',
      enableBloom: container.dataset.enableBloom !== 'false'
    };
    
    if (container.dataset.cameraPosition) {
      options.cameraPosition = container.dataset.cameraPosition.split(',').map(Number);
    }
    if (container.dataset.modelScale) {
      options.modelScale = parseFloat(container.dataset.modelScale);
    }
    
    const viewer = new ModelViewer(options);
    viewer.load();
    
    // Expose for button controls
    window.modelViewer = viewer;
  }
});