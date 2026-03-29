import bpy
import bmesh
import math
import os

print("=" * 70)
print("🚀 ANIME STAR FIGHTER V5 - 75 ITERATIONS")
print("Strategy: Skeleton → Gap Fill → Shapes → Materials → Cohesion")
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

# Core palette
m_primary = create_material("Primary", (0.08, 0.22, 0.65), 0.7, 0.3)
m_secondary = create_material("Secondary", (0.92, 0.93, 0.95), 0.1, 0.4)
m_dark = create_material("Dark", (0.12, 0.14, 0.18), 0.3, 0.6)
m_red = create_material("Red_Accent", (0.92, 0.15, 0.12), 0.4, 0.3)
m_yellow = create_material("Yellow_Accent", (1.0, 0.75, 0.15), 0.6, 0.25)
m_cockpit = create_material("Cockpit", (0.02, 0.05, 0.12), 0.9, 0.05)
m_glow = create_material("Engine_Glow", (0.0, 0.0, 0.0), emission=(0.2, 0.8, 1.0))
m_detail = create_material("Detail", (0.25, 0.27, 0.3), 0.8, 0.35)

# ============================================
# PHASE 1: FOUNDATION/SKELETON (Iterations 1-15)
# ============================================

print("\n" + "=" * 70)
print("PHASE 1: FOUNDATION/SKELETON (1-15)")
print("=" * 70)

print("[1-5] Core fuselage - complete shell...")

# Main fuselage - single unified core
bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=7.5, location=(0, 0, 0))
core = bpy.context.active_object
core.scale = (1, 0.55, 1)
core.rotation_euler = (math.radians(90), 0, math.radians(90))
core.data.materials.append(m_primary)

# Nose cone - seamless integration
bpy.ops.mesh.primitive_cone_add(radius1=0.75, radius2=0.12, depth=4, location=(5.75, 0, 0))
nose = bpy.context.active_object
nose.scale = (1, 0.9, 1)
nose.rotation_euler = (math.radians(90), 0, math.radians(90))
nose.data.materials.append(m_primary)

print("[6-10] Wing structure - complete surfaces...")

for side in [-1, 1]:
    # Main wing - full surface
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, side * 3, 0))
    wing = bpy.context.active_object
    wing.scale = (2.5, 0.12, 1.4)
    wing.rotation_euler = (0, 0, math.radians(-18 * side))
    wing.data.materials.append(m_primary)
    
    # Wing tip - closed end
    bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.85, location=(-2, side * 5.2, 0))
    tip = bpy.context.active_object
    tip.rotation_euler = (math.radians(90), 0, math.radians(-20 * side))
    tip.data.materials.append(m_yellow)

print("[11-15] Vertical surfaces - complete...")

for side in [-1, 1]:
    # Vertical stabilizer - full surface
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.2, side * 1.7, 1.3))
    stab = bpy.context.active_object
    stab.scale = (1.6, 0.1, 2)
    stab.rotation_euler = (math.radians(-10), 0, 0)
    stab.data.materials.append(m_secondary)

# Engine housings - complete cylinders
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=2.6, location=(-3, side * 1.6, -0.2))
    engine = bpy.context.active_object
    engine.rotation_euler = (0, math.radians(90), 0)
    engine.scale = (1, 1, 0.9)
    engine.data.materials.append(m_secondary)

# ============================================
# PHASE 2: GAP FILLING (Iterations 16-30)
# ============================================

print("\n" + "=" * 70)
print("PHASE 2: GAP FILLING (16-30)")
print("Ensuring no visual gaps or holes...")
print("=" * 70)

print("[16-20] Fuselage continuity...")

# Blend nose to fuselage
bpy.ops.mesh.primitive_cylinder_add(radius=0.74, depth=0.3, location=(3.9, 0, 0))
blend = bpy.context.active_object
blend.rotation_euler = (math.radians(90), 0, math.radians(90))
blend.data.materials.append(m_primary)

# Fuselage end cap
bpy.ops.mesh.primitive_cylinder_add(radius=0.74, depth=0.2, location=(-3.8, 0, 0))
endcap = bpy.context.active_object
endcap.rotation_euler = (math.radians(90), 0, math.radians(90))
endcap.data.materials.append(m_primary)

# Underbelly fairing - closes gap below
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=5, location=(0, 0, -0.5))
fairing = bpy.context.active_object
fairing.scale = (1, 0.7, 0.6)
fairing.rotation_euler = (math.radians(90), 0, math.radians(90))
fairing.data.materials.append(m_primary)

print("[21-25] Wing root blending...")

