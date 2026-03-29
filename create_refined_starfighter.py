import bpy
import bmesh
import math
import os

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create materials with better properties
def create_material(name, color, metallic=0.3, roughness=0.4, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    if emission:
        # Find emission socket (name varies by Blender version)
        for input_name in bsdf.inputs.keys():
            if 'emission' in input_name.lower():
                if 'color' in input_name.lower() or 'strength' not in input_name.lower():
                    bsdf.inputs[input_name].default_value = emission
                else:
                    bsdf.inputs[input_name].default_value = 2.0
    return mat

# Enhanced materials
body_mat = create_material("Body", (0.25, 0.3, 0.38, 1.0), metallic=0.5, roughness=0.3)
body_detail_mat = create_material("BodyDetail", (0.2, 0.25, 0.32, 1.0), metallic=0.6, roughness=0.25)
engine_mat = create_material("Engine", (0.05, 0.35, 0.95, 1.0), metallic=0.8, roughness=0.2)
engine_glow_mat = create_material("EngineGlow", (0.0, 0.0, 0.0, 1.0), emission=(0.2, 0.6, 1.0, 1.0))
accent_mat = create_material("Accent", (0.95, 0.4, 0.05, 1.0), metallic=0.4, roughness=0.4)
cockpit_mat = create_material("Cockpit", (0.05, 0.08, 0.12, 1.0), metallic=0.9, roughness=0.1)
weapon_mat = create_material("Weapon", (0.6, 0.6, 0.65, 1.0), metallic=0.9, roughness=0.2)

# Voxel creation helper
def create_voxel(x, y, z, material, size=0.48):
    bpy.ops.mesh.primitive_cube_add(size=size, location=(x * 0.5, y * 0.5, z * 0.5))
    obj = bpy.context.active_object
    obj.data.materials.append(material)
    return obj

def create_detail_voxel(x, y, z, material, scale=(0.3, 0.3, 0.3)):
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(x * 0.5, y * 0.5, z * 0.5))
    obj = bpy.context.active_object
    obj.scale = scale
    obj.data.materials.append(material)
    return obj

voxels = []

# ITERATION 1-3: Central Fuselage with more detail
print("Building detailed fuselage...")
for z in range(-6, 9):
    for y in range(-2, 3):
        for x in range(-2, 3):
            # Rounded corners for main body
            if abs(x) == 2 and abs(y) == 2:
                continue
            
            # Material selection based on position
            if z == 5 and abs(x) <= 1 and abs(y) <= 1:
                mat = cockpit_mat
            elif z in [0, -2, 2] and abs(x) == 1:
                mat = body_detail_mat  # Panel lines
            else:
                mat = body_mat
            
            voxels.append(create_voxel(x, y, z, mat))

# ITERATION 4-5: Enhanced nose cone with progressive taper
print("Building advanced nose...")
for z in range(9, 14):
    taper = (z - 8) * 0.3
    for y in range(-2 + int(taper), 3 - int(taper)):
        for x in range(-2 + int(taper), 3 - int(taper)):
            if abs(x) + abs(y) > 3 - taper:
                continue
            if z == 13:  # Tip
                voxels.append(create_voxel(x * 0.5, y * 0.5, z * 0.5, accent_mat, size=0.3))
            else:
                voxels.append(create_voxel(x * 0.5, y * 0.5, z * 0.5, body_mat))

