# REPORT

## Personal Information
- Student Name: Arshad Momin    
- Student ID: 20986176
- WatID: a5momin

## What have been done to compile and run the code
Created build folder in the docker 'fb' directory and followed the instructions.
## What have been done to increase the coverage
Using the Freedoom.wad which has been fed to the SEED folder. This will map thee input from wad file such as sound, gui,etc. and generate the input file in CORPUS directory in build. The function which looks for '~' in the file name makes it clear that this function was not covered. Therefore changed the file name with intially to be '~'.  Also used 'use_value_profile' while running the jobs and enabled the sound,gui,fx,music,etc.
## What bugs have been found? Can you replay the bug with chocolate-doom, not with the fuzz target?
## Did you manage to compile the game and play it on your local machine (Not inside Docker)?
Installed Chocolate-doom and then using "freedoom2.wad" the wad file gets fed and installed to make it easy to run and play the game.