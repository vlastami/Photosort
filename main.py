import argparse
import os.path
import shutil
from os import path
from exif import Image
import app as a
import re

def create_sequence(sequence):
    if sequence < 10:
        return f"00{sequence}"
    elif sequence < 100:
        return f"0{sequence}"
    else:
        return f"{sequence}"


def copy_file(input_path, output_path):
    sequence = 1
    filename = f"{output_path}{create_sequence(sequence)}.jpg"
    while path.exists(filename):
        sequence += 1
        filename = f"{output_path}{create_sequence(sequence)}.jpg"
    shutil.copyfile(input_path, filename)
    return f"{output_path[-11:]}{create_sequence(sequence)}"


parser = argparse.ArgumentParser()

parser.add_argument("input_dir")
parser.add_argument("output_dir")
parser.add_argument("-x", action="store_true")
parser.add_argument("-m", action="store_true")

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

if not path.exists(input_dir):
    print("This path does not exist.")

remove_files = False
if args.x:
    if re.match("[yY](?:es)?|1", input("Do you want to remove the original files after copying?").lower()):
        remove_files = True


os.makedirs(output_dir, exist_ok=True)

positions = {}

for file in os.listdir(input_dir):
    absolute_path_input = os.path.join(input_dir, file)

    try:
        with open(absolute_path_input, "rb") as img_file:
            img = Image(img_file)

        date_taken = img.datetime
        year_dir = date_taken[0:4]
        month = date_taken[5:7]
        day = date_taken[8:10]
        new_filename = f"{year_dir}-{month}-{day}-"

        latitude = img.gps_latitude[0] + img.gps_latitude[1]/60 + img.gps_latitude[2]/3600
        longitude = img.gps_longitude[0] + img.gps_longitude[1]/60 + img.gps_longitude[2]/3600

    except KeyError:
        year_dir = "unknown"
        new_filename = ""

    except AttributeError:
        latitude = None
        longitude = None
        year_dir = "unknown"
        new_filename = ""

    os.makedirs(os.path.join(output_dir, year_dir), exist_ok=True)
    absolute_path_output = os.path.join(output_dir, year_dir, new_filename)

    filename = copy_file(absolute_path_input, absolute_path_output)

    if remove_files:
        os.remove(absolute_path_input)

    if latitude or longitude is not None:
        positions[filename] = (latitude, longitude)

if args.m:
    a.open_map(positions)
