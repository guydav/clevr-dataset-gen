script_data = """
import sys
def register(*args):
    sys.path.append('/home/ubuntu/clevr-dataset-gen/image_generation')
    print('CLEVR appended')

"""

output_path = '/usr/share/blender/2.79/scripts/startup/add_to_path.py'

with open(output_path, 'w') as script_file:
    script_file.write(script_data)
    script_file.flush()
    script_file.close()
