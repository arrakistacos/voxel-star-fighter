import bpy
import os

# Export the anime starfighter
export_path = "/home/freeman/.openclaw/workspace/voxel-star-fighter/models/starfighter_anime.gltf"
os.makedirs(os.path.dirname(export_path), exist_ok=True)

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

print("Exporting anime starfighter to glTF...")
bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT',
    export_image_format='PNG',
    export_cameras=False,
    export_lights=False
)

print(f"✅ Exported: {export_path}")