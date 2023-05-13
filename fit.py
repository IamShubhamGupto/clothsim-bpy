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

filepath = "/Users/shubham/Downloads/"
cloth_file = 'cleaned0'
mann_file = 'body_frame0001'

bpy.ops.import_scene.obj(filepath=filepath+cloth_file+'.obj')

# Get the imported mesh object
cloth_obj = bpy.data.objects[cloth_file]
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
# add a cloth modifier to the cloth object
cloth_mod.settings.vertex_group_mass = "cloth_mass"
cloth_mod.settings.vertex_group_structural_stiffness = "cloth_stiffness"
cloth_mod.settings.vertex_group_bending = "cloth_bend"
# cloth_mod.settings.vertex_group_air_damping = "cloth_air"
# cloth_mod.settings.vertex_group_velocity_damping = "cloth_damp"
cloth_mod.settings.vertex_group_pressure = "cloth_pressure"
# cloth_mod.settings.vertex_group_friction = "cloth_friction"
# cloth_mod.settings.collision_settings.use_collision = True
# cloth_mod.settings.collision_settings.collision_group = 1

# import the mannequin mesh
bpy.ops.import_scene.obj(filepath=filepath+mann_file+'.obj')
mannequin_mesh = bpy.data.objects[mann_file].data
mannequin_object = bpy.data.objects[mann_file]

# move the cloth object to align with the mannequin object
# this example assumes that the cloth mesh is initially centered at the origin
cloth_obj.location = mannequin_object.location

# scale the cloth object to fit the mannequin object
# this example assumes that the cloth mesh is initially the same size as the mannequin mesh
scale_factor = mannequin_object.dimensions[0] / cloth_obj.dimensions[0]
cloth_obj.scale = (scale_factor, scale_factor, scale_factor)

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 100
bpy.ops.ptcache.bake_all(bake=True)

# Set up the output folder for the baked frames
output_folder = "output/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path = os.path.join(output_folder, 'animation_man.mp4')

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

