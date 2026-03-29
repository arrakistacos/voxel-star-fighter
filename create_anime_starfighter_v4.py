import bpy
import bmesh
import math
import os

print("=" * 70)
print("🚀 ANIME STAR FIGHTER V4 - 90 ITERATIONS")
print("Focus: Foundation • Distinctive Shapes • Materials • Cohesiveness")
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
# PHASE 1: FOUNDATION (Iterations 1-22)
# Solid structural base - split fuselage, wings, engines
# ============================================

print("\n" + "=" * 70)
print("PHASE 1: FOUNDATION (1-22)")
print("=" * 70)

print("[1-5] Core fuselage structure...")

# Main core - split lower
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=7, location=(0, 0, -0.3))
core = bpy.context.active_object
core.scale = (1, 0.5, 1)
core.rotation_euler = (math.radians(90), 0, math.radians(90))
core.data.materials.append(m_primary)

# Upper fuselage
bpy.ops.mesh.primitive_cylinder_add(radius=0.65, depth=6.5, location=(0, 0, 0.4))
upper = bpy.context.active_object
upper.scale = (1, 0.55, 1)
upper.rotation_euler = (math.radians(90), 0, math.radians(90))
upper.data.materials.append(m_primary)

# Spine connector
bpy.ops.mesh.primitive_cube_add(size=1, location=(-1, 0, 0))
spine = bpy.context.active_object
spine.scale = (4, 0.3, 0.6)
spine.data.materials.append(m_dark)

# Nose cone
bpy.ops.mesh.primitive_cone_add(radius1=0.65, radius2=0.12, depth=3.5, location=(5.25, 0, 0))
nose = bpy.context.active_object
nose.scale = (1, 0.8, 1)
nose.rotation_euler = (math.radians(90), 0, math.radians(90))
nose.data.materials.append(m_primary)

print("[6-10] Wing structures...")

# Forward swept wings - main
for side in [-1, 1]:
    # Main wing panel
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1, side * 2.8, 0.1))
    wing = bpy.context.active_object
    wing.scale = (2.2, 0.08, 1.2)
    wing.rotation_euler = (0, 0, math.radians(-20 * side))
    wing.data.materials.append(m_primary)
    
    # Wing leading edge
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, side * 3.2, 0.15))
    edge = bpy.context.active_object
    edge.scale = (2.8, 0.06, 0.15)
    edge.rotation_euler = (0, 0, math.radians(-22 * side))
    edge.data.materials.append(m_secondary)
    
    # Wing tip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.9, location=(-1.8, side * 4.8, 0.1))
    tip = bpy.context.active_object
    tip.rotation_euler = (math.radians(90), 0, math.radians(-25 * side))
    tip.data.materials.append(m_yellow)

print("[11-15] Vertical stabilizers...")

for side in [-1, 1]:
    # Main stabilizer
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.2, side * 1.6, 1.2))
    stab = bpy.context.active_object
    stab.scale = (1.5, 0.08, 1.8)
    stab.rotation_euler = (math.radians(-12), 0, 0)
    stab.data.materials.append(m_secondary)
    
    # Stab tip
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.2, side * 1.6, 2.8))
    stab_tip = bpy.context.active_object
    stab_tip.scale = (0.4, 0.06, 0.25)
    stab_tip.data.materials.append(m_red)

print("[16-20] Engine nacelles...")

for side in [-1, 1]:
    # Main engine housing
    bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=2.4, location=(-3, side * 1.5, -0.3))
    engine = bpy.context.active_object
    engine.rotation_euler = (0, math.radians(90), 0)
    engine.scale = (1, 1, 0.85)
    engine.data.materials.append(m_secondary)
    
    # Engine intake lip
    bpy.ops.mesh.primitive_torus_add(major_radius=0.61, minor_radius=0.05, location=(-1.8, side * 1.5, -0.3))
    lip = bpy.context.active_object
    lip.rotation_euler = (0, math.radians(90), 0)
    lip.data.materials.append(m_yellow)
    
    # Thruster
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.15, location=(-4.4, side * 1.5, -0.3))
    thrust = bpy.context.active_object
    thrust.rotation_euler = (0, math.radians(90), 0)
    thrust.data.materials.append(m_glow)
    
    # Nozzle detail ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.03, location=(-4.3, side * 1.5, -0.3))
    ring = bpy.context.active_object
    ring.rotation_euler = (0, math.radians(90), 0)
    ring.data.materials.append(m_dark)

print("[21-22] Intake ducts...")

for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=1.2, location=(2, side * 0.85, -0.15))
    intake = bpy.context.active_object
    intake.rotation_euler = (0, math.radians(90), 0)
    intake.scale = (1, 1, 0.7)
    intake.data.materials.append(m_dark)
    
    # Intake rim
    bpy.ops.mesh.primitive_torus_add(major_radius=0.36, minor_radius=0.04, location=(2.6, side * 0.85, -0.15))
    intake_rim = bpy.context.active_object
    intake_rim.rotation_euler = (0, math.radians(90), 0)
    intake_rim.data.materials.append(m_red)

