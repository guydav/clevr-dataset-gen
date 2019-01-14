INSIDE_BLENDER = True
try:
    import bpy, bpy_extras
    from mathutils import Vector
    import utils
except ImportError as e:
    INSIDE_BLENDER = False


def main():
    bpy.ops.wm.open_mainfile(filepath='data/blank_scene.blend')

    render_args = bpy.context.scene.render
    render_args.engine = "CYCLES"
    render_args.filepath = '/Users/guydavidson/Downloads/blender_test_render_2.png'

    # exec(open('/Users/guydavidson/projects/clevr-dataset-gen/image_generation/simple_render.py', 'r').read())

    import os

    base_dir = '/Users/guydavidson/projects/clevr-dataset-gen/image_generation/data'
    object_dir = os.path.join(base_dir, 'shapes')
    material_dir = os.path.join(base_dir, 'materials')

    object_name = 'SmoothCube_v2'
    material_name = 'BSDFWoodFloor'

    # add object
    filename = os.path.join(object_dir, '%s.blend' % object_name, 'Object', object_name)
    bpy.ops.wm.append(filename=filename)

    # Give it a new name to avoid conflicts
    new_name = '%s_%d' % (object_name, 0)
    bpy.data.objects[object_name].name = new_name

    # load material
    filepath = os.path.join(material_dir, material_name + '.blend', 'NodeTree', material_name)
    bpy.ops.wm.append(filename=filepath)

    # join material to object
    OUTPUT_KEYS = ('Shader', 'BSDF')

    # Figure out how many materials are already in the scene
    mat_count = len(bpy.data.materials)

    # Create a new material
    mat = bpy.data.materials.new('Material_%d' % mat_count)
    mat.use_nodes = True

    if 'Diffuse BSDF' in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(mat.node_tree.nodes['Diffuse BSDF'])

    # Attach the new material to the active object
    # Make sure it doesn't already have materials
    bpy.context.scene.objects.active = bpy.data.objects[new_name]
    obj = bpy.context.active_object
    assert len(obj.data.materials) == 0
    obj.data.materials.append(mat)

    # Find the output node of the new material
    # output_node = None
    # for n in mat.node_tree.nodes:
    #     if n.name == 'Material Output':
    #         output_node = n
    #         break
    output_node = mat.node_tree.nodes['Material Output']

    # Add a new GroupNode to the node tree of the active material,
    # and copy the node tree from the preloaded node group to the
    # new group node. This copying seems to happen by-value, so
    # we can create multiple materials of the same type without them
    # clobbering each other
    group_node = mat.node_tree.nodes.new('ShaderNodeGroup')
    group_node.node_tree = bpy.data.node_groups[material_name]

    # Find and set the "Color" input of the new group node
    group_node.inputs['Color'].default_value = [0.0, 1.0, 0.0, 1.0]

    # Wire the output of the new group node to the input of
    # the MaterialOutput node

    assert (any([key in group_node.outputs for key in OUTPUT_KEYS]))

    for key in OUTPUT_KEYS:
        if key in group_node.outputs:
            mat.node_tree.links.new(
                group_node.outputs[key],
                output_node.inputs['Surface'],
            )
            break

    obj.active_material = mat

    # Fix all image paths
    for image in bpy.data.images:
        if image.filepath is None or len(image.filepath) == 0:
            continue

        fixed_path = os.path.abspath(os.path.join(os.getcwd(), image.filepath)).replace('//data', '')
        image.filepath = fixed_path

    while True:
        try:
            bpy.ops.render.render(write_still=True)
            break
        except Exception as e:
            print(e)

    bpy.ops.wm.save_as_mainfile(filepath='/Users/guydavidson/Downloads/blender_test_2.blend')


if __name__ == '__main__':
    if INSIDE_BLENDER:
        main()
