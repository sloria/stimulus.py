# -*- coding: utf-8 -*-
"""Classes that make it easy to create and present a series of 
Psychopy stimuli.
"""
import os
import time
from inspect import ismethod

from psychopy import core, visual, sound, event, logging

class Paradigm(object):
    """Represents a study paradigm.
    """
    def __init__(self, window_dimensions=(720, 480), 
                        color='Black', escape_key=None, 
                        dataset=None, format="csv",
                        destination="data.csv",
                        unique=False,
                        *args, **kwargs):
        '''Initialize a paradigm.

        Arguments:
        window_dimensions - The dimensions of the Psychopy window object. 
                            Use 'full_screen' to make a full screen paradigm.
        escape_key - The keyboard button that exits the paradigm.
        dataset - An instance of tablib.Dataset. Data is stored
                        by calling the get_data() method of each stimulus in the 
                        paradigm, if the stimulus has and get_data() method.
        format - What format to save the data. Can be one of ("csv", "json",
                    "xlsx", or "yaml").
        destination - Where to save the data. Defaults to data-[timestamp].csv.
        unique - Whether or not to use a timestamp (epoch) as a unique identifier
                    for a dataset file.
        '''
        if window_dimensions in ['full_screen', 'fullscr']:
            self.window = visual.Window(fullscr=True, 
                                        color=color, units='norm', *args, **kwargs)
        else:
            self.window = visual.Window(window_dimensions, 
                                        color=color, units='norm', *args, **kwargs)

        # List of stimuli for this study
        self.stimuli = []
        self.escape_key = escape_key
        self.dataset = dataset
        if format.lower() in ['csv', 'json', 'yaml', 'xlsx']:
            self.format = format.lower()
        else:
            raise ValueError, "Unsupported data format '{0}'".format(format)
        
        if unique:
            # use epoch time for a unique identifier for saved data files
            suffix = "-" + str(time.time()).replace(".", '')  # Need to remove periods
            fname = suffix.join(os.path.splitext(destination))
        else: 
            fname = destination
        self.destination = fname

        self.stim_idx = 0  # Used to track which stimulus is playing

    def __iter__(self):
        return iter(self.stimuli)

    def add_stimulus(self, stimulus):
        '''Adds a stimulus.

        A stimuli must be a tuple of the form:
            (StimulusType, (arguments))

        Example:
        >> paradigm = Paradigm()
        >> paradigm.add_stimulus( (Text, ('Hi!', 3.0)) )
        '''
        assert type(stimulus) in (tuple, list), 'Stimulus must be a tuple of the form (StimulusType, (arguments))'
        self.stimuli.append(stimulus)

    def add_stimuli(self, stimuli):
        '''Adds multiple stimuli. 

        Args:
        stimuli - A list of stimuli, formatted as tuples
                    (see add_stimulus for how to format stimuli)
        '''
        for stimulus in stimuli:
            self.add_stimulus(stimulus)

    def play_all(self, save_dataset=True, quit=True):
        '''Plays all the stimuli in sequence.
        This simply runs the show() method for each stimuli 
        in self.stimuli, then quits.
        '''
        for stim in self:
            if self.escape_key in event.getKeys():
                break
            self.play_stimulus(stim)

        if save_dataset and self.dataset:
            # Save the data if it exists
            self.write_data()
            logging.info("Saved dataset to {0}".format(self.destination))
        if quit: core.quit()
        logging.info("Finished playing stimuli.")

    def play_next(self):
        '''Plays the next stimuli in the sequence.
        '''
        if len(self.stimuli) > 0:
            stim_data = self.stimuli[self.stim_idx] # The next stimulus tuple
            # Instantiate the stimulus object
            stim = self.initialize_stimulus(stim_data)
            # Show the stimulus
            logging.exp("Showing stimulus {0}: {1}".format(self.stim_idx, stim))
            stim.show()
            self.append_stim_data(stim)
            self.stim_idx += 1
            return stim
        # If there are no more stimuli
        else:
            raise IndexError, "There are no stimuli to be played"
        return None

    def play_stimulus(self, stim):
        '''Plays a stimulus.

        Arguments:
        stim - Either an index or a tuple specificying which stimulus in 
                self.stimuli to play.
        '''
        if type(stim) == int:
            index = stim
            stim_data = self.stimuli[stim]
        elif type(stim) in (list, tuple):
            index = self.stimuli.index(stim)
            stim_data = stim
        else:
            raise ValueError, "'stim' argument must be either an integer, list, or tuple"
        stim = self.initialize_stimulus(stim_data)
        logging.exp("Showing stimulus {0}: {1}".format(index, stim))
        stim.show()
        self.append_stim_data(stim)
        self.stim_idx = index + 1
        return True

    def append_stim_data(self, stim):
        '''Append a stimulus' data to this paradigm's dataset.
        Calls the get_data() method on the stimulus and appends the 
        return value to self.dataset.
        '''
        if has_method(stim, 'get_data'):
            # Append the stimulus' data
            try:
                self.dataset.append(stim.get_data())
                return True
            # If there's no dataset
            except AttributeError:
                pass
        return False

    def write_data(self):
        with open(self.destination, 'wb') as fp:
            if self.format == 'csv':
                fp.write(self.dataset.csv)
            elif self.format == 'json':
                fp.write(self.dataset.json)
            elif self.format == "xlsx":
                fp.write(self.dataset.xlsx)
            else:
                fp.write(self.dataset.yaml)
        return None

    def quit(self):
        core.quit()

    def initialize_stimulus(self, stim_data):
        '''Initialize a stimulus object from a tuple of the form:
            (StimulusType, (arguments)). Keyword arguments may also be
            passed as a dict.

        Args:
        stim_data - The stimulus and its arguments as a tuple
        '''
        stim_class = stim_data[0] # The class of the stimulus
        # Get stim args if passed
        # If not, an empty tuple is passed to the stimulus constructor
        stim_args = stim_data[1] if type(stim_data[1])==tuple else tuple()
        # Get the kwargs if they are passed
        try:
            # the index of the kwargs in stim_data depends on whether 
            # positional args were passed
            stim_kwargs = stim_data[2] if stim_args else stim_data[1]  
        except IndexError:
            # If no kwargs were passed, just pass an empty dict
            stim_kwargs = {}
        return stim_class(self.window, *stim_args, **stim_kwargs)