# ============================================
# PHASE 2: DISTINCTIVE SHAPES (Iterations 23-45)
# V-fin, panel lines, surface details, hardpoints
# ============================================

print("\n" + "=" * 70)
print("PHASE 2: DISTINCTIVE SHAPES (23-45)")
print("=" * 70)

print("[23-28] V-fin and head elements...")

# V-fin - anime mecha signature
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.2, 0, 0.35))
vfin_base = bpy.context.active_object
vfin_base.scale = (0.15, 1.6, 0.12)
vfin_base.rotation_euler = (math.radians(12), 0, 0)
vfin_base.data.materials.append(m_yellow)

# Secondary V-fin angle
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.1, 0, 0.55))
vfin_top = bpy.context.active_object
vfin_top.scale = (0.12, 0.8, 0.1)
vfin_top.rotation_euler = (math.radians(-8), 0, 0)
vfin_top.data.materials.append(m_yellow)

print("[29-35] Panel lines and surface detail...")

# Horizontal panel lines on fuselage
for i, x in enumerate([-2.5, -1.2, 0, 1.2, 2.5, 3.8]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.72))
    panel = bpy.context.active_object
    panel.scale = (0.02, 1.3, 0.01)
    panel.data.materials.append(m_dark)

# Vertical panel lines
for x in [-1.5, 0.5, 2.5]:
    for y in [-0.6, 0, 0.6]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.35))
        vpanel = bpy.context.active_object
        vpanel.scale = (0.01, 0.02, 0.4)
        vpanel.data.materials.append(m_dark)

print("[36-40] Weapon hardpoints...")

for side in [-1, 1]:
    # Pylon
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.2, side * 3.4, -0.3))
    pylon = bpy.context.active_object
    pylon.scale = (0.4, 0.12, 0.6)
    pylon.data.materials.append(m_detail)
    
    # Weapon rail
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.8, side * 3.4, -0.25))
    rail = bpy.context.active_object
    rail.scale = (1.2, 0.06, 0.08)
    rail.rotation_euler = (0, 0, math.radians(5 * side))
    rail.data.materials.append(m_detail)
    
    # Rail mounts
    for x in [1.4, 2.2]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.15, location=(x, side * 3.4, -0.25))
        mount = bpy.context.active_object
        mount.data.materials.append(m_dark)

print("[41-45] Surface features...")

# Raised panel sections
for pos in [(-2, 0.6, 0.5), (0, -0.6, 0.45), (2, 0.6, 0.48)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    panel = bpy.context.active_object
    panel.scale = (0.5, 0.3, 0.02)
    panel.data.materials.append(m_secondary)

# Maintenance hatches
for pos in [(-1.5, -0.5, 0.7), (1.5, 0.5, 0.68)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    hatch = bpy.context.active_object
    hatch.scale = (0.35, 0.25, 0.015)
    hatch.data.materials.append(m_dark)

# ============================================
# PHASE 3: MATERIALS (Iterations 46-68)
# Surface detail, navigation lights, decals
# ============================================

print("\n" + "=" * 70)
print("PHASE 3: MATERIALS (46-68)")
print("=" * 70)

print("[46-52] Fasteners and bolts...")

# Panel fasteners across surfaces
fastener_locs = []
for i in range(8):
    x = -3 + i * 0.8
    for y in [-0.65, 0, 0.65]:
        fastener_locs.append((x, y, 0.73))

for i in range(6):
    x = -2.4 + i * 0.9
    for y in [-0.5, 0.5]:
        fastener_locs.append((x, y, 0.68))

for pos in fastener_locs:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.025, location=pos)
    bolt = bpy.context.active_object
    bolt.data.materials.append(m_detail)

print("[53-58] Navigation and formation lights...")

# Red/green nav lights
for side in [-1, 1]:
    # Wingtip nav light
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.03, location=(-2.2, side * 4.7, 0.1))
    nav = bpy.context.active_object
    nav.rotation_euler = (math.radians(90), 0, 0)
    nav.data.materials.append(m_red if side == 1 else m_detail)

# Formation lights
for x in [-2.8, -1.5, 3]:
    for y in [-0.65, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.72))
        form = bpy.context.active_object
        form.scale = (0.08, 0.03, 0.005)
        form.data.materials.append(m_yellow)

print("[59-65] Decals and markings...")

# Roundels (cylinders on surface)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.01, location=(0, side * 0.72, 0.35))
    rnd = bpy.context.active_object
    rnd.rotation_euler = (math.radians(90), 0, 0)
    rnd.data.materials.append(m_secondary)
    
    # Inner dot
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.012, location=(0, side * 0.72, 0.35))
    dot = bpy.context.active_object
    dot.rotation_euler = (math.radians(90), 0, 0)
    dot.data.materials.append(m_red)

