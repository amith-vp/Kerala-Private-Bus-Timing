# Kerala Private Bus Schedule 

## Overview

This repository hosts a dataset of Kerala state's private bus schedule, initially available in PDF format, now conveniently converted to JSON. The dataset aims to offer detailed information about major bus stops, timings, vehicle number regarding private bus services in Kerala.

If you find any parsing errors, please create a pull request (PR) or a raise an issue

## Structure
```json
{
      "Vehicle Number": "KL 05 AQ 4567",
      "route": [
        "ALUVA BANK JUNCTION",
        "PULINCHODE SIGNAL JUNCTION",
        "COMPANYPADI",
        "MUTTOM"
      ],
      "schedule": [
        {
          "trip": 1,
          "stations": [
            {
              "station": "ALUVA BANK JUNCTION",
              "arrivalTime": "05:00 am",
              "departureTime": "05:00 am"
            },
            {
              "station": "PULINCHODE SIGNAL JUNCTION",
              "arrivalTime": "05:07 am",
              "departureTime": "05:07 am"
            },
            {
              "station": "COMPANYPADI",
              "arrivalTime": "05:15 am",
              "departureTime": "05:15 am"
            },
            {
              "station": "MUTTOM",
              "arrivalTime": "05:18 am",
              "departureTime": "05:18 am"
            }
          ]
        },
        {
          "trip": 2,
          "stations": [
            {
              "station": "MUTTOM",
              "arrivalTime": "05:19 am",
              "departureTime": "05:19 am"
            },
            {
              "station": "COMPANYPADI",
              "arrivalTime": "05:20 am",
              "departureTime": "05:20 am"
            },
            {
              "station": "PULINCHODE SIGNAL JUNCTION",
              "arrivalTime": "05:30 am",
              "departureTime": "05:30 am"
            },
            {
              "station": "ALUVA BANK JUNCTION",
              "arrivalTime": "05:55 am",
              "departureTime": "05:55 am"
            }
          ]
        }
      ]
    }
```

## Disclaimer

This dataset is compiled from publicly available information and may not encompass the complete Kerala private bus schedule or accurate data(parsing errors). Users are advised to verify information from official sources or contact relevant authorities for the most accurate and up-to-date schedule details.

## Conversion Process

1. **Preprocessing:**
   - [Adobe's PDF-to-Word online tool](https://www.adobe.com/in/acrobat/online/pdf-to-word.html) to convert the PDF to DOCX format and then back to PDF due to parsing errors in the original PDF.

2. **Table Extraction:**
   - Employed the [PDF Table Extractor tool](https://ronnywang.github.io/pdf-table-extractor/) to extract tabular data from the PDF files.

3. **PDF Content to XML:**
   - Used the `pdftohtml` command-line tool with options `-c -i -hidden -xml` to convert the PDF content to XML format.[Reference](https://datascience.blog.wzb.eu/2017/02/16/data-mining-ocr-pdfs-using-pdftabextract-to-liberate-tabular-data-from-scanned-documents/)

4. **Preprocessing Script:**
   - To remove unnecessary fields or data inconsistencies from the extracted table data.
   ```py
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
   ```

5. **Vehicle Information Processing :**
   - Combine and organize vehicle numbers into the JSON format

   ```py
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

   
   ```

6. **Conversion to Formatted JSON :**
   ```py
    import json
    from datetime import datetime

    with open('input.json', 'r') as file:
        data = json.load(file)
    bus_schedule_data = []

    for page_table in data['pageTables']:
        header_row = page_table['tables'][0]
        print(page_table['page'])

        stations = [header_row[i] for i in range(len(header_row)) if i % 3 == 2]

        num_trips = page_table['height'] - 2  
        bus_schedules = []
        if page_table['height'] == 1:
            exit()


        route_name = stations  

        for trip_num in range(1, num_trips + 1):
            trip_info = {"trip": trip_num, "stations": []}
            trip_stations = []

            for i, station in enumerate(stations):
                departure_index = 3 + i * 3
                arrival_index = 2 + i * 3

                departure_time = page_table['tables'][trip_num + 1][departure_index].strip()
                arrival_time = page_table['tables'][trip_num + 1][arrival_index].strip()

                if departure_time or arrival_time:
                    if not departure_time:
                        departure_time = arrival_time
                    elif not arrival_time:
                        arrival_time = departure_time
                    station_info = {
                        "station": station,
                        "arrivalTime": arrival_time,
                        "departureTime": departure_time
                    }
                    trip_info["stations"].append(station_info)

            if trip_info["stations"]:
                bus_schedules.append(trip_info)

        for trip_info in bus_schedules:
            trip_info["stations"] = sorted(trip_info["stations"], key=lambda x: datetime.strptime(x["departureTime"], '%I:%M %p'))

        bus_schedule_data.append({
            "Vehicle Number": page_table['vehicle_number'],
            "route": route_name,
            "schedule": bus_schedules
        })

    output_data = {"busSchedules": bus_schedule_data}

    with open('output.json', 'w') as output_file:
        json.dump(output_data, output_file, indent=2)

   
   ```
