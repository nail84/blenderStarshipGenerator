import bpy
import random
import math

pointsNumber = 0
edgesNumber = 3
glMeshName = "defName"

def generate(meshName):
	print('generation v0.13 ' + meshName)

	global pointsNumber
	global edgesNumber
	global glMeshName
	glMeshName = meshName
	
	coords=[]
	edges = []
	faces=[]

	edgesNumber = 8#random.randint(3,10)

	if pointsNumber == 0 :
		pointsNumber = random.randint(2,6) # Points in edge

	rands = [] # random dots in line pattern
	mainAxe = 0
	for i in range(0,pointsNumber): # generate line pattern
		elt = [random.random()*2+0.5, mainAxe, 0]
		#if elt not in rands :
		rands.append(elt)
		# mainAxe = min(10, random.random()*i+0.2) #+= random.random()/10+0.2
		mainAxe += random.random()*2+0.2

	for i in range(len(rands)-2,0,-1): # intersection check
		for j in range(len(rands)-2,0,-1):
			if(intersection([rands[i], rands[i+1]],[rands[j], rands[j+1]])):
					rands.pop(i+1)
					break

	pointsNumber = len(rands)
	ellipseFactorA = random.random() + 0.3
	ellipseFactorB = random.random() + 0.3

	for i in range(0,edgesNumber): # Generate vertices
		for x in range(0,pointsNumber):
			rnd = rands[x]; 
			coord = (
				ellipseFactorA * math.cos(2*math.pi/edgesNumber*i)*rnd[0],
				rnd[1],
				ellipseFactorB * math.sin(2*math.pi/edgesNumber*i)*rnd[0])
			coords.append(coord)

	topFace = []
	downFace = []
	for i in range(0, edgesNumber): # Generate edges & faces
		for x in range(1, pointsNumber):
			edges.append([x+pointsNumber*i-1, x+pointsNumber*i])
			
			if i < edgesNumber - 1:
				faces.append([x-1+pointsNumber*(i), x+pointsNumber*(i), (x)+pointsNumber*(i+1), (x-1)+pointsNumber*(i+1)])
			else :
				faces.append([x-1+pointsNumber*(i), x+pointsNumber*(i), (x), (x-1)])
		for y in range(0, pointsNumber):
			if i < edgesNumber - 1:
				edges.append([i*pointsNumber + y, pointsNumber*(i+1) + y])
			else :
				edges.append([i*pointsNumber + y, y])
		topFace.append(i*pointsNumber)
		downFace.append(((edgesNumber-1) - i)*pointsNumber + pointsNumber - 1) #reverse point add for correct normal
	faces.append(topFace)
	faces.append(downFace)
	
	randomMesh = bpy.data.meshes.new(meshName) # Create a new mesh
	randomMesh.from_pydata(coords, edges, faces)
	randomMesh.update()

	pointsNumber = 0

	return randomMesh

def intersection(segment1, segment2):
	v1 = ((segment2[1][0]-segment2[0][0])*(segment1[0][1]-segment2[0][1])-
		(segment2[1][1]-segment2[0][1])*(segment1[0][0]-segment2[0][0]))
	v2 = ((segment2[1][0]-segment2[0][0])*(segment1[1][1]-segment2[0][1])-
		(segment2[1][1]-segment2[0][1])*(segment1[1][0]-segment2[0][0]))
	v3 = ((segment1[1][0]-segment1[0][0])*(segment2[0][1]-segment1[0][1])-
		(segment1[1][1]-segment1[0][1])*(segment2[0][0]-segment1[0][0]))
	v4 = ((segment1[1][0]-segment1[0][0])*(segment2[1][1]-segment1[0][1])-
		(segment1[1][1]-segment1[0][1])*(segment2[1][0]-segment1[0][0]))
	
	return (v1 * v2 < 0) and (v3 * v4 < 0)

#
# FOR STANDALONE USE
#

def main():
	import sys
	#sys.path.append("C:\work\workBox\BlenderFiles")
	import clear
	clear.clear()

	randomMesh = generate("randomMesh") # Create a new mesh  
	ob = bpy.data.objects.new("randomObject", randomMesh) # Create an object with that mesh
	ob.location = bpy.context.scene.cursor_location # Position object at 3d-cursor
	ob.show_name = True
	bpy.context.scene.objects.link(ob) # Link object to scene

if __name__ == "__main__":
    main()