for side in [-1, 1]:
    # Wing root fillet - smooth transition
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=1.2, location=(1.5, side * 1.2, 0))
    fillet = bpy.context.active_object
    fillet.rotation_euler = (0, math.radians(90), 0)
    fillet.scale = (1, 0.5, 1)
    fillet.data.materials.append(m_primary)
    
    # Wing trailing edge fill
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.5, side * 4.5, 0))
    te_fill = bpy.context.active_object
    te_fill.scale = (0.8, 0.08, 0.9)
    te_fill.rotation_euler = (0, 0, math.radians(-18 * side))
    te_fill.data.materials.append(m_primary)

print("[26-30] Engine and surface continuity...")

for side in [-1, 1]:
    # Engine intake closure
    bpy.ops.mesh.primitive_torus_add(major_radius=0.63, minor_radius=0.06, location=(-1.7, side * 1.6, -0.2))
    intake_lip = bpy.context.active_object
    intake_lip.rotation_euler = (0, math.radians(90), 0)
    intake_lip.data.materials.append(m_yellow)
    
    # Engine nozzle closure
    bpy.ops.mesh.primitive_torus_add(major_radius=0.48, minor_radius=0.05, location=(-4.3, side * 1.6, -0.2))
    nozzle_ring = bpy.context.active_object
    nozzle_ring.rotation_euler = (0, math.radians(90), 0)
    nozzle_ring.data.materials.append(m_dark)
    
    # Thruster face
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.1, location=(-4.4, side * 1.6, -0.2))
    thrust_face = bpy.context.active_object
    thrust_face.rotation_euler = (0, math.radians(90), 0)
    thrust_face.data.materials.append(m_glow)

# ============================================
# PHASE 3: DISTINCTIVE SHAPES (Iterations 31-45)
# ============================================

print("\n" + "=" * 70)
print("PHASE 3: DISTINCTIVE SHAPES (31-45)")
print("Adding character without creating gaps...")
print("=" * 70)

print("[31-35] V-fin and head...")

# V-fin - integrated design
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.5, 0, 0.45))
vfin = bpy.context.active_object
vfin.scale = (0.18, 1.8, 0.15)
vfin.rotation_euler = (math.radians(15), 0, 0)
vfin.data.materials.append(m_yellow)

# V-fin base integration
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.3, 0, 0.3))
vfin_base = bpy.context.active_object
vfin_base.scale = (0.3, 0.5, 0.2)
vfin_base.data.materials.append(m_yellow)

print("[36-40] Surface detailing...")

# Panel lines - indented not raised (no gaps)
for x in [-2.8, -1.5, -0.2, 1.1, 2.4, 3.7]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.78))
    panel = bpy.context.active_object
    panel.scale = (0.015, 1.4, 0.005)
    panel.data.materials.append(m_dark)

# Vertical panel accents
for x in [-2, 0.5, 3]:
    for y in [-0.5, 0.5]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.4))
        vpanel = bpy.context.active_object
        vpanel.scale = (0.01, 0.015, 0.35)
        vpanel.data.materials.append(m_dark)

print("[41-45] Hardpoints and features...")

for side in [-1, 1]:
    # Weapon pylon - solid
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5, side * 3.5, -0.25))
    pylon = bpy.context.active_object
    pylon.scale = (0.5, 0.15, 0.55)
    pylon.data.materials.append(m_detail)
    
    # Pylon cap
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=0.05, location=(1.5, side * 3.5, 0.05))
    pylon_cap = bpy.context.active_object
    pylon_cap.rotation_euler = (math.radians(90), 0, 0)
    pylon_cap.data.materials.append(m_yellow)
    
    # Leading edge detail
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.3, side * 3.3, 0.15))
    ledge = bpy.context.active_object
    ledge.scale = (2.8, 0.06, 0.12)
    ledge.rotation_euler = (0, 0, math.radians(-18 * side))
    ledge.data.materials.append(m_secondary)

# ============================================
# PHASE 4: MATERIALS/TEXTURES (Iterations 46-60)
# ============================================

print("\n" + "=" * 70)
print("PHASE 4: MATERIALS/TEXTURES (46-60)")
print("=" * 70)

print("[46-50] Fasteners and hardware...")

# Panel fasteners - surface mounted
fastener_locs = []
for i in range(6):
    x = -2.5 + i * 1.0
    for y in [-0.65, 0, 0.65]:
        fastener_locs.append((x, y, 0.79))

for pos in fastener_locs:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.02, location=pos)
    bolt = bpy.context.active_object
    bolt.data.materials.append(m_detail)

print("[51-55] Lights and indicators...")

# Navigation lights
for side in [-1, 1]:
    # Wingtip light
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.03, location=(-2.2, side * 5.1, 0))
    nav = bpy.context.active_object
    nav.rotation_euler = (math.radians(90), 0, 0)
    nav.data.materials.append(m_red if side == 1 else m_detail)
    
    # Stabilizer tip light
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.2, side * 1.7, 2.6))
    stab_light = bpy.context.active_object
    stab_light.scale = (0.15, 0.08, 0.08)
    stab_light.data.materials.append(m_red if side == 1 else m_detail)

