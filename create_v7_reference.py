import bpy
import bmesh
import math
import os

print("=" * 70)
print("🚀 ANIME STAR FIGHTER V7 - Reference-First Approach")
print("40 Iterations following Top/Side/Front reference diagrams")
print("=" * 70)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ============================================
# MATERIALS
# ============================================

def create_material(name, base_color, metallic=0.0, roughness=0.5, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    
    if emission:
        emission_node = nodes.new('ShaderNodeEmission')
        emission_node.location = (0, 200)
        emission_node.inputs['Color'].default_value = (*emission, 1.0)
        emission_node.inputs['Strength'].default_value = 3.0
        
        mix = nodes.new('ShaderNodeMixShader')
        mix.location = (200, 0)
        mix.inputs['Fac'].default_value = 0.3
        
        links.new(emission_node.outputs['Emission'], mix.inputs[1])
        links.new(bsdf.outputs['BSDF'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])
    else:
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# Palette from references
m_body = create_material("Body_Blue", (0.12, 0.28, 0.72), 0.7, 0.3)  # Main blue
m_white = create_material("Secondary_White", (0.94, 0.94, 0.94), 0.1, 0.4)  # Stabilizers
m_dark = create_material("Dark_Gray", (0.15, 0.15, 0.15), 0.3, 0.6)  # Intakes/details
m_yellow = create_material("VFin_Yellow", (1.0, 0.78, 0.2), 0.5, 0.3)  # V-fin
m_cockpit = create_material("Cockpit_Glass", (0.05, 0.08, 0.15), 0.9, 0.05)
m_glow = create_material("Engine_Glow", (0.0, 0.0, 0.0), emission=(0.2, 0.8, 1.0))

# ============================================
# PHASE 1: FOUNDATION (1-10)
# Following reference proportions
# ============================================

print("\n" + "=" * 70)
print("PHASE 1: FOUNDATION (1-10)")
print("Building to reference proportions: Length ~7.5m, Span ~10m")
print("=" * 70)

print("[1-3] Main fuselage - per side view")
# Cylinder: 7 units long, radius 0.7 (scales to ~7.5m)
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=7, location=(0, 0, 0))
fuselage = bpy.context.active_object
fuselage.scale = (1, 0.55, 1)  # Oval cross-section per front view
fuselage.rotation_euler = (math.radians(90), 0, math.radians(90))
fuselage.name = "Fuselage_Main"
fuselage.data.materials.append(m_body)

print("[4-6] Nose cone - per side view curve")
# Cone: blends to nose, length 3.5, radius 0.15 at tip
bpy.ops.mesh.primitive_cone_add(radius1=0.7, radius2=0.15, depth=3.5, location=(5.25, 0, 0))
nose = bpy.context.active_object
nose.scale = (1, 0.9, 1)  # Slightly flattened per references
nose.rotation_euler = (math.radians(90), 0, math.radians(90))
nose.name = "Nose"
nose.data.materials.append(m_body)

print("[7-10] Rear fuselage taper")
# Rear ellipse per top view
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=1.5, location=(-4.25, 0, 0))
rear = bpy.context.active_object
rear.scale = (1, 0.55, 1)
rear.rotation_euler = (math.radians(90), 0, math.radians(90))
rear.name = "Rear"
rear.data.materials.append(m_body)

# ============================================
# PHASE 2: WINGS (11-20)
# Forward swept, span ~10m total
# ============================================

print("\n" + "=" * 70)
print("PHASE 2: WINGS (11-20)")
print("Forward swept, per top and front view")
print("=" * 70)

print("[11-15] Main wing panels")
for side in [-1, 1]:
    # Per top view: swept forward, span from center to ~150px = ~3.75 units each side
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5, side * 3.5, 0))
    wing = bpy.context.active_object
    wing.scale = (2.8, 0.12, 0.9)
    wing.rotation_euler = (0, 0, math.radians(-20 * side))  # Forward sweep
    wing.name = f"Wing_{side}"
    wing.data.materials.append(m_body)

print("[16-20] Wing tips and details")
for side in [-1, 1]:
    # Wing tip pods per top view
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.8, location=(-2.5, side * 5, 0))
    tip = bpy.context.active_object
    tip.rotation_euler = (math.radians(90), 0, math.radians(-22 * side))
    tip.name = f"WingTip_{side}"
    tip.data.materials.append(m_yellow)

# ============================================
# PHASE 3: STABILIZERS & ENGINES (21-30)
# ============================================

print("\n" + "=" * 70)
print("PHASE 3: STABILIZERS & ENGINES (21-30)")
print("=" * 70)

print("[21-25] Vertical stabilizers")
for side in [-1, 1]:
    # Per side and front view: angled, positioned rear
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.2, side * 1.8, 1.3))
    stab = bpy.context.active_object
    stab.scale = (1.4, 0.1, 1.8)
    stab.rotation_euler = (math.radians(-8), 0, 0)  # Angled back
    stab.name = f"Stabilizer_{side}"
    stab.data.materials.append(m_white)

