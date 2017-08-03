<h1>Auto-Music</h1>
This is a set of scripts I wrote to compile multiple MIDI files into a single, simplified text file that a machine learning script can use. The MIDI files and the MIDICSV program have been gitignored to prevent potential copyright issues. Also, the scripts are only written to run on Linux.

<h2>Setup</h2>
In order for the scripts to run, a copy of the MIDICSV software must be put inside the "midicsv" folder. You can find that software <a href="http://www.fourmilab.ch/webtools/midicsv/">here</a>. In addition, one or more MIDI files should be placed inside the "midi-files" folder. Avoid using MIDI files with more than one track, as I haven't developed the scripts to include any more than one track in the end product.

<h2>Usage</h2>
Once MIDI files have been placed in the correct folder, you can execute the file "midi2simple", which will create the file "simple.txt" inside the output folder. Use this to train a neural network or other machine learning script.
After getting a sample from a machine learning algorythm, name the sample "simple.txt" and place it into the input folder. Then run the file "simple2midi". This will generate a MIDI file in the output folder.