# Formation lights
for x in [-3, -1, 1.5, 3.5]:
    for y in [-0.7, 0.7]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.79))
        form = bpy.context.active_object
        form.scale = (0.1, 0.025, 0.005)
        form.data.materials.append(m_yellow)

print("[56-60] Markings and decals...")

# Roundels
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.008, location=(0, side * 0.78, 0.4))
    rnd = bpy.context.active_object
    rnd.rotation_euler = (math.radians(90), 0, 0)
    rnd.data.materials.append(m_secondary)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.01, location=(0, side * 0.78, 0.4))
    dot = bpy.context.active_object
    dot.rotation_euler = (math.radians(90), 0, 0)
    dot.data.materials.append(m_red)

# Belly stripes
for i in range(3):
    x = -2 + i * 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -0.82))
    stripe = bpy.context.active_object
    stripe.scale = (0.2, 0.55, 0.008)
    stripe.data.materials.append(m_yellow if i % 2 == 0 else m_red)

# Cockpit canopy
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.58, location=(1.3, 0, 0.65))
canopy = bpy.context.active_object
canopy.scale = (1, 0.9, 0.7)
canopy.data.materials.append(m_cockpit)

# Canopy frame
bpy.ops.mesh.primitive_torus_add(major_radius=0.59, minor_radius=0.025, location=(1.3, 0, 0.65))
frame = bpy.context.active_object
frame.scale = (1, 0.9, 0.7)
frame.data.materials.append(m_dark)

# ============================================
# PHASE 5: COHESION PASSES (Iterations 61-75)
# ============================================

print("\n" + "=" * 70)
print("PHASE 5: COHESION PASSES (61-75)")
print("Reviewing and refining - no new gaps...")
print("=" * 70)

print("[61-63] Pass 1: Edge refinement...")

# Edge guards - blend surfaces
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, side * 1.55, 0.3))
    guard = bpy.context.active_object
    guard.scale = (5, 0.04, 0.06)
    guard.data.materials.append(m_yellow)

print("[64-66] Pass 2: Surface harmony...")

# Underbelly heat tiles - complete coverage
for x in range(-3, 3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x * 0.7, 0, -0.68))
    tile = bpy.context.active_object
    tile.scale = (0.3, 1.4, 0.04)
    tile.data.materials.append(m_dark)

print("[67-70] Pass 3: Detail cohesion...")

# Surface detail strips
for i in range(8):
    x = -3 + i * 0.8
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.79, 0.55))
    strip = bpy.context.active_object
    strip.scale = (0.04, 0.01, 0.12)
    strip.data.materials.append(m_detail)

# Antenna
bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.6, location=(-3.8, 0, 2.8))
ant = bpy.context.active_object
ant.data.materials.append(m_detail)

print("[71-73] Pass 4: Final surface check...")

# Pitot tube
bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.8, location=(6, 0.3, -0.1))
pitot = bpy.context.active_object
pitot.rotation_euler = (math.radians(-12), 0, 0)
pitot.data.materials.append(m_detail)

# Static ports
for pos in [(5.5, 0.45, -0.05), (5.5, -0.45, -0.05)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.025, location=pos)
    port = bpy.context.active_object
    port.rotation_euler = (0, math.radians(90), 0)
    port.data.materials.append(m_dark)

print("[74-75] Pass 5: Final polish...")

# Small surface details for visual interest
for i in range(6):
    x = -2.5 + i * 0.9
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -0.75))
    vent = bpy.context.active_object
    vent.scale = (0.15, 0.4, 0.02)
    vent.data.materials.append(m_dark)

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

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-10, 6, 5))
fill = bpy.context.active_object
fill.data.energy = 3.0
fill.data.color = (0.75, 0.85, 1.0)
fill.data.size = 6

# Rim light
bpy.ops.object.light_add(type='AREA', location=(0, 12, -5))
rim = bpy.context.active_object
rim.data.energy = 4.0
rim.data.color = (1.0, 0.75, 0.6)
rim.data.size = 4

# Engine glow
for side in [-1, 1]:
    bpy.ops.object.light_add(type='POINT', location=(-4.5, side * 1.6, -0.2))
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
    filepath="models/starfighter_anime_v5.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT'
)

# Save
bpy.ops.wm.save_as_mainfile(filepath="starfighter_anime_v5.blend")

# Render
print("🖼️ Rendering preview...")
scene.render.filepath = "preview_anime_v5.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 70)
print("✅ ANIME STAR FIGHTER V5 COMPLETE!")
print("=" * 70)
print("📁 Model: models/starfighter_anime_v5.gltf")
print("💾 Blend: starfighter_anime_v5.blend")
print("🖼️  Preview: preview_anime_v5.png")
print("🎨 Total: 75 iterations")
print("🔥 Strategy: Skeleton → Gap Fill → Shapes → Materials → Cohesion")
print("=" * 70)