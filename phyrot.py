
import bpy
import os
from mathutils import Vector

# Get the cube object
cube_obj = bpy.data.objects['Cube']

# Select the object
bpy.ops.object.select_all(action='DESELECT')
cube_obj.select_set(True)

# Remove the object
bpy.ops.object.delete(use_global=False)

# Load the .obj file
filepath = "/Users/shubham/Downloads/reconstruction-dan-001/frame0001/mesh/mesh_000000481.obj"
bpy.ops.import_scene.obj(filepath=filepath)

# Get the imported mesh object
cloth_obj = bpy.data.objects["mesh_000000481"]
bpy.ops.object.select_all(action='DESELECT')
cloth_obj.select_set(True)
bpy.context.view_layer.objects.active = cloth_obj

# Add a cloth simulation to the object
bpy.ops.object.modifier_add(type='CLOTH')
cloth_mod = cloth_obj.modifiers[-1]

cloth_mesh = cloth_obj.data

# Create a new vertex group
group_name = "Group"
group = cloth_obj.vertex_groups.new(name=group_name)

# Add all vertices to the group
for i, v in enumerate(cloth_mesh.vertices):
    group.add([i], 1.0, 'REPLACE')

# print(type(group))
cloth_mod.settings.quality = 5  # Set the cloth quality (higher values are more accurate but slower)
cloth_mod.settings.time_scale = 0.5  # Set the time scale of the simulation
cloth_mod.settings.use_gravity = False

# Add a hook modifier to suspend the object
hook_obj = bpy.data.objects.new('Hook', None)
bpy.context.scene.collection.objects.link(hook_obj)
hook_mod = cloth_obj.modifiers.new(name='Hook', type='HOOK')
# Get the indices of vertices in the group
# Get the vertex indices in the group
group_indices = []
for i, v in enumerate(cloth_mesh.vertices):
    weight = group.weight(v.index)
    if weight != -1 and weight > 0.0:
        group_indices.append(v.index)
hook_mod.vertex_indices_set(group_indices)
hook_mod.object = hook_obj

# Create a keyframe animation of the object's rotation
num_frames = 100  # Set the number of frames in the animation
for i in range(num_frames):
    frame = i + 1
    angle = i * 2 * 3.14159 / num_frames  # Calculate the rotation angle for this frame
    cloth_obj.rotation_euler.z = angle  # Set the object's rotation for this frame
    cloth_obj.keyframe_insert(data_path="rotation_euler", frame=frame)  # Insert a keyframe for this frame
    # bpy.context.scene.camera.location = cloth_obj.matrix_world @ Vector((0, 0, 3))  # Set the camera position

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 100
bpy.ops.ptcache.bake_all(bake=True)

# Set up the output folder for the baked frames
output_folder = "output/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path = os.path.join(output_folder, 'animation_spin.mp4')

# Set render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.filepath = output_path
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.codec = 'H264'
bpy.context.scene.render.fps = 24
bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480

# Render animation
bpy.ops.render.render(animation=True)
print("Done!")
