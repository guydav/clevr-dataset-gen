#!/usr/bin/env bash

# source activate pytorch_p36

# Install Blender
sudo add-apt-repository -y ppa:thomas-schiex/blender-legacy
sudo apt-get install -y nvidia-modprobe
sudo apt update -y
sudo apt-get install -y blender

# Add startup script
sudo python ./add_blender_startup_script.py

# Fix the built-in OS numpy
sudo cp -R /home/ubuntu/anaconda3/envs/python3/lib/python3.6/site-packages/numpy /usr/lib/python3/dist-packages

# Fix a small thing in Blender's CUDA scripts
sudo python ./fix_blender_cuda.py
