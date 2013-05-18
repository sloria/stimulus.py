# stimulus.py 

stimulus.py implements wrapper classes for [PsychoPy](http://www.psychopy.org/) stimuli, allowing for a consistent and easy-to-use API for presenting a study paradigm.

Currently supported stimulus types: 
* Text
* VideoStimulus
* VideoRatingStimulus
* Pause
* WaitForKey
* WaitForTTL

More to come. 

Example usage (also in `paradigm_example.py`):

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

## Defining new stimulus types
It's easy to create your own custom stimulus types. Just create a subclass of `Stimulus` and implement its `__init__` and `show()` methods. Make sure to set the `window` instance variable in the constructor.

Example:

```python
from psychopy import core, visual
from stimulus import Stimulus, Paradigm

class HelloWorldStim(Stimulus):
    """A stimulus that just shows "Hello, World!" in green."""
    def __init__(self, window, duration=2.0):
        self.window = window
        self.text = visual.TextStim(self.window, 
                        text="Hello, World!", color="Green")
        self.duration = duration

    def show(self):
        self.text.draw()
        self.window.flip()
        core.wait(self.duration)

# Now you can use it!
par = Paradigm()
hello = (HelloWorldStim, (5.0,))
par.add_stimulus(hello)
par.play_all()
```
