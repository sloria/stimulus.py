#!/usr/bin/env python
'''A basic example script showing how to display text, wait for a key press, 
and pause at a blank screen.

This file can be executed in the Psychopy Coder window.
'''
from stimulus import Paradigm, Text, WaitForKey, Pause

def main():
    # Initialize a paradigm
    par = Paradigm(window_dimensions=(720, 480))
    # Create a list of stimuli in the order they will show up
    # Each stimuli is added as a tuple of the form (StimulusClass, (arguments))
    stimuli = [
                (Text, ('This text will disappear in 5 seconds. '
                        'Then press the "c" key to continue ', 5.0)),
                (WaitForKey, (['c'], 'continue')),
                (Text, ("Here's some more text", )),  # duration defaults to 2 sec
                # You can also specify keyword arguments in a dictionary
                (Text, 
                    {'text': 'This text will display for 5 seconds',
                    'duration': 5.0}),
                (Text, ('Nice! There will be a 2 second pause '
                        'after this disappears, then an exit.', 4.0)),
                (Pause, (2,))
             ]
    par.add_stimuli(stimuli)  # Add the stimuli
    par.play_all() # Play all stimuli. Press escape to quit 

if __name__ == '__main__':
    main()