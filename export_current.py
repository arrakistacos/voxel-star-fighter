import bpy
import os

print("Exporting current scene...")

os.makedirs("models", exist_ok=True)

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

export_path = "/home/freeman/.openclaw/workspace/voxel-star-fighter/models/starfighter_anime_v2.gltf"
print(f"Exporting to: {export_path}")

bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False
)

# Save blend
print("Saving blend file...")
bpy.ops.wm.save_as_mainfile(filepath="/home/freeman/.openclaw/workspace/voxel-star-fighter/starfighter_anime_v2.blend")

# Render
print("Rendering preview...")
scene = bpy.context.scene
scene.render.filepath = "/home/freeman/.openclaw/workspace/voxel-star-fighter/preview_anime_v2.png"
bpy.ops.render.render(write_still=True)

print("✅ Export complete!")