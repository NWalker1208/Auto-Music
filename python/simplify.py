#!/usr/bin/python3
import os
import csv
from operator import itemgetter

script_location = os.path.dirname(__file__)

csv_directory = os.path.join(script_location, '../csv-files')

output_filename = os.path.join(script_location, '../output/simple.txt')

# opening the file with w+ mode truncates the file
with open(output_filename, 'w+') as out:
    output_csv = csv.writer(out, lineterminator = "\n")

    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv') and filename.startswith('song'): 
            # Process file
            with open(os.path.join(csv_directory, filename)) as song:
                songCSV = csv.reader(song, lineterminator = "\n")

                # Grab all events from all tracks
                allEvents = []

                for event in songCSV:
                    if (event[2][1:] == 'Note_on_c' or event[2][1:] == 'Note_off_c'):
                        track = int(event[0])
                        time = int(event[1][1:])
                        channel = int(event[3][1:])
                        note = int(event[4][1:])
                        velocity = int(event[5][1:])
                        active = (event[2][1:] == 'Note_on_c') and (velocity > 0)

                        allEvents.append({'time': time, 'active': active, 'note': note, 'velocity': velocity})

                song.close()
                
                # Sort events by timestamp
                allEvents = sorted(allEvents, key=itemgetter('time'))
                
                # Convert events into keypresses with time lengths
                keyPresses = []
                activeKeys = {}
                
                for event in allEvents:
                    if event['active']:
                        activeKeys[event['note']] = {'time': event['time'], 'velocity': event['velocity']}
                    elif event['note'] in activeKeys:
                        keyPresses.append({'time': activeKeys[event['note']]['time'], 'length': (event['time'] - activeKeys[event['note']]['time']), 'note': event['note'], 'velocity': activeKeys[event['note']]['velocity']})
                        del activeKeys[event['note']]

                # Sort keypresses by timestamp
                keyPresses = sorted(keyPresses, key=itemgetter('time'))
                
                # Simply events and add to text file in order of time stamp
                lastEventTime = 0
                for keyPress in keyPresses:
                    output_csv.writerow([str(keyPress['time'] - lastEventTime), chr(keyPress['note'] + 128), str(keyPress['length']), str(keyPress['velocity'])])
                                        
                    lastEventTime = keyPress['time']
        
            continue
        else:
            continue
    
    out.close()
    print('Finished compiling simplified text file that is ready for use in neural network training (simple.txt)')


