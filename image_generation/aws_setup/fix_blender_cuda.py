
cuda_file_path = '/usr/share/blender/2.79/scripts/addons/cycles/source/util/util_half.h'
target_line = 'typedef unsigned short half;'
new_line = '#include "cuda_fp16.h"'

line_index = None
cuda_lines = []

with open(cuda_file_path, 'r') as cuda_file_in:
    cuda_lines = cuda_file_in.readlines()
    for index, line in enumerate(cuda_lines):
        if target_line == line.strip().lower():
            line_index = index
            break

cuda_lines[index] = f'// {target_line}'
cuda_lines.insert(index + 1, new_line)

with open(cuda_file_path, 'w') as cuda_file_out:
    cuda_file_out.write('\n'.join(cuda_lines))

