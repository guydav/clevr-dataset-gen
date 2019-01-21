#!/usr/bin/env bash
blender -noaudio --background --python render_images.py -- --use_gpu 1 --properties_json "data/properties.json" --output_image_dir "../output/preview_random_spacing/images" --output_scene_dir "../output/preview_random_spacing/scenes" --output_scene_file "../output/preview_random_spacing/CLEVR_scenes.json"  --render_num_samples 512 --num_images 3 --min_objects 4 --max_objects 5 --min_dist 0.7  --min_rotation_angle 45 --max_rotation_angle 45 --camera_jitter 0  --min_pixels_per_object 700 --width 160 --height 120 --base_scene_blendfile "data/base_scene_modified.blend" --each_attribute_once --x_spacing_scale 2 --y_spacing_scale 3 --location_rotation_angle 45 --max_retries 20

#/Applications/Blender/blender.app/Contents/MacOS/blender --background --python render_images.py -- --properties_json "data/properties.json" --output_image_dir "../output/preview_circular_spacing/images" --output_scene_dir "../output/preview_circular_spacing/scenes" --output_scene_file "../output/preview_circular_spacing/CLEVR_scenes.json"  --render_num_samples 512 --num_images 10 --min_objects 3 --max_objects 5 --margin 0.5  --min_rotation_angle 45 --max_rotation_angle 45 --camera_jitter 0  --min_pixels_per_object 500 --width 128 --height 128 --base_scene_blendfile "data/base_scene_modified.blend" --each_attribute_once --spacing_scale 2.5 --equal_circular_spacing

#/Applications/Blender/blender.app/Contents/MacOS/blender --background --python render_images.py -- --properties_json "data/properties.json" --output_image_dir "../output/preview_grid_spacing/images" --output_scene_dir "../output/preview_grid_spacing/scenes" --output_scene_file "../output/preview_grid_spacing/CLEVR_scenes.json"  --render_num_samples 64 --num_images 10 --min_objects 5 --max_objects 5 --margin 0.5  --min_rotation_angle 45 --max_rotation_angle 45 --camera_jitter 0  --min_pixels_per_object 600 --width 160 --height 120 --base_scene_blendfile "data/base_scene_modified.blend" --each_attribute_once --grid_spacing --grid_size 3 --y_grid_center 0.5 --x_spacing_scale 1.5 --y_spacing_scale 3  --location_rotation_angle 45 # --render_num_samples 512