class Stimulus(object):
    """An abstract stimulus class. All stimulus types will inherit
    from this class.
    """
    index = True

    def __init__(self, window):
        self.window = window

    def show(self):
        '''Show the stimuli. This must be implemented by
        descendant classes.'''
        return self

    def close(self):
        '''Close out.
        '''
        core.quit()

    def flip(self):
        '''Flips the window.
        '''
        self.window.flip()
        return self

class Text(Stimulus):
    '''A text stimulus.
    '''
    def __init__(self, window, text, duration=2.0, 
                keys=None, *args, **kwargs):
        '''Initialize a text stimulus.

        Args:
        window - The window object
        text - text to display
        duration - the duration the text will appear
        keys - list of keys to press to continue to next stimulus. If None, 
                will automatically go to the next stimulus.
        '''
        super(Text, self).__init__(window)
        self.text = visual.TextStim(self.window, 
                        text=text, units='norm',
                        *args, **kwargs)
        self.duration = duration
        self.keys = keys

    def show(self):
        self.draw()
        self.window.flip()
        core.wait(self.duration)
        if self.keys:
            wait_for_key(self.keys)
            self.window.flip()
        else:
            self.window.flip()
        return super(Text, self).show()

    def draw(self):
        self.text.draw()
        return None


class Image(Stimulus):
    '''A simple image stimulus.

    Arguments:
    image - (string) File path of image file.
    text - Optional text to show at the top of the screen.
    keys - (list, optional) Keys used to advance to the next stim.
            If this is specified, the paradigm will pause until one 
            of these keys is pressed by the user.

    Additional args and kwargs are passed to the visual.ImageStim
    constructor.
    '''
    def __init__(self, window,
                    image, duration,
                    text=None, text_size=0.15, units="norm", keys=None,
                    *args, **kwargs):
        super(Image, self).__init__(window)
        self.image = visual.ImageStim(self.window, image=image, *args, **kwargs)
        self.text = visual.TextStim(self.window, 
                                    text=text, 
                                    pos=(0, 0.7), 
                                    height=text_size,
                                    wrapWidth=2.0, # ??
                                    units=units) if text else None
        self.duration = duration
        self.keys = keys

    def show(self):
        self.draw()
        # Show image
        self.window.flip()
        core.wait(self.duration)
        if self.keys:
            # Wait for keypress
            wait_for_key(self.keys)
        # Hide image
        self.window.flip()
        return super(Image, self).show()

    def draw(self):
        self.image.draw()
        if self.text: self.text.draw()
        return None

class Audio(Stimulus):
    '''A simple audio stimulus.'''
    def __init__(self, window,
                    value,
                    text=None,
                    *args, **kwargs):
        '''Constructor for the Audio stimulus.

        Arguments:
        value - A number (pitch in Hz), string for a note,
                or string for a filename.
                For more info, see:
                http://www.psychopy.org/api/sound.html
        text - Text to display on screen (Optional).

        Additional args and kwargs are passed to the 
        sound.Sound constructor.
        '''
        super(Audio, self).__init__(window)
        self.sound = sound.Sound(value, *args, **kwargs)
        self.text = visual.TextStim(self.window, text=text) if text else None

    def show(self):
        if self.text: self.text.draw()
        self.window.flip()
        self.sound.play()
        core.wait(self.sound.getDuration())
        return super(Audio, self).show()

class Video(Stimulus):
    '''A basic video stimulus.
    '''
    def __init__(self, window, movie, movie_dimensions=None, *args, **kwargs):
        '''Constructor for the Video stimulus.

        Arguments:
            movie - A filename (string) for the video file.
            movie_dimensions - Movie dimensions. If not specified, defaults to
                        50\% of the window area.
        '''
        super(Video, self).__init__(window)
        movie_dims = None
        if movie_dimensions:
            movie_dims = movie_dimensions
        else:
            # Default movie to half of the window area
            movie_dims = (self.window.size[0] / 2, self.window.size[1] / 2)
        self.mov = visual.MovieStim(self.window, movie, size=movie_dims,
                                    flipVert=False, loop=False, *args, **kwargs)

    def show(self):
        '''Show the stimulus (movie).
        '''
        while self.mov.status != visual.FINISHED:
            self.mov.draw()
            self.window.update()
        self.window.flip()
        return super(Video, self).show()