# ITERATION 6: Angled wings with detail
print("Building detailed wings...")
for x_offset in range(-8, -1):
    wing_span = abs(x_offset)
    z_range = range(-wing_span // 3, 5 - wing_span // 4)
    
    for z in z_range:
        # Main wing structure
        voxels.append(create_voxel(x_offset * 0.5, 0, z * 0.5, body_mat))
        voxels.append(create_voxel(x_offset * 0.5, 1, z * 0.5, body_mat))
        voxels.append(create_voxel(x_offset * 0.5, -1, z * 0.5, body_mat))
        
        # Wing edge details
        if z == 0:
            voxels.append(create_voxel(x_offset * 0.5, 0, z * 0.5, accent_mat))

# Mirror wings
for x_offset in range(2, 9):
    wing_span = abs(x_offset)
    z_range = range(-wing_span // 3, 5 - wing_span // 4)
    
    for z in z_range:
        voxels.append(create_voxel(x_offset * 0.5, 0, z * 0.5, body_mat))
        voxels.append(create_voxel(x_offset * 0.5, 1, z * 0.5, body_mat))
        voxels.append(create_voxel(x_offset * 0.5, -1, z * 0.5, body_mat))
        
        if z == 0:
            voxels.append(create_voxel(x_offset * 0.5, 0, z * 0.5, accent_mat))

# ITERATION 7: Wing tips with weapons
print("Adding wing weapons...")
for x_offset in [-9, 9]:
    # Wing tip
    voxels.append(create_voxel(x_offset * 0.5, 0, 0, accent_mat))
    voxels.append(create_voxel(x_offset * 0.5, 0, 1, body_mat))
    
    # Weapon barrels
    for z in range(2, 6):
        voxels.append(create_voxel(x_offset * 0.5, 0.3, z * 0.5, weapon_mat, size=0.25))
        voxels.append(create_voxel(x_offset * 0.5, -0.3, z * 0.5, weapon_mat, size=0.25))

# ITERATION 8: Enhanced engines with glow
print("Building detailed engines...")
for z in range(-9, -5):
    for x_offset in [-3, 3]:
        for y in range(-2, 3):
            if abs(y) == 2 and z == -9:
                continue
            mat = engine_glow_mat if z == -9 and abs(y) < 2 else engine_mat
            voxels.append(create_voxel(x_offset * 0.5, y * 0.5, z * 0.5, mat))

# Engine thruster effects
for x_offset in [-3, 3]:
    # Inner glow
    voxels.append(create_voxel(x_offset * 0.5, 0, -9.5 * 0.5, engine_glow_mat, size=0.35))
    voxels.append(create_voxel(x_offset * 0.5, 0.5, -9.3 * 0.5, engine_glow_mat, size=0.25))
    voxels.append(create_voxel(x_offset * 0.5, -0.5, -9.3 * 0.5, engine_glow_mat, size=0.25))

# ITERATION 9: Vertical stabilizers (tail fins)
print("Adding stabilizers...")
for z in range(-5, -2):
    height = abs(z + 5) * 0.5
    for y in range(2, 2 + int(height) + 1):
        voxels.append(create_voxel(-2.5 * 0.5, y * 0.5, z * 0.5, accent_mat))
        voxels.append(create_voxel(2.5 * 0.5, y * 0.5, z * 0.5, accent_mat))

# ITERATION 10: Surface details - antennas, panels, vents
print("Adding surface details...")
# Rear vent
for x in range(-1, 2):
    voxels.append(create_voxel(x * 0.5, 0, -7 * 0.5, body_detail_mat, size=0.35))

# Top antenna
voxels.append(create_voxel(0, 2.5 * 0.5, 1 * 0.5, accent_mat, size=0.2))
voxels.append(create_voxel(0, 3.5 * 0.5, 1 * 0.5, accent_mat, size=0.15))

# Side thrusters
for x_offset in [-1.5, 1.5]:
    voxels.append(create_voxel(x_offset * 0.5, 1.8 * 0.5, 0, accent_mat, size=0.3))

print(f"Total voxels created: {len(voxels)}")

# Professional lighting setup
print("Setting up professional lighting...")

# Key light
bpy.ops.object.light_add(type='AREA', location=(8, -8, 6))
key_light = bpy.context.active_object
key_light.data.energy = 800
key_light.data.size = 4
key_light.rotation_euler = (math.radians(45), 0, math.radians(-45))

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-6, 4, 3))
fill_light = bpy.context.active_object
fill_light.data.energy = 400
fill_light.data.size = 3
fill_light.data.color = (0.9, 0.95, 1.0)

# Rim light
bpy.ops.object.light_add(type='AREA', location=(0, 8, -4))
rim_light = bpy.context.active_object
rim_light.data.energy = 500
rim_light.data.size = 2
rim_light.data.color = (1.0, 0.9, 0.8)

# Under fill
bpy.ops.object.light_add(type='AREA', location=(0, 0, -6))
under_light = bpy.context.active_object
under_light.data.energy = 200
under_light.data.size = 5
under_light.data.color = (0.8, 0.85, 0.9)

# Camera setup
bpy.ops.object.camera_add(location=(10, -10, 6))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(55), 0, math.radians(45))
camera.data.lens = 35
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 15
bpy.context.scene.camera = camera

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 2048
scene.render.resolution_y = 1152
scene.render.film_transparent = True
scene.cycles.samples = 256
scene.cycles.use_denoising = True

# Join all voxels into one object for easier export
print("Joining voxel objects...")
bpy.ops.object.select_all(action='DESELECT')
for obj in voxels:
    obj.select_set(True)
bpy.context.view_layer.objects.active = voxels[0]
bpy.ops.object.join()

# Rename the joined object
starfighter = bpy.context.active_object
starfighter.name = "VoxelStarFighter"

# Export GLTF for Three.js
print("Exporting GLTF...")
export_path = "/home/freeman/.openclaw/workspace/voxel-star-fighter/starfighter.gltf"
bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLTF_SEPARATE',
    use_selection=False,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False
)

# Save blend file
print("Saving blend file...")
bpy.ops.wm.save_as_mainfile(filepath="/home/freeman/.openclaw/workspace/voxel-star-fighter/voxel_starfighter.blend")

# Render
print("Rendering...")
scene.render.filepath = "/home/freeman/.openclaw/workspace/voxel-star-fighter/voxel_starfighter.png"
bpy.ops.render.render(write_still=True)

print("✅ DONE!")
print(f"📁 GLTF: {export_path}")
print(f"🖼️  PNG: /home/freeman/.openclaw/workspace/voxel-star-fighter/voxel_starfighter.png")
print(f"💾 BLEND: /home/freeman/.openclaw/workspace/voxel-star-fighter/voxel_starfighter.blend")