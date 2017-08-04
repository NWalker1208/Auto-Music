#!/usr/bin/python3
import os
import csv

def clamp(n, minn, maxn):
    return min(max(n, minn), maxn)

script_location = os.path.dirname(__file__)

csv_directory = os.path.join(script_location, "../csv-files")

input_filename = os.path.join(script_location, "../input/simple.txt")
output_filename = os.path.join(csv_directory, "autoMusic.csv")

# Opening the file with w+ mode truncates the file
with open(output_filename, "w+") as out:
    output_csv = csv.writer(out, quotechar = "'", lineterminator = "\n")

    # Header 
    output_csv.writerow(["0", " 0", " Header", " 1", " 1", " 480"])
    output_csv.writerow(["1", " 0", " Start_track"])
    #output_csv.writerow(["1", " 0", " Time_signature", " 2", " 2", " 24", " 8"])
    #output_csv.writerow(["1", " 0", " Key_signature", " 0", " \"major\""])
    #output_csv.writerow(["1", " 0", " Tempo", " 400000"])
    output_csv.writerow(["1", " 0", " MIDI_port", " 0"])

    totalTime = 0
    
    with open(input_filename, "r") as simple:
        simple_csv = csv.reader(simple)

        i = 0
        for event in simple_csv:
            i += 1
            if len(event) == 4:
                try:
                    track = 1
                    totalTime += int(event[0])
                    time = totalTime
                    active = event[2] == "1"
                    channel = 0
                    note = ord(event[1])
                    velocity = clamp(int(event[3]), 0, 127)

                    if active:
                        output_csv.writerow([str(track), ' ' + str(time), ' Note_on_c', ' ' + str(channel), ' ' + str(note), ' ' + str(velocity)])
                    else:
                        output_csv.writerow([str(track), ' ' + str(time), ' Note_off_c', ' ' + str(channel), ' ' + str(note), ' ' + str(velocity)])                    
                except (ValueError, TypeError):
                    print("Found faulty note, skipping...")
                except:
                    print("Unexpected error occurred on event number " + str(i))
                    raise
                
        simple.close()

    totalTime += 1

    output_csv.writerow(["1", ' ' + str(totalTime), " End_track"])
    output_csv.writerow(["0", " 0", " End_of_file"])

    out.close()
    print("Finished generating complexified CSV that is ready for conversion to MIDI")

        
