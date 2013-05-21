import unittest
from nose.tools import *

from stimulus import *

class TestStimulus(unittest.TestCase):

    def setUp(self):
        self.par = Paradigm()
        
    def tearDown(self):
        print "TEAR DOWN!"
        
    def _create_stimulus(self, stim_class):
        pass

    def test_text_stim(self):
        text = (Text, ('Hello world!', 5.0))
        text_stim = self.par._initialize_stimulus(text)        
        assert_true(isinstance(text_stim, Text))

if __name__ == '__main__':
    unittest.main()