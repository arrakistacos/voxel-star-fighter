import bpy
import bmesh
import math
import os

print("=" * 70)
print("🚀 ANIME STAR FIGHTER - 50 ADDITIONAL ITERATIONS (V3)")
print("Focus: Weapons • Weathering • Interior • Mechanicals • Detail")
print("=" * 70)

# Clear and start fresh with V2 as reference
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ============================================
# MATERIAL SETUP (All materials defined here)
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

# Core materials
m_body = create_material("Body_Primary", (0.08, 0.22, 0.65), 0.7, 0.3)
m_secondary = create_material("Body_Secondary", (0.92, 0.93, 0.95), 0.1, 0.4)
m_red = create_material("Accent_Red", (0.92, 0.15, 0.12), 0.4, 0.3)
m_yellow = create_material("Accent_Yellow", (1.0, 0.75, 0.15), 0.6, 0.25)
m_dark = create_material("Dark_Panel", (0.12, 0.14, 0.18), 0.3, 0.6)
m_cockpit = create_material("Cockpit", (0.02, 0.05, 0.12), 0.9, 0.05)
m_glow = create_material("Engine_Glow", (0.0, 0.0, 0.0), emission=(0.2, 0.8, 1.0))
m_gunmetal = create_material("Gunmetal", (0.25, 0.27, 0.3), 0.8, 0.35)
m_hydraulic = create_material("Hydraulic", (0.7, 0.65, 0.6), 0.8, 0.3)
m_cable = create_material("Cable", (0.2, 0.15, 0.1), 0.0, 0.9)
m_burnt = create_material("Burnt", (0.08, 0.1, 0.12), 0.6, 0.8)
m_chipped = create_material("Chipped", (0.1, 0.3, 0.5), 0.4, 0.7)

print("\n📦 Creating Anime Star Fighter V3 from scratch...")
print("Building 90 total iterations worth of detail...")

# ============================================
# CORE STRUCTURE (Iterations 1-40 consolidated)
# ============================================

print("[1-40] Building core structure...")

# Main fuselage - split design
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=7, location=(0, 0, -0.3))
core = bpy.context.active_object
core.scale = (1, 0.5, 1)
core.rotation_euler = (math.radians(90), 0, math.radians(90))
core.data.materials.append(m_body)

# Upper fuselage
bpy.ops.mesh.primitive_cylinder_add(radius=0.65, depth=6.5, location=(0, 0, 0.4))
upper = bpy.context.active_object
upper.scale = (1, 0.55, 1)
upper.rotation_euler = (math.radians(90), 0, math.radians(90))
upper.data.materials.append(m_body)

# Spine
bpy.ops.mesh.primitive_cube_add(size=1, location=(-1, 0, 0))
spine = bpy.context.active_object
spine.scale = (4, 0.3, 0.6)
spine.data.materials.append(m_dark)

# Nose
bpy.ops.mesh.primitive_cone_add(radius1=0.65, radius2=0.15, depth=3.5, location=(5.25, 0, 0))
nose = bpy.context.active_object
nose.scale = (1, 0.8, 1)
nose.rotation_euler = (math.radians(90), 0, math.radians(90))
nose.data.materials.append(m_body)

# V-fin
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.2, 0, 0.4))
vfin = bpy.context.active_object
vfin.scale = (0.2, 1.8, 0.15)
vfin.rotation_euler = (math.radians(15), 0, 0)
vfin.data.materials.append(m_yellow)

# Intakes
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=1.5, location=(2, side * 0.9, -0.2))
    intake = bpy.context.active_object
    intake.rotation_euler = (0, math.radians(90), 0)
    intake.scale = (1, 1, 0.6)
    intake.data.materials.append(m_dark)
    
    bpy.ops.mesh.primitive_torus_add(major_radius=0.36, minor_radius=0.04, location=(2.7, side * 0.9, -0.2))
    rim = bpy.context.active_object
    rim.rotation_euler = (0, math.radians(90), 0)
    rim.data.materials.append(m_red)

