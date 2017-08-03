#!/usr/bin/python3
import os
import csv

script_location = os.path.dirname(__file__)

csv_directory = os.path.join(script_location, "../csv-files")

output_filename = os.path.join(script_location, "../output/simple.txt")

# opening the file with w+ mode truncates the file
with open(output_filename, "w+") as out:
    output_csv = csv.writer(out)

    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv") and filename.startswith("song"): 
            # Process file
            with open(os.path.join(csv_directory, filename)) as song:
                songCSV = csv.reader(song)

                lastEventTime = 0

                #print("Opened " + filename + " with " + str(len(song.readlines())) + " events")
                for event in songCSV:
                    if (event[2][1:] == "Note_on_c" or event[2][1:] == "Note_off_c") and event[0] == "1":
                    
                        track = int(event[0])
                        time = int(event[1][1:])
                        active = event[2][1:] == "Note_on_c"
                        channel = int(event[3][1:])
                        note = int(event[4][1:])
                        velocity = int(event[5][1:])
    
                        if active:
                            output_csv.writerow([str(time - lastEventTime), chr(note), "1", str(velocity)])
                        else:
                            output_csv.writerow([str(time - lastEventTime), chr(note), "0", str(velocity)])
                                        
                        lastEventTime = time

                song.close()
        
            continue
        else:
            continue
    
    out.close()
    print("Finished compiling simplified text file that is ready for use in neural network training (simple.txt)")


