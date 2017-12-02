import sys
sys.path.append("C:\work\workBox\BlenderFiles\starshipGenerator")
import clear
import bpy
import random
import math
import modelPartGenerator
import imp

def addChild(name, mesh):
	ob = bpy.data.objects.new(name, mesh) # Create an object with that mesh
	ob.show_name = True
	bpy.context.scene.objects.link(ob) # Link object to scene
	return ob

def main():
	print("global start")
	print("generation --start")
	clear.clear()
	imp.reload(modelPartGenerator)

	mesh = modelPartGenerator.generate("mainMesh") # Create a new mesh
	hull = addChild("hull", mesh)
	bpy.data.scenes["Scene"].update()
	#dummy = addChild("fakeHull", mesh)
	#!!bpy.data.objects["hull"].closest_point_on_mesh((x,x,x))!!
	#location, normal, index
	# (
	# 	Vector((0.5422042012214661, 1.0032684803009033, 0.8865776062011719)), 
	# 	Vector((-0.9541674256324768, -0.1835169941186905, -0.23640218377113342)), 
	# 	5
	# )
	for j in range(2, 5):
		partsNumber = random.randint(1,4)
		mesh = modelPartGenerator.generate("partMesh" + str(j))
		direction = random.choice([-math.pi, 0])

		for i in range(0, partsNumber):
			objct = addChild('object' + str(j) + "-" + str(i), mesh)
			partSin = math.sin(2*math.pi/partsNumber*i) * 100
			partCos = math.cos(2*math.pi/partsNumber*i) * 100
			if(direction >= 0):
				partDepth = (bpy.data.objects["hull"].bound_box[2][1] - bpy.data.objects["hull"].bound_box[0][1]) * (random.random()+0.1)
			else:
				partDepth = (bpy.data.objects["hull"].bound_box[2][1] + bpy.data.objects["hull"].bound_box[0][1]) * (random.random()+0.1)
			closestLocation = hull.closest_point_on_mesh((partCos, partDepth, partSin))
			objct.location = closestLocation[0]
			objct.rotation_euler.z = direction
			
			scaleFactor = 1/(j/2)
			objct.scale = [scaleFactor, scaleFactor, scaleFactor]
			#objct.rotation_euler = [-directionChanger * math.pi/2,-math.pi/2 ,0]
			#objct.rotation_euler = closestLocation[1]
			
			# objct.rotation_quaternion.x = closestLocation[1][0]
			# objct.rotation_quaternion.y = closestLocation[1][1]
			# objct.rotation_quaternion.z = closestLocation[1][2]

		for i in range(0,partsNumber):
			bpy.ops.object.select_all(action='DESELECT')
			hull.select = True
			bpy.context.scene.objects.active = hull
			bpy.ops.object.modifier_add(type='BOOLEAN')
			objct = bpy.data.objects['object' + str(j) + "-" + str(i)]
			mod = hull.modifiers[0]
			mod.name = "unionMod"
			mod.operation = 'UNION'
			mod.object = objct
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)	
			hull.select = False
			objct.select = True
			bpy.context.scene.objects.active = objct
			bpy.ops.object.delete()

	bpy.ops.object.select_all(action='DESELECT')
	hull.select = True
	bpy.context.scene.objects.active = hull
	bpy.ops.object.modifier_add(type='REMESH')
	mod = hull.modifiers[0]
	mod.name = "remeshMod"
	mod.mode = "SMOOTH"
	mod.scale = 1
	mod.octree_depth = 4
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

	#Intresting Modifiers: Cast Displace SimpleDeform(Bend Stretch) Smooth Wave 
	hull.rotation_euler = [0,-math.pi/2 ,0]
	print('global finish')

if __name__ == "__main__":
	main()