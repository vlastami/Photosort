
import argparse
import sys
import os.path
from os import path
from PIL import Image
import shutil
import datetime

parser = argparse.ArgumentParser()


parser.add_argument("input_dir")
parser.add_argument("output_dir")

args = parser.parse_args()


if args.input_dir == None:
    print("Chybí input_dir")
    sys.exit()

if args.output_dir == None:
    print("Chybí output_dir")
    sys.exit()

if path.exists(args.input_dir) == False:
    print("Složka input neexistuje")

if path.exists(args.output_dir) == False:
    os.makedirs(args.output_dir, exist_ok=False)


for filename in os.listdir(args.input_dir):
    absolute_path_input = os.path.join(args.input_dir,filename)
    sequence_unknown = 1
    new_filename_unknown = f"{sequence_unknown}.jpg"
    try:
        date_taken = Image.open(absolute_path_input)._getexif()[36867]
    except KeyError:
        os.makedirs(os.path.join(args.output_dir, "unknown"), exist_ok=True)
        absolute_path_output = os.path.join(args.output_dir, "unknown", new_filename_unknown)

        while path.exists(absolute_path_output):
            sequence_unknown += 1
            new_filename_unknown = f"{sequence_unknown}.jpg"
            absolute_path_output = os.path.join(args.output_dir, "unknown", new_filename_unknown)

        shutil.copyfile(absolute_path_input, os.path.join(args.output_dir, "unknown", new_filename_unknown))
        continue

    print(date_taken)

    year = date_taken[0:4]

    month = date_taken[5:7]
    day = date_taken[8:10]
    sequence = 1

    new_filename = f"{year}-{month}-{day}-{sequence}.jpg"



    absolute_path_output = os.path.join(args.output_dir,year, new_filename)

    while path.exists(absolute_path_output):
        sequence += 1
        new_filename = f"{year}-{month}-{day}-{sequence}.jpg"
        absolute_path_output = os.path.join(args.output_dir,year, new_filename)

    os.makedirs(os.path.join(args.output_dir,year), exist_ok=True)
    shutil.copyfile(absolute_path_input, absolute_path_output)

