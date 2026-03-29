import bpy
import bmesh
import math
import os

print("=" * 70)
print("👻 GENGAR 3D MODEL - 50 Iterations")
print("Ghost/Poison Pokemon with sinister grin and spiky back")
print("=" * 70)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ============================================
# MATERIALS - Gengar's distinct colors
# ============================================

def create_material(name, base_color, metallic=0.0, roughness=0.5, emission=None, alpha=1.0):
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
    if alpha < 1.0:
        mat.blend_method = 'BLEND'
        bsdf.inputs['Alpha'].default_value = alpha
    
    if emission:
        emission_node = nodes.new('ShaderNodeEmission')
        emission_node.location = (0, 200)
        # emission is (r, g, b, strength) - use rgb for color
        emission_color = (emission[0], emission[1], emission[2], 1.0)
        emission_node.inputs['Color'].default_value = emission_color
        emission_node.inputs['Strength'].default_value = emission[3] if len(emission) > 3 else 2.0
        
        mix = nodes.new('ShaderNodeMixShader')
        mix.location = (200, 0)
        mix.inputs['Fac'].default_value = 0.8
        
        links.new(emission_node.outputs['Emission'], mix.inputs[1])
        links.new(bsdf.outputs['BSDF'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])
    else:
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# Gengar palette
m_body = create_material("Gengar_Purple", (0.35, 0.15, 0.45), 0.0, 0.7)  # Dark purple body
m_eyes = create_material("Gengar_Eyes", (0.9, 0.05, 0.05), 0.0, 0.2, emission=(0.9, 0.05, 0.05, 3.0))  # Glowing red eyes
m_tooth = create_material("Gengar_Teeth", (0.98, 0.98, 0.95), 0.0, 0.3)  # White teeth
m_mouth_inside = create_material("Gengar_Mouth", (0.15, 0.05, 0.15), 0.0, 0.9)  # Dark mouth interior

print("\n" + "=" * 70)
print("PHASE 1: FOUNDATION (1-15)")
print("Core body shape and head")
print("=" * 70)

print("[1-5] Main body - Gengar's roundish form")
# Central body: round but slightly flattened
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 1.2))
body = bpy.context.active_object
body.scale = (1.1, 0.95, 1.0)  # Slightly oval
body.name = "Gengar_Body"
body.data.materials.append(m_body)

print("[6-10] Head shape")
# Head is integrated with body but distinct
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.85, location=(0, 0, 2.1))
head = bpy.context.active_object
head.scale = (1.15, 0.9, 0.85)  # Wider than tall
head.name = "Gengar_Head"
head.data.materials.append(m_body)

print("[11-15] Eye bulges")
# Eyes protrude slightly
for side in [-1, 1]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(side * 0.35, 0.3, 2.0))
    eye_bulge = bpy.context.active_object
    eye_bulge.scale = (1, 0.6, 1)
    eye_bulge.name = f"EyeBulge_{side}"
    eye_bulge.data.materials.append(m_body)

print("\n" + "=" * 70)
print("PHASE 2: SPIKES & BACK (16-30)")
print("Gengar's iconic jagged spine")
print("=" * 70)

print("[16-25] Back spikes - the jagged forest")
# Multiple rows of spikes along the back
spike_positions = [
    # Top row
    (0, -0.9, 2.3), (0, -0.95, 1.8), (0, -0.9, 1.3), (0, -0.8, 0.8),
    # Side rows
    (0.5, -0.8, 2.0), (-0.5, -0.8, 2.0),
    (0.6, -0.7, 1.5), (-0.6, -0.7, 1.5),
    (0.5, -0.6, 1.0), (-0.5, -0.6, 1.0),
]

for i, pos in enumerate(spike_positions):
    bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.02, depth=0.5, location=pos)
    spike = bpy.context.active_object
    # Randomize spike orientation slightly
    spike.rotation_euler = (math.radians(-15), math.radians(10 * (i % 3 - 1)), 0)
    spike.name = f"Spike_{i}"
    spike.data.materials.append(m_body)

print("[26-30] Ear spikes")
# Two large spikes on top of head
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cone_add(radius1=0.18, radius2=0.03, depth=0.7, location=(side * 0.5, 0, 2.8))
    ear = bpy.context.active_object
    ear.rotation_euler = (math.radians(20), 0, side * math.radians(15))
    ear.name = f"EarSpike_{side}"
    ear.data.materials.append(m_body)

print("\n" + "=" * 70)
print("PHASE 3: FACE & MOUTH (31-45)")
print("Gengar's sinister grin")
print("=" * 70)

print("[31-35] Wide grin mouth")
# Large mouth spans most of the face
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(0, 0.35, 1.9))
mouth = bpy.context.active_object
mouth.scale = (1.6, 0.4, 0.8)  # Wide and flat
mouth.name = "Gengar_Mouth"
mouth.data.materials.append(m_mouth_inside)

print("[36-40] Eyes - glowing red")
for side in [-1, 1]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(side * 0.35, 0.55, 2.05))
    eye = bpy.context.active_object
    eye.scale = (0.8, 0.4, 1)
    eye.name = f"Eye_{side}"
    eye.data.materials.append(m_eyes)

