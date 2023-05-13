
import bpy
import os
from mathutils import Vector

def new_plane(mylocation, mysize, myname):
    bpy.ops.mesh.primitive_plane_add(
        size=mysize,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=mylocation,
        rotation=(0, 0, 0),
        scale=(0, 0, 0))
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname + "_mesh"
    return

new_plane((0,0,-4), 10, "MyFloor")
plane = bpy.data.objects['MyFloor']
# Add a collision modifier to the plane object
bpy.ops.object.modifier_add(type='COLLISION')
collision_mod = plane.modifiers[-1]
collision_mod.name = 'FloorCollision'
# collision_mod.object = plane

# Get the cube object
cube_obj = bpy.data.objects['Cube']

# Select the object
bpy.ops.object.select_all(action='DESELECT')
cube_obj.select_set(True)

# Remove the object
bpy.ops.object.delete(use_global=False)

# Load the .obj file
# filepath = "/Users/shubham/Downloads/reconstruction-dan-001/frame0001/mesh/mesh_000000481.obj"
filepath = "/Users/shubham/Downloads/cleaned0.obj"
bpy.ops.import_scene.obj(filepath=filepath)

# Get the imported mesh object
cloth_obj = bpy.data.objects["cleaned0"]
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

# # Add collision to the cloth object
# bpy.ops.object.modifier_add(type='COLLISION')
# cloth_collision_mod = cloth_obj.modifiers[-1]
# cloth_collision_mod.name = 'ClothCollision'
# cloth_collision_mod.object = plane

# Set up camera
cam = bpy.data.cameras.new(name="Camera")
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam)
cam_obj.location = (0, -3, 2) # Update camera location
cam_obj.rotation_mode = 'XYZ' # Set rotation mode to XYZ
cam_obj.rotation_euler = (0.6, 0, 0)  # Update camera rotation (in radians)
bpy.context.scene.camera = cam_obj
bpy.data.collections["Collection"].objects.link(cam_obj)

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

output_path = os.path.join(output_folder, 'animation_spin0.mp4')

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
