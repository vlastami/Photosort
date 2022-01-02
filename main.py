import argparse
import sys
import os.path
from os import path
from PIL import Image
import shutil

parser = argparse.ArgumentParser()

parser.add_argument("input_dir")
parser.add_argument("output_dir")

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

if input_dir is None:
    print("Missing input_dir")
    sys.exit()

if output_dir is None:
    print("Missing output_dir")
    sys.exit()

if not path.exists(input_dir):
    print("No input_dir")

if not path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=False)

for filename in os.listdir(input_dir):
    absolute_path_input = os.path.join(input_dir, filename)
    sequence_unknown = 1
    new_filename_unknown = f"{sequence_unknown}.jpg"
    try:
        date_taken = Image.open(absolute_path_input)._getexif()[36867]
    except KeyError:
        os.makedirs(os.path.join(output_dir, "unknown"), exist_ok=True)
        absolute_path_output = os.path.join(output_dir, "unknown", new_filename_unknown)

        while path.exists(absolute_path_output):
            sequence_unknown += 1
            new_filename_unknown = f"{sequence_unknown}.jpg"
            absolute_path_output = os.path.join(output_dir, "unknown", new_filename_unknown)

        shutil.copyfile(absolute_path_input, os.path.join(output_dir, "unknown", new_filename_unknown))
        continue

    year = date_taken[0:4]

    month = date_taken[5:7]
    day = date_taken[8:10]
    sequence = 1

    new_filename = f"{year}-{month}-{day}-{sequence}.jpg"

    absolute_path_output = os.path.join(output_dir, year, new_filename)

    while path.exists(absolute_path_output):
        sequence += 1
        new_filename = f"{year}-{month}-{day}-{sequence}.jpg"
        absolute_path_output = os.path.join(output_dir, year, new_filename)

    os.makedirs(os.path.join(output_dir, year), exist_ok=True)
    shutil.copyfile(absolute_path_input, absolute_path_output)
