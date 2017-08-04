#!/usr/bin/python3
import os
import subprocess
import chardet

script_location = os.path.dirname(__file__)

midi_directory = os.path.join(script_location, "../midi-files")
csv_directory = os.path.join(script_location, "../csv-files")

midi_files = []

for filename in os.listdir(midi_directory):
    if filename.endswith(".mid"): 
        midi_files.append(filename)
        continue
    else:
        continue

print("Found MIDI files:", midi_files)

# Clean CSV folder
for file in os.listdir(csv_directory):
    file_path = os.path.join(csv_directory, file)
    try:
        if os.path.isfile(file_path) and file_path.endswith(".csv"):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# Generate CSV files
output_files = []

for i, midi_file in enumerate(midi_files):
    subprocess.call([os.path.join(script_location, '../midicsv/midicsv'), os.path.join(midi_directory, midi_file), os.path.join(csv_directory, "temp.csv")])

    f = open(os.path.join(csv_directory, "song" + str(i) + ".csv"), "w+")
    subprocess.call(["iconv", "-f", "UTF-8", "-t", "UTF-8", "-c", os.path.join(csv_directory, "temp.csv")], stdout=f)
    f.close()
    
    output_files.append("song" + str(i) + ".csv")

print("Created " + str(len(output_files)) + " CSV files")
