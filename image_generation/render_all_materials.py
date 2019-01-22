import os


PROPERTIES_TEMPLATE = """
{
  "shapes": {
    "shape_name": "shape_file"
  },
  "colors": {
    "gray": [87, 87, 87],
    "red": [173, 35, 35],
    "blue": [42, 75, 215],
    "green": [29, 105, 20],
    "brown": [129, 74, 25],
    "purple": [129, 38, 192],
    "cyan": [41, 208, 208],
    "yellow": [255, 238, 51],
    "orange": [255, 146, 51],
    "pink": [255, 205, 243]
  },
  "materials": {
    "material_name": "material_file"
  },
  "sizes": {
    "large": 1.0
  }
}
"""

COMMAND_TEMPLATE = '/Applications/Blender/blender.app/Contents/MacOS/blender --background --python render_images.py -- --properties_json "{properties_path}" --output_image_dir "../output/final_preview/{shape_name}/{material_name}" --output_scene_dir "../output/materials/scenes" --output_scene_file "../output/materials/CLEVR_scenes.json"  --render_num_samples 64 --num_images {num_images} --min_objects {num_objects} --max_objects {num_objects} --margin 0.5  --min_rotation_angle 45 --max_rotation_angle 45 --render_tile_size 256 --camera_jitter 0  --min_pixels_per_object 300 --width 128 --height 128 --base_scene_blendfile "data/base_scene_modified.blend"'


SHAPES = {
    # "cube": "SmoothCube_v2",
    # "sphere": "Sphere",
    # "cylinder": "SmoothCylinder",
    # "pyramid": "Pyramid",
    # "cone": "Cone",
    # "torus": "Torus",
    # "rectangle": "RectangularBox",
    # "ellipsoid": "Ellipsoid",
    # "octahedron": "Octahedron",
    "dodecahedron": "Dodecahedron"
}


MATERIALS = {
    "metal": "MyMetal",
    "rubber": "Rubber",
    "chain_mail": "BSDFChainMail",
    "marble": "BSDFMarble",
    # "maze": "BSDFMaze",
    # "metal_weave": "BSDFMetalWeave",
    # "polka": "BSDFPolka",
    # "rug": "BSDFRug",
    # "tiles": "BSDFTiles",
    # "wood_plank": "BSDFWoodPlank"
}


NUM_IMAGES_PER_MATERIAL = 5
NUM_OBJECTS_PER_IMAGE = 4
MATERIAL_DIR = 'data/materials'
PROPERTIES_PATH_TEMPLATE = '~/temp/properties.{name}.json'


def main():
    # for material_file in os.listdir(MATERIAL_DIR):
    #     material_name = os.path.splitext(material_file)[0]
    #
    #     if not material_file.endswith('.blend') or material_name not in MISSING_MATERIALS:
    #         print('*' * 50)
    #         print('Skipping ', material_file)
    #         print('*' * 50)
    #         continue

    for shape_name in SHAPES:
        print('*' * 50)
        print('Starting ', shape_name)
        print('*' * 50)

        properties_with_shape = PROPERTIES_TEMPLATE.\
            replace('shape_name', shape_name).\
            replace('shape_file', SHAPES[shape_name])

        for material_name in MATERIALS:
            print('*' * 50)
            print('Starting ', material_name)
            print('*' * 50)

            properties = properties_with_shape.\
                replace('material_name', material_name).\
                replace('material_file', MATERIALS[material_name])
            properties_path = os.path.expanduser(PROPERTIES_PATH_TEMPLATE.format(name=material_name))

            with open(properties_path, 'w') as f:
                f.write(properties)
                f.flush()
                f.close()

            # os.mkdir("../output/materials/{name}/images".format(name=material_name))

            command = COMMAND_TEMPLATE.format(properties_path=properties_path,
                                              shape_name=shape_name,
                                              material_name=material_name,
                                              num_images=NUM_IMAGES_PER_MATERIAL,
                                              num_objects=NUM_OBJECTS_PER_IMAGE)

            os.system(command)


if __name__ == '__main__':
    # print(os.getcwd())
    main()

