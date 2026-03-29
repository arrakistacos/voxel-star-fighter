import bpy
import bmesh
import math
import os

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Enable required addons
bpy.ops.preferences.addon_enable(module="io_scene_gltf2")

print("=" * 60)
print("🎨 LOW-POLY ANIME STAR FIGHTER - 10 ITERATIONS")
print("=" * 60)

# ============================================
# ITERATION 1: Base Setup & Reference Planes
# ============================================
print("\n[1/10] Setting up base scene with anime-style lighting...")

# Set up anime-style lighting (3-point + toon rim)
bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
key_light = bpy.context.active_object
key_light.data.energy = 4.0
key_light.data.color = (1.0, 0.98, 0.95)
key_light.rotation_euler = (math.radians(60), 0, math.radians(-45))

bpy.ops.object.light_add(type='AREA', location=(-5, 3, 3))
fill_light = bpy.context.active_object
fill_light.data.energy = 2.0
fill_light.data.color = (0.9, 0.95, 1.0)
fill_light.data.size = 4

bpy.ops.object.light_add(type='AREA', location=(0, 5, -2))
rim_light = bpy.context.active_object
rim_light.data.energy = 3.0
rim_light.data.color = (1.0, 0.9, 0.8)  # Warm rim for anime style
rim_light.data.size = 3

# World lighting for anime sky gradient
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.4, 0.6, 0.9, 1.0)  # Soft anime sky
bg.inputs['Strength'].default_value = 0.5

# ============================================
# ITERATION 2: Material Library (Anime Shaders)
# ============================================
print("[2/10] Creating anime-style materials with toon shaders...")

