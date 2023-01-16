Simple sequencer
----------------

Just a simple event based sequencer

lets say I want a function that acts as a player which takes a song as a parameter and is responsible for sending midi notes, keeping track of time and sleeping between notes in the song. the song knows which notes to play at any identified tick and is responsible for dynamically repeating, muting and varying the patterns according to a structure, pitch space and motive rhythm it takes as parameters. the patterns can be either pitch patterns or rhythm patterns. the whole structure is immutable. what pure python patterns can i use to compose this software