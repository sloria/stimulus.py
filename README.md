# stimulus.py 

stimulus.py implements wrapper classes for Psychopy stimuli, allowing for a consistent and easy-to-use API for presenting a study paradigm.

Example (also in `paradigm_example.py`):

```python
from stimulus import Paradigm, Text, WaitForKey, Pause    

# Initialize a paradigm
par = Paradigm(window_dimensions=(720, 480))
# Create a list of stimuli in the order they will show up
# Each stimuli is added as a tuple of the form (StimulusClass, (arguments))
stimuli = [
            (Text, ('This text will disappear in 5 seconds. '
                    'Then press any key at the blank screen to continue '
                    'or press "q" to quit.', 5.0)),
            (WaitForKey, (['q'], 'exit')),
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
```