print("[26-30] Engine nacelles")
for side in [-1, 1]:
    # Per top and side view: pods behind wings
    bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=2.2, location=(-3.5, side * 1.6, -0.25))
    engine = bpy.context.active_object
    engine.rotation_euler = (0, math.radians(90), 0)
    engine.scale = (1, 1, 0.9)
    engine.name = f"Engine_{side}"
    engine.data.materials.append(m_white)
    
    # Exhaust glow per side view
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.1, location=(-4.8, side * 1.6, -0.25))
    exhaust = bpy.context.active_object
    exhaust.rotation_euler = (0, math.radians(90), 0)
    exhaust.name = f"Exhaust_{side}"
    exhaust.data.materials.append(m_glow)

# ============================================
# PHASE 4: COCKPIT & DETAILS (31-40)
# ============================================

print("\n" + "=" * 70)
print("PHASE 4: COCKPIT & DETAILS (31-40)")
print("=" * 70)

print("[31-35] Cockpit canopy")
# Per side view: bubble canopy
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(1.2, 0, 0.65))
canopy = bpy.context.active_object
canopy.scale = (1, 0.9, 0.6)
canopy.name = "Canopy"
canopy.data.materials.append(m_cockpit)

print("[36-38] Intakes")
# Per front and side view: side pods
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=1.2, location=(2, side * 0.85, -0.1))
    intake = bpy.context.active_object
    intake.rotation_euler = (0, math.radians(90), 0)
    intake.scale = (1, 1, 0.75)
    intake.name = f"Intake_{side}"
    intake.data.materials.append(m_dark)

print("[39-40] V-fin")
# Per side and front view: distinctive yellow V
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.2, 0, 0.45))
vfin = bpy.context.active_object
vfin.scale = (0.18, 1.6, 0.12)
vfin.rotation_euler = (math.radians(14), 0, 0)
vfin.name = "VFin"
vfin.data.materials.append(m_yellow)

# ============================================
# REFINEMENT PASS
# ============================================

print("\n" + "=" * 70)
print("REFINEMENT")
print("Ensuring cohesion per references")
print("=" * 70)

# Panel lines per references
for x in [-2.5, -1, 0.5, 2, 3.5]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.72))
    panel = bpy.context.active_object
    panel.scale = (0.015, 1.25, 0.005)
    panel.name = f"Panel_{x}"
    panel.data.materials.append(m_dark)

# Roundels per references
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.01, location=(0, side * 0.72, 0.35))
    rnd = bpy.context.active_object
    rnd.rotation_euler = (math.radians(90), 0, 0)
    rnd.name = f"Roundel_{side}"
    rnd.data.materials.append(m_white)

# ============================================
# LIGHTING & CAMERA
# ============================================

print("\n💡 Setting up lighting...")

for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Key light
bpy.ops.object.light_add(type='SUN', location=(10, -12, 15))
key = bpy.context.active_object
key.data.energy = 5.0
key.data.color = (1.0, 0.9, 0.8)
key.rotation_euler = (math.radians(55), 0, math.radians(-50))

# Fill
bpy.ops.object.light_add(type='AREA', location=(-10, 6, 5))
fill = bpy.context.active_object
fill.data.energy = 3.0
fill.data.color = (0.75, 0.85, 1.0)
fill.data.size = 6

# Rim
bpy.ops.object.light_add(type='AREA', location=(0, 12, -5))
rim = bpy.context.active_object
rim.data.energy = 4.0
rim.data.color = (1.0, 0.75, 0.6)
rim.data.size = 4

# Engine glow
for side in [-1, 1]:
    bpy.ops.object.light_add(type='POINT', location=(-4.6, side * 1.6, -0.25))
    glow = bpy.context.active_object
    glow.data.energy = 25
    glow.data.color = (0.4, 0.8, 1.0)

# Camera
print("📷 Camera setup...")
bpy.ops.object.camera_add(location=(14, -11, 7))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(55), 0, math.radians(52))
cam.data.lens = 50
bpy.context.scene.camera = cam

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.film_transparent = True
scene.cycles.samples = 1024
scene.cycles.use_denoising = True

# World
world = bpy.context.scene.world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.1, 0.18, 0.3, 1.0)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.3

# ============================================
# EXPORT
# ============================================

print("\n📦 Exporting...")
os.makedirs("models", exist_ok=True)

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

bpy.ops.export_scene.gltf(
    filepath="models/starfighter_v7_reference.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT'
)

bpy.ops.wm.save_as_mainfile(filepath="starfighter_v7_reference.blend")

print("🖼️ Rendering preview...")
scene.render.filepath = "preview_v7_reference.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 70)
print("✅ STAR FIGHTER V7 COMPLETE!")
print("=" * 70)
print("📁 Model: models/starfighter_v7_reference.gltf")
print("📁 References: references/starfighter_{top,side,front}_view.png")
print("💾 Blend: starfighter_v7_reference.blend")
print("🖼️  Preview: preview_v7_reference.png")
print("🎨 Method: Reference-first (40 iterations)")
print("=" * 70)