# Forward swept wings
for side in [-1, 1]:
    # Wing using cube positioned and rotated
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, side * 3, 0))
    wing = bpy.context.active_object
    wing.scale = (2.5, 0.1, 0.8)
    wing.rotation_euler = (0, 0, math.radians(-25 * side))
    wing.data.materials.append(m_body)
    
    # Wing tip pod
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.8, location=(-1.5, side * 5, 0))
    tip = bpy.context.active_object
    tip.rotation_euler = (math.radians(90), 0, math.radians(-20 * side))
    tip.data.materials.append(m_yellow)
    
    # Stabilizer
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.5, side * 1.8, 1))
    stab = bpy.context.active_object
    stab.scale = (1.2, 0.08, 1.5)
    stab.rotation_euler = (math.radians(-10), 0, 0)
    stab.data.materials.append(m_secondary)
    
    # Engine
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=2.2, location=(-3.2, side * 1.5, -0.3))
    engine = bpy.context.active_object
    engine.rotation_euler = (0, math.radians(90), 0)
    engine.scale = (1, 1, 0.8)
    engine.data.materials.append(m_secondary)
    
    bpy.ops.mesh.primitive_torus_add(major_radius=0.56, minor_radius=0.06, location=(-2.1, side * 1.5, -0.3))
    lip = bpy.context.active_object
    lip.rotation_euler = (0, math.radians(90), 0)
    lip.data.materials.append(m_yellow)
    
    # Thruster
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.1, location=(-4.6, side * 1.5, -0.3))
    thrust = bpy.context.active_object
    thrust.rotation_euler = (0, math.radians(90), 0)
    thrust.data.materials.append(m_glow)

# Cockpit
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(1.2, 0, 0.6))
canopy = bpy.context.active_object
canopy.scale = (1, 0.9, 0.65)
canopy.data.materials.append(m_cockpit)

# ============================================
# 50 NEW ITERATIONS (V3 Additions)
# ============================================

print("\n" + "=" * 70)
print("PHASE 1: SURFACE DETAIL (41-55)")
print("=" * 70)

# 41-45: Panel details
print("[41-45] Panel fasteners, hatches, labels...")
for i in range(20):
    x = -3 + i * 0.35
    for y in [-0.6, 0, 0.6]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.02, location=(x, y, 0.7))
        bolt = bpy.context.active_object
        bolt.data.materials.append(m_gunmetal)

# Access hatches
for pos in [(-2, 0.5, 0.65), (0, -0.5, 0.65), (2, 0.5, 0.65)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    hatch = bpy.context.active_object
    hatch.scale = (0.4, 0.3, 0.02)
    hatch.data.materials.append(m_dark)

# Maintenance labels
for i in range(8):
    x = -2.5 + i * 0.7
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.72, 0.35))
    label = bpy.context.active_object
    label.scale = (0.15, 0.01, 0.08)
    label.data.materials.append(m_yellow)

print("[46-55] Structural ribs, plating, conduit...")
# Structural ribs
for x in [-2.5, -1.5, -0.5, 0.5, 1.5]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0))
    rib = bpy.context.active_object
    rib.scale = (0.03, 1.4, 0.6)
    rib.data.materials.append(m_secondary)

# Edge guards
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, side * 1.45, 0))
    guard = bpy.context.active_object
    guard.scale = (4, 0.05, 0.1)
    guard.data.materials.append(m_yellow)

print("\n" + "=" * 70)
print("PHASE 2: MECHANICAL SYSTEMS (51-65)")
print("=" * 70)

