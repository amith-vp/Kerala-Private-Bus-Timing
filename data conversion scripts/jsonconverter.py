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

