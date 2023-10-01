#!/usr/bin/env python3

import sys
import csv
from datetime import datetime, timedelta
import json

# User-defined variables
event_name = "BEAR 100 Race - 2023"
aid_station_number = 4
aid_station_name = "Right Hand Fork"

# Load or initialize the filename counter
try:
    with open("filename_counter.txt", "r") as counter_file:
        csv_filename_counter = int(counter_file.read().strip())
except FileNotFoundError:
    csv_filename_counter = 1

def convert_time(epoch, minutes):
    full_epoch = epoch * 60 * 1000  # Convert to milliseconds
    time = datetime.fromtimestamp(full_epoch / 1000) + timedelta(minutes=minutes)
    return time.strftime('%H:%M:%S %d %b')

def main():
    global csv_filename_counter

    # Check if data is piped into stdin
    if sys.stdin.isatty():
        print("Please enter the base epoch time JSON and data (Press Ctrl+D when done):")
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        base_epoch = json.loads(lines.pop(0).strip())['epoch']
    else:
        lines = sys.stdin.readlines()
        base_epoch = json.loads(lines.pop(0).strip())['epoch']

    # Extract and convert the base epoch time
    base_epoch = int(base_epoch)

    # Prepare the CSV output
    csv_output = []
    csv_output.append([event_name, f"Aid Station #{aid_station_number} - {aid_station_name}",
                       "All times are based off of the system they were recorded on"])
    csv_output.append(["Sequence", "X", "Runner#", "In Time", "Out Time", "Notes"])

    sequence = 1
    for line in lines:
        data = line.strip().split(',')
        runner_number = data[0]
        in_minutes = data[1]
        out_minutes = data[2]
        note = data[3] if len(data) > 3 else ""
        in_time = convert_time(base_epoch, int(in_minutes)) if in_minutes else ""
        if out_minutes:  # Check if out_minutes is non-empty
            out_time = convert_time(base_epoch, int(out_minutes))
        elif len(data) > 3:
            out_time = "DNF"
        else:
            out_time = ""
        csv_output.append([sequence, '', runner_number, in_time, out_time, note])
        sequence += 1

    # Print CSV to stdout
    for row in csv_output:
        row = ['"' + str(item) + '"' for item in row]  # Enclose each field in double quotes
        print(','.join(row))

    # Save CSV to a file with a dynamic filename
    csv_file = f"AID{str(aid_station_number).zfill(2)}_{csv_filename_counter}.csv"
    csv_filename_counter += 1
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in csv_output:
            writer.writerow(row)

    # Save the updated counter value to a file
    with open("filename_counter.txt", "w") as counter_file:
        counter_file.write(str(csv_filename_counter))
    
    print(f"CSV data has been saved to {csv_file}.")

if __name__ == "__main__":
    main()