# 51-55: Hydraulics and lines
print("[51-55] Hydraulic lines, linkages, cables...")
for side in [-1, 1]:
    # Hydraulic lines
    for z in [-0.3, 0, 0.3]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=3, location=(0, side * 0.8, z))
        line = bpy.context.active_object
        line.rotation_euler = (0, math.radians(90), 0)
        line.data.materials.append(m_hydraulic)
    
    # Actuator
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.4, location=(0.3, side * 1.25, 0.15))
    act = bpy.context.active_object
    act.rotation_euler = (math.radians(90), math.radians(75 * side), 0)
    act.data.materials.append(m_hydraulic)
    
    # Control linkage
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, side * 1.3, 0.1))
    link = bpy.context.active_object
    link.scale = (0.15, 0.05, 0.05)
    link.rotation_euler = (0, 0, math.radians(15 * side))
    link.data.materials.append(m_gunmetal)

# Cable runs
for x in [-1, 0, 1]:
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.6, location=(x, side * 0.72, 0.5))
        cable = bpy.context.active_object
        cable.rotation_euler = (math.radians(90), 0, 0)
        cable.data.materials.append(m_cable)

print("[56-65] Cooling, power, service panels...")
# Cooling radiators
for x in [-2.5, 2.5]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -0.6))
    rad = bpy.context.active_object
    rad.scale = (0.8, 0.6, 0.05)
    rad.data.materials.append(m_gunmetal)

# Emergency releases
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.25, location=(1.5, side * 0.8, 0.6))
    handle = bpy.context.active_object
    handle.rotation_euler = (math.radians(90), 0, math.radians(90 * side))
    handle.data.materials.append(m_red)

print("\n" + "=" * 70)
print("PHASE 3: WEAPONS (66-75)")
print("=" * 70)

print("[66-75] Enhanced weapons and targeting...")
for side in [-1, 1]:
    # Pylon
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.2, side * 3.3, -0.2))
    pylon = bpy.context.active_object
    pylon.scale = (0.3, 0.15, 0.5)
    pylon.data.materials.append(m_gunmetal)
    
    # Cannon barrel with shroud
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1, location=(2.2, side * 3.8, -0.3))
    shroud = bpy.context.active_object
    shroud.rotation_euler = (0, math.radians(90), 0)
    shroud.data.materials.append(m_gunmetal)
    
    # Cooling fins
    for i in range(5):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.015, location=(1.8 + i * 0.15, side * 3.8, -0.3))
        fin = bpy.context.active_object
        fin.rotation_euler = (0, math.radians(90), 0)
        fin.data.materials.append(m_burnt)
    
    # Muzzle brake (cylinder instead)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.2, location=(2.8, side * 3.8, -0.3))
    brake = bpy.context.active_object
    brake.rotation_euler = (0, math.radians(90), 0)
    brake.data.materials.append(m_burnt)

# Targeting sensor
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.3, location=(4, 0, -0.2))
target = bpy.context.active_object
target.rotation_euler = (math.radians(90), 0, 0)
target.data.materials.append(m_dark)

# Laser designator
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.2, location=(3.5, 0.15, 0.1))
lasers = bpy.context.active_object
lasers.rotation_euler = (math.radians(90), math.radians(15), 0)
lasers.data.materials.append(m_gunmetal)

print("\n" + "=" * 70)
print("PHASE 4: WEATHERING (76-85)")
print("=" * 70)

print("[76-85] Battle damage and wear...")
# Scorch marks
for pos in [(2, 0.4, 0.4), (-1.5, -0.5, 0.3)]:
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.06, location=pos, subdivisions=2)
    scorch = bpy.context.active_object
    scorch.scale = (1, 1, 0.3)
    scorch.data.materials.append(m_burnt)

# Paint chips
for i in range(15):
    x = -3 + i * 0.4
    y = 0.7 if i % 2 == 0 else -0.7
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.72))
    chip = bpy.context.active_object
    chip.scale = (0.03, 0.01, 0.03)
    chip.rotation_euler = (0, 0, math.radians(30 * i))
    chip.data.materials.append(m_chipped)

# Burnt engine edges
for side in [-1, 1]:
    bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.04, location=(-4.5, side * 1.5, -0.3))
    burnt = bpy.context.active_object
    burnt.rotation_euler = (0, math.radians(90), 0)
    burnt.data.materials.append(m_burnt)

