import bpy
import os

# Export the anime starfighter v2
os.makedirs("models", exist_ok=True)

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

print("Exporting anime starfighter v2 to glTF...")
export_path = "models/starfighter_anime_v2.gltf"
bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLTF_SEPARATE',
    use_selection=True,
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False
)

print(f"✅ Exported: {export_path}")

# Save blend
print("💾 Saving blend file...")
bpy.ops.wm.save_as_mainfile(filepath="starfighter_anime_v2.blend")

# Render preview
print("🖼️ Rendering preview...")
scene = bpy.context.scene
scene.render.filepath = "preview_anime_v2.png"
bpy.ops.render.render(write_still=True)

print("✅ Complete!")