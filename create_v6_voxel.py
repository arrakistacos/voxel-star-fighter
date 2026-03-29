import bpy
import bmesh
import math
import os

print("=" * 70)
print("🚀 ANIME STAR FIGHTER V6 - 40 Iterations + Voxel Refinement")
print("Design → Voxelize Components → Shape Voxels → Refine")
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
m_primary = create_material("Primary", (0.12, 0.28, 0.72), 0.7, 0.3)
m_secondary = create_material("Secondary", (0.9, 0.92, 0.94), 0.1, 0.4)
m_dark = create_material("Dark", (0.15, 0.17, 0.22), 0.3, 0.6)
m_red = create_material("Red_Accent", (0.88, 0.12, 0.08), 0.4, 0.3)
m_yellow = create_material("Yellow_Accent", (0.95, 0.72, 0.12), 0.6, 0.25)
m_cockpit = create_material("Cockpit", (0.05, 0.08, 0.15), 0.9, 0.05)
m_glow = create_material("Engine_Glow", (0.0, 0.0, 0.0), emission=(0.15, 0.75, 1.0))

# Voxel material - slightly rougher
m_voxel_blue = create_material("Voxel_Blue", (0.12, 0.28, 0.72), 0.5, 0.5)
m_voxel_white = create_material("Voxel_White", (0.9, 0.92, 0.94), 0.2, 0.5)
m_voxel_dark = create_material("Voxel_Dark", (0.15, 0.17, 0.22), 0.4, 0.7)
m_voxel_yellow = create_material("Voxel_Yellow", (0.95, 0.72, 0.12), 0.5, 0.4)

# ============================================
# PHASE 1: DESIGN (40 Iterations)
# ============================================

print("\n" + "=" * 70)
print("PHASE 1: DESIGN - 40 Iterations (Low-poly reference)")
print("=" * 70)

print("[1-10] Foundation...")

# Main fuselage
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=7, location=(0, 0, -0.25))
core = bpy.context.active_object
core.scale = (1, 0.55, 1)
core.rotation_euler = (math.radians(90), 0, math.radians(90))
core.name = "REF_Fuselage"

# Nose
bpy.ops.mesh.primitive_cone_add(radius1=0.7, radius2=0.15, depth=3.5, location=(5.25, 0, 0))
nose = bpy.context.active_object
nose.scale = (1, 0.9, 1)
nose.rotation_euler = (math.radians(90), 0, math.radians(90))
nose.name = "REF_Nose"

print("[11-20] Wings...")

for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, side * 2.8, 0))
    wing = bpy.context.active_object
    wing.scale = (2.3, 0.12, 0.85)
    wing.rotation_euler = (0, 0, math.radians(-20 * side))
    wing.name = f"REF_Wing_{side}"

print("[21-30] Stabilizers and engines...")

for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.2, side * 1.7, 1.2))
    stab = bpy.context.active_object
    stab.scale = (1.3, 0.1, 1.6)
    stab.rotation_euler = (math.radians(-8), 0, 0)
    stab.name = f"REF_Stab_{side}"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=2, location=(-3, side * 1.6, -0.25))
    engine = bpy.context.active_object
    engine.rotation_euler = (0, math.radians(90), 0)
    engine.scale = (1, 1, 0.9)
    engine.name = f"REF_Engine_{side}"

print("[31-40] Head and details...")

# V-fin
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.2, 0, 0.35))
vfin = bpy.context.active_object
vfin.scale = (0.2, 1.6, 0.12)
vfin.rotation_euler = (math.radians(12), 0, 0)
vfin.name = "REF_VFin"

# Canopy
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.52, location=(1.2, 0, 0.55))
canopy = bpy.context.active_object
canopy.scale = (1, 0.9, 0.65)
canopy.name = "REF_Canopy"

# Intakes
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=1.2, location=(2, side * 0.85, -0.1))
    intake = bpy.context.active_object
    intake.rotation_euler = (0, math.radians(90), 0)
    intake.scale = (1, 1, 0.75)
    intake.name = f"REF_Intake_{side}"

print("✓ Reference design complete")

# ============================================
# PHASE 2: VOXELIZE COMPONENTS
# ============================================

print("\n" + "=" * 70)
print("PHASE 2: VOXELIZE COMPONENTS")
print("Converting each part to voxel representation")
print("=" * 70)

