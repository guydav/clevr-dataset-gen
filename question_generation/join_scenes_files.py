import json
import os
import glob


SCENE_FILE_GLOB = '../meta_learning_50k/CLEVR_scenes_part_*.json'
ALL_SCENE_FOLDER = '../meta_learning_50k/scenes'
OUTPUT_PATH = '../meta_learning_50k/CLEVR_scenes.json'


if __name__ == '__main__':
    files = sorted(glob.glob(SCENE_FILE_GLOB))

    with open(files[0], 'r') as first_file:
        output = json.load(first_file)

    all_scenes = []
    all_scene_files_paths = sorted(os.listdir(ALL_SCENE_FOLDER))

    for scene_path in all_scene_files_paths:
        with open(os.path.join(ALL_SCENE_FOLDER, scene_path), 'r') as f:
            all_scenes.append(json.load(f))

    output['scenes'] = all_scenes

    with open(OUTPUT_PATH, 'w') as output_file:
        json.dump(output, output_file)