def create_anime_material(name, base_color, highlight=(1.0, 1.0, 1.0), shadow_mult=0.6):
    """Create a toon/anime style material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # Clear default nodes
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Diffuse BSDF (base)
    diffuse = nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.location = (0, 0)
    diffuse.inputs['Color'].default_value = base_color
    diffuse.inputs['Roughness'].default_value = 0.8
    
    # ColorRamp for toon shading
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-200, 0)
    color_ramp.color_ramp.interpolation = 'CONSTANT'
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (base_color[0] * shadow_mult, 
                                                  base_color[1] * shadow_mult, 
                                                  base_color[2] * shadow_mult, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.5
    color_ramp.color_ramp.elements[1].color = base_color
    
    # Add highlight color
    highlight_elem = color_ramp.color_ramp.elements.new(0.8)
    highlight_elem.color = (min(base_color[0] + 0.3, 1.0),
                            min(base_color[1] + 0.3, 1.0),
                            min(base_color[2] + 0.3, 1.0), 1.0)
    
    # Geometry node for facing ratio
    geometry = nodes.new('ShaderNodeNewGeometry')
    geometry.location = (-600, 0)
    
    # Dot product for lighting calculation
    vec_math = nodes.new('ShaderNodeVectorMath')
    vec_math.location = (-400, 0)
    vec_math.operation = 'DOT_PRODUCT'
    
    links.new(geometry.outputs['Normal'], vec_math.inputs[0])
    # Connect to color ramp and then to output
    links.new(vec_math.outputs[0], color_ramp.inputs['Fac'])
    
    # Principled BSDF for main output
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = base_color
    principled.inputs['Roughness'].default_value = 0.4
    principled.inputs['Metallic'].default_value = 0.0
    
    # Mix with toon
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (200, 0)
    mix.inputs['Fac'].default_value = 0.7
    
    links.new(color_ramp.outputs['Color'], mix.inputs[1])
    links.new(principled.outputs['BSDF'], mix.inputs[2])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])
    
    return mat

# Anime color palette
body_primary = create_anime_material("Body_Primary", (0.15, 0.35, 0.65, 1.0))  # Classic mecha blue
body_secondary = create_anime_material("Body_Secondary", (0.9, 0.9, 0.95, 1.0))  # White/gray
accent_red = create_anime_material("Accent_Red", (0.9, 0.2, 0.15, 1.0))  # Gundam red
accent_yellow = create_anime_material("Accent_Yellow", (1.0, 0.8, 0.1, 1.0))  # V-fin yellow
cockpit = create_anime_material("Cockpit", (0.05, 0.1, 0.2, 1.0), shadow_mult=0.3)  # Dark glass
thruster = create_anime_material("Thruster", (0.2, 0.8, 1.0, 1.0))  # Cyan glow
metal = create_anime_material("Metal", (0.4, 0.45, 0.5, 1.0))  # Gunmetal

# ============================================
# ITERATION 3: Main Fuselage (Streamlined)
# ============================================
print("[3/10] Creating streamlined anime fuselage...")

# Main body - using curves for smooth anime lines
bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=8, location=(0, 0, 0))
fuselage = bpy.context.active_object
fuselage.scale = (1, 0.6, 1)  # Flatten slightly
fuselage.rotation_euler = (math.radians(90), 0, math.radians(90))
fuselage.data.materials.append(body_primary)

# Smooth shading for anime look
bpy.ops.object.shade_smooth()

# Add edge split for crisp anime edges
edge_split = fuselage.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
edge_split.split_angle = math.radians(45)

# ============================================
# ITERATION 4: Nose Section (Pointed anime style)
# ============================================
print("[4/10] Building pointed anime nose cone...")

bpy.ops.mesh.primitive_cone_add(radius1=0.8, radius2=0.1, depth=4, location=(6, 0, 0))
nose = bpy.context.active_object
nose.scale = (1, 0.6, 1)
nose.rotation_euler = (math.radians(90), 0, math.radians(90))
nose.data.materials.append(body_primary)
bpy.ops.object.shade_smooth()

# V-fin (Gundam style nose detail)
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.5, 0, 0.3))
vfin = bpy.context.active_object
vfin.scale = (0.1, 1.2, 0.8)
vfin.rotation_euler = (0, math.radians(-15), 0)
vfin.data.materials.append(accent_yellow)

# ============================================
# ITERATION 5: Cockpit (Bubble canopy style)
# ============================================
print("[5/10] Creating bubble canopy cockpit...")

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.65, location=(1, 0, 0.4))
cockpit_glass = bpy.context.active_object
cockpit_glass.scale = (0.8, 1, 0.5)
cockpit_glass.data.materials.append(cockpit)
bpy.ops.object.shade_smooth()

# Cockpit frame
bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.05, location=(1, 0, 0.4))
frame = bpy.context.active_object
frame.scale = (0.8, 1, 0.5)
frame.data.materials.append(body_secondary)

# ============================================
# ITERATION 6: Wings (Angular anime style)
# ============================================
print("[6/10] Building angular swept wings...")

# Left wing using poly shape for sharp anime edges
left_wing_verts = [(2, -3, 0), (-2, -6, 0), (-2, -6, -0.3), (1, -2.5, -0.2)]
faces = [(0, 1, 2, 3)]

mesh = bpy.data.meshes.new(name="LeftWing")
left_wing = bpy.data.objects.new("LeftWing", mesh)
bpy.context.collection.objects.link(left_wing)

bm = bmesh.new()
for v in left_wing_verts:
    bm.verts.new(v)
bm.verts.ensure_lookup_table()

for f in faces:
    bm.faces.new([bm.verts[i] for i in f])

bm.to_mesh(mesh)
bm.free()

left_wing.data.materials.append(body_primary)
left_wing.data.update()

# Add thickness
solidify = left_wing.modifiers.new(name="Solidify", type='SOLIDIFY')
solidify.thickness = 0.15

# Mirror for right wing
bpy.ops.object.select_all(action='DESELECT')
left_wing.select_set(True)
bpy.context.view_layer.objects.active = left_wing
bpy.ops.object.modifier_add(type='MIRROR')
mirror = left_wing.modifiers["Mirror"]
mirror.use_axis[0] = False
mirror.use_axis[1] = True
mirror.use_axis[2] = False

# Wing details - panel lines
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, -3, 0.1))
wing_detail = bpy.context.active_object
wing_detail.scale = (2, 0.05, 0.02)
wing_detail.data.materials.append(accent_red)

# ============================================
# ITERATION 7: Vertical Stabilizers (Tail fins)
# ============================================
print("[7/10] Adding anime-style stabilizers...")

# Main vertical stabilizer
stab_verts = [(-2, -1, 0), (-2.5, -3, 0), (-2.5, -3, 2), (-2, -1, 2.5)]
faces = [(0, 1, 2, 3)]

for side in [-1, 1]:
    mesh = bpy.data.meshes.new(name=f"Stab_{side}")
    stab = bpy.data.objects.new(f"Stab_{side}", mesh)
    bpy.context.collection.objects.link(stab)
    
    bm = bmesh.new()
    for v in stab_verts:
        bm.verts.new((v[0], v[1] * side, v[2]))
    bm.verts.ensure_lookup_table()
    bm.faces.new([bm.verts[i] for i in faces[0]])
    bm.to_mesh(mesh)
    bm.free()
    
    stab.data.materials.append(body_secondary)
    
    solidify = stab.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.1

# ============================================
# ITERATION 8: Engine Thrusters (Dual exhaust)
# ============================================
print("[8/10] Creating dual thruster engines...")

for side in [-1, 1]:
    # Engine housing
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1.5, location=(-3, side * 1.5, 0))
    housing = bpy.context.active_object
    housing.rotation_euler = (0, math.radians(90), 0)
    housing.data.materials.append(body_secondary)
    
    # Engine nozzle
    bpy.ops.mesh.primitive_cone_add(radius1=0.4, radius2=0.6, depth=0.5, location=(-3.8, side * 1.5, 0))
    nozzle = bpy.context.active_object
    nozzle.rotation_euler = (0, math.radians(-90), 0)
    nozzle.data.materials.append(metal)
    
    # Inner glow
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.1, location=(-3.9, side * 1.5, 0))
    glow = bpy.context.active_object
    glow.rotation_euler = (0, math.radians(90), 0)
    glow.data.materials.append(thruster)
    
    # Engine detail rings
    for i in range(3):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.5, minor_radius=0.03, 
                                         location=(-2.8 + i * 0.3, side * 1.5, 0))
        ring = bpy.context.active_object
        ring.rotation_euler = (0, math.radians(90), 0)
        ring.data.materials.append(metal)

# ============================================
# ITERATION 9: Weapon Systems & Details
# ============================================
print("[9/10] Adding weapons and panel details...")

# Wing-mounted cannons
for side in [-1, 1]:
    # Barrel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, location=(0, side * 4.5, -0.2))
    barrel = bpy.context.active_object
    barrel.rotation_euler = (0, math.radians(90), 0)
    barrel.data.materials.append(metal)
    
    # Energy emitter tip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.3, location=(1, side * 4.5, -0.2))
    emitter = bpy.context.active_object
    emitter.rotation_euler = (0, math.radians(90), 0)
    emitter.data.materials.append(thruster)

# Panel lines and vents
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1 + i * 1.5, 0, 0.55))
    panel = bpy.context.active_object
    panel.scale = (0.8, 0.3, 0.02)
    panel.data.materials.append(body_secondary)

# Intake vents
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1, side * 0.7, -0.2))
    vent = bpy.context.active_object
    vent.scale = (1.5, 0.3, 0.1)
    vent.data.materials.append(metal)

# ============================================
# ITERATION 10: Final Touches & Camera
# ============================================
print("[10/10] Final touches and camera setup...")

# Add some "greebles" (anime panel details)
for i in range(8):
    x = -2 + i * 0.8
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, 0.35, 0.3))
    greeble = bpy.context.active_object
    greeble.scale = (0.3, 0.05, 0.05)
    greeble.data.materials.append(accent_red if i % 2 == 0 else accent_yellow)

# Sensor array on top
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.5, location=(-1, 0, 0.8))
sensor = bpy.context.active_object
sensor.data.materials.append(accent_red)

# Antenna
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=1.5, location=(-2, 0, 0.9))
antenna = bpy.context.active_object
antenna.data.materials.append(metal)
bpy.ops.mesh.primitive_cone_add(radius1=0.08, radius2=0, depth=0.2, location=(-2, 0, 1.7))
antenna_tip = bpy.context.active_object
antenna_tip.data.materials.append(accent_red)

# Camera setup for hero shot
bpy.ops.object.camera_add(location=(12, -8, 6))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(55))
camera.data.lens = 50  # Longer lens for anime proportions
bpy.context.scene.camera = camera

# Render settings - anime style
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = True
scene.cycles.samples = 256

# World shader for anime sky
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0

# Export for web
print("\n📦 Exporting glTF for Three.js viewer...")
export_path = "/home/freeman/.openclaw/workspace/voxel-star-fighter/models/starfighter_anime.gltf"
os.makedirs(os.path.dirname(export_path), exist_ok=True)

# Select all objects for export
bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False
)

# Save blend
print("💾 Saving blend file...")
bpy.ops.wm.save_as_mainfile(filepath="/home/freeman/.openclaw/workspace/voxel-star-fighter/starfighter_anime.blend")

# Render preview
print("🖼️ Rendering preview...")
scene.render.filepath = "/home/freeman/.openclaw/workspace/voxel-star-fighter/preview_anime.png"
bpy.ops.render.render(write_still=True)

print("\n" + "=" * 60)
print("✅ ANIME STAR FIGHTER COMPLETE!")
print("=" * 60)
print(f"📁 Model: {export_path}")
print(f"💾 Blend: starfighter_anime.blend")
print(f"🖼️  Preview: preview_anime.png")
print(f"🎨 Style: Low-poly anime with toon materials")
print("=" * 60)