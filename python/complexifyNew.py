#!/usr/bin/python3
import os
import subprocess
import csv
import operator

def clamp(n, minn, maxn):
    return min(max(n, minn), maxn)

script_location = os.path.dirname(__file__)

csv_directory = os.path.join(script_location, "../csv-files")

input_filename = os.path.join(script_location, "../input/simple.txt")
output_filename = os.path.join(csv_directory, "autoMusic.csv")

note_time_limit = 5000

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

    total_time = 0

    f = open(os.path.join(csv_directory, "temp.csv"), "w+")
    subprocess.call(["iconv", "-f", "UTF-8", "-t", "UTF-8", "-c", input_filename], stdout=f)
    f.close()
    
    with open(os.path.join(csv_directory, "temp.csv"), "r") as simple:
        simple_csv = csv.reader(simple, lineterminator = "\n")

        allEvents = []
        
        i = 0
        for keyPress in simple_csv:
            i += 1
            if len(keyPress) == 4:
                old_total_time = total_time
                try:
                    track = 1
                    total_time += int(event[0])
                    time = total_time
                    length = int(event[2])
                    channel = 0
                    note = ord(event[1][0]) - 128
                    velocity = clamp(int(event[3]), 0, 127)

                    assert note > -1 and note < 128

                    allEvents.append({"track": track, "time": time, "active": True, "channel": 0, "note": note, "velocity": velocity})
                        
                    if active:
                        if not note in active_notes:
                            output_csv.writerow([str(track), ' ' + str(time), ' Note_on_c', ' ' + str(channel), ' ' + str(note), ' ' + str(velocity)])
                    else:
                        if note in active_notes:
                            output_csv.writerow([str(track), ' ' + str(time), ' Note_off_c', ' ' + str(channel), ' ' + str(note), ' ' + str(0)])

                    event_count += 1                 
                except (ValueError, TypeError, IndexError):
                    total_time = old_total_time
                    print("Found faulty event, skipping...")
                except AssertionError:
                    total_time = old_total_time
                    print("Found faulty event (note out of range), skipping...")
                except:
                    print("Unexpected error occurred on event number " + str(i))
                    raise
                
        

                
        simple.close()

    total_time += 1

    output_csv.writerow(["1", ' ' + str(total_time), " End_track"])
    output_csv.writerow(["0", " 0", " End_of_file"])

    out.close()
    print("Finished generating complexified CSV that is ready for conversion to MIDI")

        
