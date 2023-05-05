
import bpy
import os

# Get the cube object
cube_obj = bpy.data.objects['Cube']

# Select the object
bpy.ops.object.select_all(action='DESELECT')
cube_obj.select_set(True)

# Remove the object
bpy.ops.object.delete(use_global=False)

# # Set up camera
# cam = bpy.data.cameras.new(name="Camera")
# cam_obj = bpy.data.objects.new(name="Camera", object_data=cam)
# cam_obj.location = (0, -5, 2)
# cam_obj.rotation_euler = (1.0472, 0, 0)  # 60 degrees in radians
# bpy.context.scene.camera = cam_obj
# bpy.data.collections["Collection"].objects.link(cam_obj)

# # Set up lighting
# light_data = bpy.data.lights.new(name="Light", type='SUN')
# light_obj = bpy.data.objects.new(name="Light", object_data=light_data)
# light_obj.location = (-5, -5, 5)
# bpy.data.collections["Collection"].objects.link(light_obj)

# Import the body and cloth objects
body_file = "/Users/shubham/Downloads/reconstruction-dan-001/frame0001/tposed/tposed_000000481.obj"
cloth_file = "/Users/shubham/Downloads/reconstruction-dan-001/frame0001/mesh/mesh_000000481.obj"
bpy.ops.import_scene.obj(filepath=body_file)
bpy.ops.import_scene.obj(filepath=cloth_file)

body_obj = bpy.data.objects["tposed_000000481"]
bpy.ops.object.select_all(action='DESELECT')
body_obj.select_set(True)
bpy.context.view_layer.objects.active = body_obj

# Set up camera
cam = bpy.data.cameras.new(name="Camera")
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam)
cam_obj.location = (0, -3, 2) # Update camera location
cam_obj.rotation_mode = 'XYZ' # Set rotation mode to XYZ
cam_obj.rotation_euler = (0.6, 0, 0)  # Update camera rotation (in radians)
bpy.context.scene.camera = cam_obj
bpy.data.collections["Collection"].objects.link(cam_obj)

# Set up lighting
light_data = bpy.data.lights.new(name="Light", type='SUN')
light_obj = bpy.data.objects.new(name="Light", object_data=light_data)
light_obj.location = (0, -5, 5) # Update lighting location
light_obj.rotation_mode = 'XYZ' # Set rotation mode to XYZ
light_obj.rotation_euler = (1.2, 0, 0)  # Update lighting rotation (in radians)
bpy.data.collections["Collection"].objects.link(light_obj)

# Add material to body object
body_material = bpy.data.materials.new(name="BodyMaterial")
body_material.diffuse_color = (1, 0.8, 0.6, 1)  # skin color
body_obj.data.materials.append(body_material)

bpy.ops.object.modifier_add(type='COLLISION')

cloth_obj = bpy.data.objects["mesh_000000481"]
bpy.ops.object.select_all(action='DESELECT')
cloth_obj.select_set(True)
bpy.context.view_layer.objects.active = cloth_obj

# Add material to cloth object
cloth_material = bpy.data.materials.new(name="ClothMaterial")
cloth_material.diffuse_color = (0.8, 0.8, 0.8, 1)  # gray color
cloth_obj.data.materials.append(cloth_material)

bpy.ops.object.modifier_add(type='CLOTH')

cloth_modifier = cloth_obj.modifiers["Cloth"]
collision_collection = bpy.data.collections.new("Collision Collection")
bpy.context.scene.collection.children.link(collision_collection)
collision_collection.objects.link(body_obj)
cloth_modifier.collision_settings.collection = collision_collection

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 100
bpy.ops.ptcache.bake_all(bake=True)

# Set up the output folder for the baked frames
output_folder = "output/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path = os.path.join(output_folder, 'animation.mp4')

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

