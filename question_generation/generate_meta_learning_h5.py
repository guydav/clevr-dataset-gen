# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import print_function
import argparse, json, os
from skimage import io, color
import h5py
import numpy as np



"""
TODO: document

TODO: add materials as well

TODO: if using num_wrong_queries, how do I devide them between properties?

TODO: multiple-property generating queries

TODO: what dtype for y and Q?

TODO: RGB or RGBA?
"""


COLOR_KEY = 'color'
SHAPE_KEY = 'shape'
MATERIAL_KEY = 'material'


parser = argparse.ArgumentParser()

# Inputs
parser.add_argument('--input_queries_file', default='../output/CLEVR_meta_learning_queries.json',
                    help='JSON file containing queries to write out')
parser.add_argument('--image_folder', default='../output/images',
                    help='The folder containing images')

# Output
parser.add_argument('--output_h5_file',
                    default='../output/CLEVR_meta_learning.h5',
                    help="The output file to write containing generated h5")

# Flags
parser.add_argument('--num_objects_per_image', default=5, type=int,
                    help='How many objects exist in each image (if variable, give the max)')
parser.add_argument('--num_dimensions', default=3, type=int,
                    help='How many relevant dimensions identify each object')

# Control which and how many images to process
parser.add_argument('--scene_start_idx', default=0, type=int,
                    help="The image at which to start generating queries; this allows " +
                         "question generation to be split across many workers")
parser.add_argument('--num_scenes', default=0, type=int,
                    help="The number of images for which to generate queries. Setting to 0 " +
                         "generates questions for all scenes in the input file starting from " +
                         "--scene_start_idx")

# Misc
parser.add_argument('--verbose', action='store_true', help="Print more verbose output")
parser.add_argument('--profile', action='store_true',
                    help="If given then run inside cProfile")
# args = parser.parse_args()


def load_image(image_folder, image_filename):
    return np.uint8(256 * color.rgba2rgb(io.imread(os.path.join(image_folder, image_filename))))


def create_dataset(output_path, image_folder, sample_query, num_images, num_query_units,
                   num_objects_per_image, num_dimensions):
    output_file = h5py.File(output_path, 'w')
    image_filename = sample_query['image_filename']
    image = load_image(image_folder, image_filename)

    X = output_file.create_dataset('X', (num_images, *image.shape), np.uint8)
    D = output_file.create_dataset('D', (num_images, num_objects_per_image, num_dimensions), np.uint8)
    Q = output_file.create_dataset('Q', (num_images,
                                         num_query_units,
                                         num_query_units), np.uint8)
    y = output_file.create_dataset('y', (num_images, num_query_units), np.uint8)

    return output_file, X, D, Q, y


def main(args):
    with open(args.input_queries_file, 'r') as f:
        queries_data = json.load(f)
        all_queries = queries_data['queries']
        all_properties = queries_data['properties']

    begin = args.scene_start_idx
    if args.num_scenes > 0:
        end = args.scene_start_idx + args.num_scenes
        all_queries = all_queries[begin:end]
    else:
        all_queries = all_queries[begin:]

    num_colors = len(all_properties['colors'])
    num_shapes = len(all_properties['shapes'])
    num_materials = len(all_properties['materials'])
    num_query_units = num_colors + num_shapes + num_materials

    output_file, X, D, Q, y = create_dataset(args.output_h5_file, args.image_folder, all_queries[0],
                                             len(all_queries), num_query_units,
                                             args.num_objects_per_image, args.num_dimensions)

    # save properties
    properties_output = output_file.create_dataset('properties', (num_query_units,),
                                                   h5py.special_dtype(vlen=str))

    color_index_to_val = {v: k for k, v in all_properties['colors'].items()}
    shape_index_to_val = {v: k for k, v in all_properties['shapes'].items()}
    material_index_to_val = {v: k for k, v in all_properties['materials'].items()}

    for i in range(num_colors):
        properties_output[i] = color_index_to_val[i]
    for i in range(num_shapes):
        properties_output[num_colors + i] = shape_index_to_val[i]
    for i in range(num_materials):
        properties_output[num_colors + num_shapes + i] = material_index_to_val[i]

    for i, query_set in enumerate(all_queries):
        # index = query_set['image_index']
        image_filename = query_set['image_filename']
        queries = query_set['queries']
        print('starting image %s (%d / %d)' % (image_filename, i + 1, len(all_queries)))

        X[i] = load_image(args.image_folder, image_filename)
        current_d = np.ones((args.num_objects_per_image, args.num_dimensions), dtype=np.uint8) * 255
        current_q = np.identity(num_query_units, dtype=np.uint8)
        current_y = np.zeros((num_query_units,), dtype=np.uint8)

        for j, query_dict in enumerate(queries):
            color_idx = query_dict[COLOR_KEY]
            shape_idx = num_colors + query_dict[SHAPE_KEY]
            material_idx = num_colors + num_shapes + query_dict[MATERIAL_KEY]

            current_d[j] = color_idx, shape_idx, material_idx

            current_y[color_idx] = 1
            current_y[shape_idx] = 1
            current_y[material_idx] = 1

        D[i] = current_d
        Q[i] = current_q
        y[i] = current_y


if __name__ == '__main__':
    args = parser.parse_args()
    if args.profile:
        import cProfile
        cProfile.run('main(args)')
    else:
        main(args)

