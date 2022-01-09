import argparse
import os.path
from os import path
from PIL import Image
import shutil


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


parser = argparse.ArgumentParser()

parser.add_argument("input_dir")
parser.add_argument("output_dir")
parser.add_argument("-x", action="store_true")

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir


if not path.exists(input_dir):
    print("This path does not exist.")

remove_files = False
if args.x:
    if input("Do you want to remove the original files after copying?").lower() == ("y" or "yes"):
        remove_files = True


os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    absolute_path_input = os.path.join(input_dir, file)

    try:
        date_taken = Image.open(absolute_path_input)._getexif()[36867]
        year_dir = date_taken[0:4]
        month = date_taken[5:7]
        day = date_taken[8:10]
        new_filename = f"{year_dir}-{month}-{day}-"

    except KeyError:
        year_dir = "unknown"
        new_filename = ""

    os.makedirs(os.path.join(output_dir, year_dir), exist_ok=True)
    absolute_path_output = os.path.join(output_dir, year_dir, new_filename)

    copy_file(absolute_path_input, absolute_path_output)
    if remove_files:
        os.remove(absolute_path_input)

"""import gmaps
gmaps.configure(api_key='AI...')
nuclear_power_plants = [
{'name': 'Atucha', 'location': (-34.0, -59.167), 'active_reactors': 1},
{'name': 'Embalse', 'location': (-32.2333, -64.4333), 'active_reactors': 1},
{'name': 'Armenia', 'location': (40.167, 44.133), 'active_reactors': 1},
{'name': 'Br', 'location': (51.217, 5.083), 'active_reactors': 1},
{'name': 'Doel', 'location': (51.333, 4.25), 'active_reactors': 4},
{'name': 'Tihange', 'location': (50.517, 5.283), 'active_reactors': 3}
]
plant_locations = [plant['location'] for plant in nuclear_power_plants]
info_box_template = 
<dl>
<dt>Name</dt><dd>{name}</dd>
<dt>Number reactors</dt><dd>{active_reactors}</dd>
</dl>

plant_info = [info_box_template.format(**plant) for plant in nuclear_power_plants]
marker_layer = gmaps.marker_layer(plant_locations, info_box_content=plant_info)
fig = gmaps.figure()
fig.add_layer(marker_layer)
fig"""