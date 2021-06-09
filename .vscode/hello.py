import numpy as np
import pygltflib
#from pygltflib import GLTF2, BufferFormat
from pygltflib import *
from pygltflib.utils import ImageFormat, Image
import math

# https://gitlab.com/dodgyville/pygltflib#create-a-mesh-convert-to-bytes-convert-back-to-mesh

vertexes = []
indexes = []
tex_coords = []

NI = 500
NJ = 500


# vertex's
for i in range(0, NI, 1):
  for j in range(0, NJ, 1):
    x = -1.0 + i * (2.0 / NI)
    y = -1.0 + j * (2.0 / NJ)
    z = 1.0 * math.exp(-1.0 * (5.0 * x*x + 5.0 * y*y))
    v = [x, y, z]
    vertexes.append(v)
    #print('%s %d %d' % ("i, j = ", i, j))
    u = z
    v = 0.5
    tex_coords.append([u, v])


# index's
for i in range(0, NI-1, 1):
  for j in range(0, NJ-1, 1):
    ind0 = ((i+0) * NJ) + (j+0)
    ind1 = ((i+0) * NJ) + (j+1)
    ind2 = ((i+1) * NJ) + (j+0)
    ind3 = ((i+1) * NJ) + (j+1)
    t1 = [ind0, ind2, ind3]
    t2 = [ind0, ind3, ind1]
    indexes.append(t1)
    indexes.append(t2)


points = np.array(
    vertexes,
    dtype="float32",
)
triangles = np.array(
    indexes,
    dtype="uint32",  #uint8 XXX 
)
texture_coords = np.array(
    tex_coords,
    dtype="float32",
)



triangles_binary_blob = triangles.flatten().tobytes()
points_binary_blob    = points.flatten().tobytes()
texture_binary_blob   = texture_coords.flatten().tobytes()

gltf = pygltflib.GLTF2(
    scene=0,
    scenes=[pygltflib.Scene(nodes=[0])],
    nodes=[pygltflib.Node(mesh=0)],
    meshes=[
        pygltflib.Mesh(
            primitives=[
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(POSITION=1, TEXCOORD_0=2),
                    indices=0,
                    material=0
                )
            ]
        )
    ],
    accessors=[
        pygltflib.Accessor(
            bufferView=0,
            componentType=pygltflib.UNSIGNED_INT, # XXX  UNSIGNED_BYTE, UNSIGNED_INT
            count=triangles.size,
            type=pygltflib.SCALAR,
            max=[int(triangles.max())],
            min=[int(triangles.min())],
        ),
        pygltflib.Accessor(
            bufferView=1,
            componentType=pygltflib.FLOAT,
            count=len(points),
            type=pygltflib.VEC3,
            max=points.max(axis=0).tolist(),
            min=points.min(axis=0).tolist(),
        ),
       pygltflib.Accessor(
            bufferView=2,
            componentType=pygltflib.FLOAT,
            count=len(texture_coords),
            type=pygltflib.VEC2,
            max = texture_coords.max(axis=0).tolist(),
            min = texture_coords.min(axis=0).tolist(),
        ),
    ],
    bufferViews=[
        pygltflib.BufferView(
            buffer=0,
            byteOffset=0,
            byteLength=len(triangles_binary_blob),
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
        ),
        pygltflib.BufferView(
            buffer=0,
            byteOffset=len(triangles_binary_blob),
            byteLength=len(points_binary_blob),
            target=pygltflib.ARRAY_BUFFER,
        ),
        pygltflib.BufferView(
            buffer=0,
            byteOffset=len(triangles_binary_blob) + len(points_binary_blob),
            byteLength=len(texture_binary_blob),
            target=pygltflib.ARRAY_BUFFER, # er dette riktig??
        )
    ],
    buffers=[
        pygltflib.Buffer(
            byteLength=len(triangles_binary_blob) + len(points_binary_blob) + len(texture_binary_blob)
        )
    ],
)

### image for texture ###############
#https://gitlab.com/dodgyville/pygltflib#import-png-files-as-textures-into-a-gltf
image = Image()
image.uri = "colors.png"
gltf.images.append(image)
texture = Texture()
texture.source = 0
#texture.sampler = ??
gltf.textures.append(texture) 


### TEST how to add a material ######
# https://stackoverflow.com/questions/66127030/how-do-i-apply-a-material-to-a-glb-gltf-mesh
material = Material() # Create a material
pbr = PbrMetallicRoughness() # Use PbrMetallicRoughness
#pbr.baseColorFactor = [1.0, 0.0, 0.0, 1.0] # solid red

texture_info = TextureInfo()
texture_info.index = 0
pbr.baseColorTexture = texture_info # baseColorTexture is the index of the texture that will be applied to the object surface

material.pbrMetallicRoughness = pbr
material.doubleSided = True # make material double sided
material.alphaMode = MASK   # to get around 'MATERIAL_ALPHA_CUTOFF_INVALID_MODE' warning
#print(material)
###############


gltf.materials.append(material)

gltf.set_binary_blob(triangles_binary_blob + points_binary_blob + texture_binary_blob)

# alt i en fil:
#gltf.convert_buffers(BufferFormat.DATAURI)  # convert buffer URIs to data.
#gltf.save_binary("test.glb")  # try and save, will get warning.
#gltf.save_binary("test.gltf")  # try and save, will get warning.


filename = "test.gltf"
#filename = "test.glb"
gltf.save(filename)


# vertexes = [
#         [-0.5, -0.5, 0.5],
#         [0.5, -0.5, 0.5],
#         [-0.5, 0.5, 0.5],
#         [0.5, 0.5, 0.5],
#         [0.5, -0.5, -0.5],
#         [-0.5, -0.5, -0.5],
#         [0.5, 0.5, -0.5],
#         [-0.5, 0.5, -0.5],
#     ]

# indexes = [
#         [0, 1, 2],
#         [3, 2, 1],
#         [1, 0, 4],
#         [5, 4, 0],
#         [3, 1, 6],
#         [4, 6, 1],
#         [2, 3, 7],
#         [6, 7, 3],
#         [0, 2, 5],
#         [7, 5, 2],
#         [5, 7, 4],
#         [6, 4, 7],
#     ]


