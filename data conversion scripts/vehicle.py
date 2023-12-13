 import json
 import xml.etree.ElementTree as ET

 file_path_json = 'input.json'
 with open(file_path_json, 'r') as file:
     json_data = json.load(file)

 file_path_xml = 'input.xml'
 tree = ET.parse(file_path_xml)
 root = tree.getroot()

 def extract_details(page_number):
     vehicle_number = ""
     
     for page in root.findall(".//page[@number='{}']".format(page_number)):
         for text in page.findall("./text/b"):
             text_content = text.text.strip() if text is not None and text.text is not None else ""
             if text_content.startswith("Vehicle Number"):
                 vehicle_number = text_content.split(":")[1].strip() if ":" in text_content else ""
         
     return vehicle_number


 # incase of vehicle number and  table are in different pages
 for entry in json_data['pageTables']:
     page_num = entry['page']
     vehicle_num = extract_details(page_num)
     prev_vehicle_num = extract_details(page_num-1)
     if vehicle_num=="" :
             if not prev_vehicle_num=="":
                 vehicle_num = prev_vehicle_num
         
         
     entry['vehicle_number'] = vehicle_num

 with open('input.json', 'w') as file:
     json.dump(json_data, file, indent=2)

