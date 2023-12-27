#if you want to merge all json files to single one.

import glob
import json

read_files = glob.glob("*.json")
output_list = []

for f in read_files:
    with open(f, "rb") as infile:
        output_list.append(json.load(infile))

final_json = {}
all_items = []

for json_file in output_list:
    all_items.extend(json_file['busSchedules'])

final_json['busSchedules'] = all_items

with open('merged_json.json', 'w') as textfile_merged:
    json.dump(final_json, textfile_merged, indent=2)