# Stripes
for i in range(4):
    x = -2 + i * 1.5
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -0.91))
    stripe = bpy.context.active_object
    stripe.scale = (0.15, 0.5, 0.01)
    stripe.data.materials.append(m_yellow if i % 2 == 0 else m_red)

print("[66-68] Cockpit and canopy...")

# Canopy
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(1.2, 0, 0.6))
canopy = bpy.context.active_object
canopy.scale = (1, 0.9, 0.65)
canopy.data.materials.append(m_cockpit)

# Canopy frame
bpy.ops.mesh.primitive_torus_add(major_radius=0.56, minor_radius=0.02, location=(1.2, 0, 0.6))
frame = bpy.context.active_object
frame.scale = (1, 0.9, 0.65)
frame.data.materials.append(m_dark)

# ============================================
# PHASE 4: COHESIVENESS (Iterations 69-90)
# Final details, blending, harmony
# ============================================

print("\n" + "=" * 70)
print("PHASE 4: COHESIVENESS (69-90)")
print("=" * 70)

print("[69-75] Surface detail refinement...")

# Edge guards
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, side * 1.48, 0.3))
    guard = bpy.context.active_object
    guard.scale = (4.5, 0.03, 0.08)
    guard.data.materials.append(m_yellow)

# Heat tiles on belly
for x in range(-4, 4):
    for z in [-0.6, -0.3]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x * 0.6, 0, z))
        tile = bpy.context.active_object
        tile.scale = (0.25, 1.35, 0.03)
        tile.data.materials.append(m_dark)

print("[76-82] Mechanical connections...")

# Control surface hinges
for side in [-1, 1]:
    for x in [-0.5, 1.5]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.25, location=(x, side * 2.75, 0.15))
        hinge = bpy.context.active_object
        hinge.rotation_euler = (math.radians(90), 0, 0)
        hinge.data.materials.append(m_detail)

# Aileron lines
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.5, side * 2.8, 0.12))
    aileron = bpy.context.active_object
    aileron.scale = (1.8, 0.02, 0.01)
    aileron.rotation_euler = (0, 0, math.radians(-20 * side))
    aileron.data.materials.append(m_dark)

print("[83-90] Final cohesion details...")

# Pitot tube
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.7, location=(5.8, 0.25, -0.15))
pitot = bpy.context.active_object
pitot.rotation_euler = (math.radians(-15), 0, 0)
pitot.data.materials.append(m_detail)

# Static ports
for pos in [(5.2, 0.4, -0.1), (5.2, -0.4, -0.1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.02, location=pos)
    port = bpy.context.active_object
    port.rotation_euler = (0, math.radians(90), 0)
    port.data.materials.append(m_dark)

# Antenna
bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.5, location=(-3.5, 0, 2.5))
ant = bpy.context.active_object
ant.data.materials.append(m_detail)

# Small details for visual interest
for i in range(12):
    x = -3 + i * 0.5
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.73, 0.4))
    detail = bpy.context.active_object
    detail.scale = (0.02, 0.01, 0.15)
    detail.data.materials.append(m_detail)

# ============================================
# LIGHTING & CAMERA
# ============================================

print("\n💡 Setting up anime lighting...")

# Remove default
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Key light - warm
bpy.ops.object.light_add(type='SUN', location=(10, -12, 15))
key = bpy.context.active_object
key.data.energy = 5.0
key.data.color = (1.0, 0.9, 0.8)
key.rotation_euler = (math.radians(55), 0, math.radians(-50))

# Fill - cool
bpy.ops.object.light_add(type='AREA', location=(-10, 6, 5))
fill = bpy.context.active_object
fill.data.energy = 3.0
fill.data.color = (0.75, 0.85, 1.0)
fill.data.size = 6

# Rim - warm
bpy.ops.object.light_add(type='AREA', location=(0, 12, -5))
rim = bpy.context.active_object
rim.data.energy = 4.0
rim.data.color = (1.0, 0.75, 0.6)
rim.data.size = 4

# Engine glow lights
for side in [-1, 1]:
    bpy.ops.object.light_add(type='POINT', location=(-4.7, side * 1.5, -0.3))
    glow = bpy.context.active_object
    glow.data.energy = 25
    glow.data.color = (0.4, 0.8, 1.0)
    glow.data.shadow_soft_size = 0.5

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

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

bpy.ops.export_scene.gltf(
    filepath="models/starfighter_anime_v4.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT'
)

# Save blend
bpy.ops.wm.save_as_mainfile(filepath="starfighter_anime_v4.blend")

# Render preview
print("🖼️ Rendering preview...")
scene.render.filepath = "preview_anime_v4.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 70)
print("✅ ANIME STAR FIGHTER V4 COMPLETE!")
print("=" * 70)
print("📁 Model: models/starfighter_anime_v4.gltf")
print("💾 Blend: starfighter_anime_v4.blend")
print("🖼️  Preview: preview_anime_v4.png")
print("🎨 Total: 90 iterations (4 phases)")
print("🔥 Focus: Foundation • Shapes • Materials • Cohesiveness")
print("=" * 70)