print("[41-45] Sharp teeth")
# Upper teeth
for i in range(-4, 5):
    x = i * 0.12
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, radius2=0.01, depth=0.15, location=(x, 0.55, 1.95))
    tooth = bpy.context.active_object
    tooth.rotation_euler = (math.radians(90), 0, 0)
    tooth.name = f"Tooth_Upper_{i}"
    tooth.data.materials.append(m_tooth)

# Lower teeth
for i in range(-3, 4):
    x = i * 0.14
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, radius2=0.01, depth=0.12, location=(x, 0.55, 1.85))
    tooth = bpy.context.active_object
    tooth.rotation_euler = (math.radians(-90), 0, 0)
    tooth.name = f"Tooth_Lower_{i}"
    tooth.data.materials.append(m_tooth)

print("\n" + "=" * 70)
print("PHASE 4: ARMS, LEGS & DETAILS (46-50)")
print("Gengar's stubby limbs")
print("=" * 70)

print("[46-48] Short arms with claws")
for side in [-1, 1]:
    # Arm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.6, location=(side * 0.8, 0.3, 1.4))
    arm = bpy.context.active_object
    arm.rotation_euler = (0, 0, side * math.radians(-30))
    arm.name = f"Arm_{side}"
    arm.data.materials.append(m_body)
    
    # Hand/claws
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(side * 1.0, 0.5, 1.2))
    hand = bpy.context.active_object
    hand.scale = (1.2, 0.6, 0.8)
    hand.name = f"Hand_{side}"
    hand.data.materials.append(m_body)
    
    # Claws
    for j in range(3):
        claw_x = side * 1.15 + j * 0.08 * side
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0.01, depth=0.15, location=(claw_x, 0.6, 1.15))
        claw = bpy.context.active_object
        claw.rotation_euler = (math.radians(70), 0, side * math.radians(10))
        claw.name = f"Claw_{side}_{j}"
        claw.data.materials.append(m_tooth)

print("[49-50] Short legs with feet")
for side in [-1, 1]:
    # Leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.5, location=(side * 0.4, 0, 0.6))
    leg = bpy.context.active_object
    leg.rotation_euler = (math.radians(90), 0, side * math.radians(-10))
    leg.name = f"Leg_{side}"
    leg.data.materials.append(m_body)
    
    # Foot
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(side * 0.45, 0.15, 0.35))
    foot = bpy.context.active_object
    foot.scale = (1.3, 1.8, 0.7)
    foot.name = f"Foot_{side}"
    foot.data.materials.append(m_body)
    
    # Toes
    for j in range(3):
        toe_offset = (j - 1) * 0.1
        bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.01, depth=0.1, location=(side * 0.55 + toe_offset * 0.5, 0.35, 0.3))
        toe = bpy.context.active_object
        toe.rotation_euler = (math.radians(80), 0, toe_offset * 0.5)
        toe.name = f"Toe_{side}_{j}"
        toe.data.materials.append(m_tooth)

# ============================================
# LIGHTING & CAMERA - Spooky atmosphere
# ============================================

print("\n💡 Setting up spooky lighting...")

for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Key light - eerie purple
bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
key = bpy.context.active_object
key.data.energy = 4.0
key.data.color = (0.6, 0.4, 0.8)  # Purple tint
key.data.size = 4

# Rim light - ghostly blue
bpy.ops.object.light_add(type='AREA', location=(-5, 5, 3))
rim = bpy.context.active_object
rim.data.energy = 3.0
rim.data.color = (0.4, 0.6, 0.9)  # Ghostly blue
rim.data.size = 5

# Under glow - from below for creepy effect
bpy.ops.object.light_add(type='POINT', location=(0, 0, -2))
under = bpy.context.active_object
under.data.energy = 2.0
under.data.color = (0.5, 0.2, 0.6)

# Eye glow lights
for side in [-1, 1]:
    bpy.ops.object.light_add(type='POINT', location=(side * 0.35, 0.6, 2.05))
    eye_glow = bpy.context.active_object
    eye_glow.data.energy = 8
    eye_glow.data.color = (1.0, 0.1, 0.1)

# Camera
print("📷 Camera setup...")
bpy.ops.object.camera_add(location=(6, -5, 3))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(75), 0, math.radians(50))
cam.data.lens = 45
bpy.context.scene.camera = cam

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.film_transparent = True
scene.cycles.samples = 1024
scene.cycles.use_denoising = True

# World - dark and moody
world = bpy.context.scene.world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.05, 0.08, 0.12, 1.0)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.2

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
    filepath="models/gengar_3d.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT'
)

bpy.ops.wm.save_as_mainfile(filepath="gengar_3d.blend")

print("🖼️ Rendering preview...")
scene.render.filepath = "preview_gengar.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 70)
print("✅ GENGAR COMPLETE!")
print("=" * 70)
print("📁 Model: models/gengar_3d.gltf")
print("💾 Blend: gengar_3d.blend")
print("🖼️  Preview: preview_gengar.png")
print("👻 Pokemon: Gengar (Ghost/Poison)")
print("=" * 70)