class VideoRating(Video):
    '''A stimulus with simultaneous video playback and valence rating (Likert).
    Ratings are saved to a CSV file in where each row is of the format: Rating,Time
    '''
    # labels on either side of the scale.
    def __init__(self, window, movie, destination_path, 
                movie_dimensions=(1, 1), units='norm',
                tick_marks=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                rating_description='Very negative  . . .  Very positive',
                header_text = None,
                header_size=0.15,
                stretch_horizontal=2.7,
                marker_style='triangle', marker_color='White', marker_start=5,
                low=1, high=9, pos=None,
                button_box=None,
                *args, **kwargs):
        
        super(VideoRating, self).__init__(window)
        # FIXME: video should mantain aspect ratio regardless of window dimensions
        self.mov = visual.MovieStim(self.window, 
                                    movie, 
                                    size=movie_dimensions,
                                    units=units,
                                    flipVert=False, 
                                    loop=False)

        # Header text
        if header_text:
            self.header_text = visual.TextStim(self.window, 
                                                text=header_text, 
                                                pos=(0, 0.7), 
                                                height=header_size,
                                                wrapWidth=2.0, # ??
                                                units=units)
        else:
            self.header_text = None

        self.rating_scale = visual.RatingScale(self.window, low=low, high=high, 
                            tickMarks=tick_marks, precision=1,
                            pos=(0, -0.75), stretchHoriz=stretch_horizontal,
                            showAccept=False, acceptKeys=[None],
                            markerStyle=marker_style, markerColor=marker_color,
                            markerStart=marker_start,
                            *args, **kwargs)
        self.rating_scale.setDescription(rating_description)
        # The destination path to write the history to
        self.dest= destination_path
        self.button_box = button_box

    def show(self):
        # Reset the scale
        self.rating_scale.reset()
        # Start the rating at 5
        # Show and update until the movie is done
        while self.mov.status != visual.FINISHED:
            if self.button_box:
                self.button_box.getEvents(returnRaw=True, asKeys=True)
                self.button_box.clearBuffer()
            self.draw()
            self.window.flip()
        # Write the history to a csv
        self.write_history()
        return super(VideoRating, self).show()

    def draw(self):
        self.mov.draw()
        self.rating_scale.draw()
        if self.header_text: self.header_text.draw()
        return None

    def write_history(self):
        '''Writes the rating history data to a CSV file 
        at the specified destination path.
        '''
        rating_history = self.rating_scale.getHistory()
        if len(rating_history) > 0:
            logging.info("Writing rating history...")
            with open(self.dest, 'w') as history_file:
                # Write header
                history_file.write('Rating,Time\n')
                for i, evt in enumerate(rating_history):
                    # Skip the (None, 0.0) event
                    if i == 0:
                        continue
                    # Write data
                    rating, time = evt
                    row = "{0},{1}\n".format(rating, round(time, 8))  # e.g. "3, 2.524"
                    history_file.write(row)
            logging.info("Wrote to {0}".format(self.dest))
        else:
            logging.info("Rating history is empty. Nothing written")


class Pause(Stimulus):
    '''A simple pause.
    '''
    def __init__(self, window, duration):
        super(Pause, self).__init__(window)
        self.duration = float(duration)

    def show(self):
        core.wait(self.duration)
        return super(Pause, self).show()


class WaitForKey(Stimulus):
    '''Wait for a keypress.'''
    def __init__(self, window, keys, event='continue'):
        '''Initialize the stimulus.

        Args:
        keys - A list of keys to wait for.
        event - The event to be triggered when one of the 
                keys is pressed. Can be 'exit' or 'continue'.
                Defaults to 'continue'.
        '''
        super(WaitForKey, self).__init__(window)
        self.keys = keys
        self.event = event

    def show(self):
        wait_for_key(self.keys)
        self.run_event()
        return super(WaitForKey, self).show()

    def run_event(self):
        if self.event == 'exit':
            logging.info("Exiting. . .")
            self.window.close()
            core.quit()
        if self.event in ['nothing', 'continue']:
            pass
        else:
            logging.warn("Event not recognized. Doing nothing.")

def wait_for_key(keys):
    '''Wait for a key that is in a set of keys
    to be pressed before proceeding.

    Args:
    keys - A list or tuple of keys.
    '''
    event.clearEvents()
    if keys:
        if any(keys):
            ret = event.waitKeys(keyList=keys)
        else:
            ret = event.waitKeys()
    return ret

def has_method(obj, method_name):
    '''Utility method that checks if an object has a method bound to it.
    '''
    return hasattr(obj, 'get_data') and ismethod(getattr(obj, 'get_data'))
