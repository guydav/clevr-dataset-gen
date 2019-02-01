# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import print_function
import argparse, json, os, itertools, random, shutil
import time
import re


"""
TODO: document

TODO: if using num_wrong_queries, how do I divide them between properties?

"""

parser = argparse.ArgumentParser()

# Inputs
parser.add_argument('--input_scene_file', default='../output/CLEVR_scenes.json',
        help="JSON file containing ground-truth scene information for all images " +
             "from render_images.py")
parser.add_argument('--properties_file', default='../image_generation/data/properties.json',
                    help='The properties file used to generate the images in render_images.py')
# parser.add_argument('--num_features', default=1, type=int,
#                     help="The number of features to build queries about.")
# parser.add_argument('--only_true', action='store_true', help="Generate only true queries")
# parser.add_argument('--num_wrong_queries', default=0, type=int,
#                     help="The number of wrong queries to generate per image. If 0, generates all.")

# Output
parser.add_argument('--output_queries_file',
                    default='../output/CLEVR_meta_learning_queries.json',
                    help="The output file to write containing generated queries")

# Control which and how many images to process
parser.add_argument('--scene_start_idx', default=0, type=int,
                    help="The image at which to start generating queries; this allows " +
                         "question generation to be split across many workers")
parser.add_argument('--num_scenes', default=0, type=int,
                    help="The number of images for which to generate queries. Setting to 0 " +
                         "generates questions for all scenes in the input file starting from " +
                         "--scene_start_idx")

# Misc
parser.add_argument('--reset_counts_every', default=250, type=int,
                    help="How often to reset template and answer counts. Higher values will " +
                         "result in flatter distributions over templates and answers, but " +
                         "will result in longer runtimes.")
parser.add_argument('--verbose', action='store_true', help="Print more verbose output")
parser.add_argument('--time_dfs', action='store_true',
                    help="Time each depth-first search; must be given with --verbose")
parser.add_argument('--profile', action='store_true',
                    help="If given then run inside cProfile")
# args = parser.parse_args()


COLOR_KEY = 'color'
SHAPE_KEY = 'shape'
MATERIAL_KEY = 'material'


# def generate_false_queries(scene_questions, num_wrong_queries, objects, property_key, property_values):
#     true_properties = set([obj[property_key] for obj in objects])
#
#     if num_wrong_queries == 0:
#         for i, false_prop in enumerate(property_values):
#             if false_prop not in true_properties:
#                 scene_questions.append(({property_key: i}, False))
#
#     else:
#         values_copy = property_values.copy()
#         for true_prop in true_properties:
#             values_copy.remove(true_prop)
#
#         false_values = random.sample(values_copy, num_wrong_queries)
#         for false_prop in false_values:
#             scene_questions.append(({property_key: property_values.index(false_prop)}, False))


def main(args):
    # Read file containing input scenes
    all_scenes = []
    with open(args.input_scene_file, 'r') as f:
        scene_data = json.load(f)
        all_scenes = scene_data['scenes']
        scene_info = scene_data['info']
    begin = args.scene_start_idx
    if args.num_scenes > 0:
        end = args.scene_start_idx + args.num_scenes
        all_scenes = all_scenes[begin:end]
    else:
        all_scenes = all_scenes[begin:]

    # Read file containing input properties
    with open(args.properties_file, 'r') as f:
        properties = json.load(f)
        colors = sorted(properties['colors'].keys())
        shapes = sorted(properties['shapes'].keys())
        materials = sorted(properties['materials'].keys())

    queries = []
    scene_count = 0
    for i, scene in enumerate(all_scenes):
        scene_fn = scene['image_filename']
        scene_struct = scene
        print('starting image %s (%d / %d)' % (scene_fn, i + 1, len(all_scenes)))

        scene_count += 1
        scene_queries = []
        scene_objects = scene_struct['objects']

        for obj in scene_objects:
            # generate true queries
            scene_queries.append({COLOR_KEY: colors.index(obj[COLOR_KEY]),
                                  SHAPE_KEY: shapes.index(obj[SHAPE_KEY]),
                                  MATERIAL_KEY: materials.index(obj[MATERIAL_KEY])})

        # if not args.only_true:
        #     for key, values in [(COLOR_KEY, colors), (SHAPE_KEY, shapes)]:
        #         generate_false_queries(scene_queries, args.num_wrong_queries, scene_objects,
        #                                key, values)

        image_index = int(os.path.splitext(scene_fn)[0].split('_')[-1])
        queries.append({
            'split': scene_info['split'],
            'image_filename': scene_fn,
            'image_index': image_index,
            'image': os.path.splitext(scene_fn)[0],
            'queries': scene_queries,
        })

    with open(args.output_queries_file, 'w') as f:
        print('Writing output to %s' % args.output_queries_file)
        json.dump({
            'info': scene_info,
            'queries': queries,
            'properties': {
                'colors': {color: colors.index(color) for color in colors},
                'shapes': {shape: shapes.index(shape) for shape in shapes},
                'materials': {mat: materials.index(mat) for mat in materials}

            },
        }, f)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.profile:
        import cProfile
        cProfile.run('main(args)')
    else:
        main(args)