# Repair patches
for pos in [(-1, 0.4, 0.5), (2, -0.4, 0.45)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    patch = bpy.context.active_object
    patch.scale = (0.25, 0.01, 0.2)
    patch.rotation_euler = (0, 0, math.radians(15))
    patch.data.materials.append(m_secondary)

print("\n" + "=" * 70)
print("PHASE 5: COCKPIT INTERIOR (86-90)")
print("=" * 70)

print("[86-90] Cockpit details...")
# HUD projector
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.2, 0, 0.85))
hud = bpy.context.active_object
hud.scale = (0.2, 0.4, 0.05)
hud.data.materials.append(m_dark)

# Control stick
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.25, location=(1.3, 0.15, 0.4))
stick = bpy.context.active_object
stick.rotation_euler = (math.radians(20), 0, 0)
stick.data.materials.append(m_gunmetal)

# Instrument panel
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5, 0, 0.45))
inst = bpy.context.active_object
inst.scale = (0.05, 0.4, 0.15)
inst.rotation_euler = (math.radians(-15), 0, 0)
inst.data.materials.append(m_dark)

print("\n" + "=" * 70)
print("PHASE 6: DECALS & FINAL (91-100)")
print("=" * 70)

print("[91-100] Markings and final touches...")
# Roundels
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.01, location=(0, side * 0.72, 0.3))
    rnd = bpy.context.active_object
    rnd.rotation_euler = (math.radians(90), 0, 0)
    rnd.data.materials.append(m_secondary)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.012, location=(0, side * 0.72, 0.3))
    dot = bpy.context.active_object
    dot.rotation_euler = (math.radians(90), 0, 0)
    dot.data.materials.append(m_red)

# Serial number
for i in range(6):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.7 + i * 0.08, 0, -0.91))
    char = bpy.context.active_object
    char.scale = (0.03, 0.08, 0.01)
    char.data.materials.append(m_yellow if i % 2 == 0 else m_red)

# Pitot tube
bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.6, location=(5.5, 0.2, -0.2))
pitot = bpy.context.active_object
pitot.rotation_euler = (math.radians(-10), 0, 0)
pitot.data.materials.append(m_gunmetal)

# ============================================
# LIGHTING & EXPORT
# ============================================

print("\n💡 Setting up lighting...")
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Key
bpy.ops.object.light_add(type='SUN', location=(10, -12, 15))
key = bpy.context.active_object
key.data.energy = 5.0
key.rotation_euler = (math.radians(55), 0, math.radians(-50))

# Fill
bpy.ops.object.light_add(type='AREA', location=(-10, 6, 5))
fill = bpy.context.active_object
fill.data.energy = 3.0
fill.data.size = 6

# Rim
bpy.ops.object.light_add(type='AREA', location=(0, 12, -5))
rim = bpy.context.active_object
rim.data.energy = 4.0
rim.data.color = (1.0, 0.75, 0.6)

# Engine glow
for side in [-1, 1]:
    bpy.ops.object.light_add(type='POINT', location=(-5, side * 1.5, -0.3))
    glow = bpy.context.active_object
    glow.data.energy = 20
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

# Export
print("\n📦 Exporting...")
os.makedirs("models", exist_ok=True)

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

bpy.ops.export_scene.gltf(
    filepath="models/starfighter_anime_v3.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False
)

# Save
bpy.ops.wm.save_as_mainfile(filepath="starfighter_anime_v3.blend")

# Render
print("🖼️ Rendering...")
scene.render.filepath = "preview_anime_v3.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 70)
print("✅ ANIME STAR FIGHTER V3 COMPLETE!")
print("=" * 70)
print("📁 Model: models/starfighter_anime_v3.gltf")
print("💾 Blend: starfighter_anime_v3.blend")
print("🖼️  Preview: preview_anime_v3.png")
print("🎨 Total: 90 iterations (40 + 50 new)")
print("🔥 Added: Weapons, weathering, cockpit, mechanicals")
print("=" * 70)