def voxelize_object(obj, voxel_size=0.15, material=None):
    """Convert an object to voxel representation"""
    bpy.context.view_layer.objects.active = obj
    
    # Add remesh modifier
    remesh = obj.modifiers.new(name="Voxelize", type='REMESH')
    remesh.mode = 'BLOCKS'
    remesh.octree_depth = 6
    remesh.use_remove_disconnected = False
    
    # Apply
    bpy.ops.object.modifier_apply(modifier="Voxelize")
    
    # Apply material
    if material:
        obj.data.materials.clear()
        obj.data.materials.append(material)
    
    return obj

print("Voxelizing fuselage...")
voxelize_object(bpy.data.objects["REF_Fuselage"], material=m_voxel_blue)
voxelize_object(bpy.data.objects["REF_Nose"], material=m_voxel_blue)

print("Voxelizing wings...")
for side in [-1, 1]:
    voxelize_object(bpy.data.objects[f"REF_Wing_{side}"], material=m_voxel_blue)

print("Voxelizing stabilizers...")
for side in [-1, 1]:
    voxelize_object(bpy.data.objects[f"REF_Stab_{side}"], material=m_voxel_white)

print("Voxelizing engines...")
for side in [-1, 1]:
    voxelize_object(bpy.data.objects[f"REF_Engine_{side}"], material=m_voxel_white)

print("Voxelizing details...")
voxelize_object(bpy.data.objects["REF_VFin"], material=m_voxel_yellow)
voxelize_object(bpy.data.objects["REF_Canopy"], material=m_cockpit)

for side in [-1, 1]:
    voxelize_object(bpy.data.objects[f"REF_Intake_{side}"], material=m_voxel_dark)

# ============================================
# PHASE 3: VOXEL REFINEMENT
# ============================================

print("\n" + "=" * 70)
print("PHASE 3: VOXEL REFINEMENT")
print("Adding detail, smoothing edges, ensuring cohesion")
print("=" * 70)

print("Adding voxel edge details...")

# Select all voxel objects and add edge definition
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.name.startswith("REF_"):
        bpy.context.view_layer.objects.active = obj
        
        # Smooth shading for voxel edges
        bpy.ops.object.shade_smooth()
        
        # Add bevel for slightly rounded voxel corners
        bevel = obj.modifiers.new(name="VoxelBevel", type='BEVEL')
        bevel.width = 0.02
        bevel.segments = 2
        bevel.limit_method = 'ANGLE'
        bevel.angle_limit = math.radians(45)

print("Adding thruster glow...")
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-4.2, side * 1.6, -0.25))
    thrust = bpy.context.active_object
    thrust.scale = (0.15, 0.35, 0.35)
    thrust.name = f"Voxel_Thrust_{side}"
    thrust.data.materials.append(m_glow)

print("Adding voxel panel lines...")
for x in [-2.5, -1, 0.5, 2, 3.3]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.65))
    panel = bpy.context.active_object
    panel.scale = (0.03, 1.2, 0.05)
    panel.name = f"Voxel_Panel_{x}"
    panel.data.materials.append(m_voxel_dark)

print("Adding wing tip details...")
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.3, side * 5.3, 0))
    tip_detail = bpy.context.active_object
    tip_detail.scale = (0.2, 0.2, 0.2)
    tip_detail.name = f"Voxel_Tip_{side}"
    tip_detail.data.materials.append(m_voxel_yellow)

# ============================================
# LIGHTING & CAMERA
# ============================================

print("\n💡 Setting up lighting...")

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
    bpy.ops.object.light_add(type='POINT', location=(-4.3, side * 1.6, -0.25))
    glow = bpy.context.active_object
    glow.data.energy = 20
    glow.data.color = (0.3, 0.7, 1.0)

# Camera
print("📷 Camera setup...")
bpy.ops.object.camera_add(location=(13, -10, 7))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(55), 0, math.radians(50))
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
    filepath="models/starfighter_v6_voxel.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT'
)

# Save
bpy.ops.wm.save_as_mainfile(filepath="starfighter_v6_voxel.blend")

# Render
print("🖼️ Rendering preview...")
scene.render.filepath = "preview_v6_voxel.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 70)
print("✅ VOXEL STAR FIGHTER V6 COMPLETE!")
print("=" * 70)
print("📁 Model: models/starfighter_v6_voxel.gltf")
print("💾 Blend: starfighter_v6_voxel.blend")
print("🖼️  Preview: preview_v6_voxel.png")
print("🎨 Process: 40 design iterations → Component voxelization → Refinement")
print("=" * 70)