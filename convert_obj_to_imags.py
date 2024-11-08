import pyrender
import trimesh
import numpy as np
import imageio

# Load the .glb model as a Trimesh Scene
scene = trimesh.load('/content/assets/3d-vh-f-lung.glb')

# Create a Pyrender scene
pyrender_scene = pyrender.Scene()

# Add each mesh in the Trimesh Scene to the Pyrender scene
for name, mesh in scene.geometry.items():
    pyrender_mesh = pyrender.Mesh.from_trimesh(mesh)
    pyrender_scene.add(pyrender_mesh, name=name)

# Set up the camera
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
camera_pose = np.eye(4)
camera_pose[2, 3] = 2.5  # Adjust the distance as needed
pyrender_scene.add(camera, pose=camera_pose)

# Set up the light
light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
pyrender_scene.add(light, pose=camera_pose)

# Create an offscreen renderer
renderer = pyrender.OffscreenRenderer(viewport_width=800, viewport_height=600)

# Number of images and rotation increment
num_images = 36
angle_increment = 360 / num_images

# Render loop
for i in range(num_images):
    angle = np.radians(i * angle_increment)
    
    # Rotate each mesh node around the Y-axis
    rotation = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])

    # Apply rotation to each mesh node individually
    for node in pyrender_scene.get_nodes():
        if isinstance(node.mesh, pyrender.Mesh):
            current_pose = pyrender_scene.get_pose(node)
            new_pose = rotation @ current_pose
            pyrender_scene.set_pose(node, new_pose)

    # Render the scene
    color, depth = renderer.render(pyrender_scene)
    
    # Save the image
    imageio.imwrite(f"image_{i:03d}.png", color)
    print(f"Saved image_{i:03d}.png")

# Clean up the renderer
renderer.delete()
print("All images saved successfully!")

