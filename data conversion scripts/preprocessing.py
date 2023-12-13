 import json
 file_path = 'input.json'  
 with open(file_path, 'r') as file:
     json_data = json.load(file)
 filtered_tables = []
 for entry in json_data['pageTables']:
     if 'tables' in entry:
         entry.pop('merges', None)
         entry.pop('merge_alias', None)
         entry.pop('width', None)
         filtered_tables.append(entry)

 json_data['pageTables'] = filtered_tables

 with open(file_path, 'w') as file:
     json.dump(json_data, file, indent=2)

 with open('input.json', 'w') as file:
     json.dump(json_data, file, indent=2)
