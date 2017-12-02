import bpy
def clear():
	candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

	# select them only.
	for object_name in candidate_list:
		bpy.data.objects[object_name].select = True

	# remove all selected.
	bpy.ops.object.delete()

	# remove the meshes, they have no users anymore.
	for item in bpy.data.meshes:
		bpy.data.meshes.remove(item)