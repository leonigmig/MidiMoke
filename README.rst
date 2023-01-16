Simple sequencer
----------------

Just a simple event based sequencer implemented in a pure Python functional style, following functional idioms where possible and using a functional / object oriented hybrid programming paradigm. For example data structures are immutable, so once defined cannot be changed.

Player
======

..  code-block:: Python

    notes, ticks_to_wait = play(movement, midi_port)

- **Player**: The traversal of a movement to produce music. Responsible for sending the notes and keeping track of how many ticks to sleep in between.
    - **MIDI Port**: The port used to send the notes to the synthesizers
    
    - **Wait**: The amount of time the player pauses between emitting notes, when traversing the movement.

Movement
========

- **Movement**: Overall collection of voices and polyphonic patterns, responsible for dynamically repeating, muting and varying the patterns according to a movement structure, pitch space, and motive rhythm it contains.
    - **Form**: The overall structure of the movement, it defines how the movement repeats, mutates and varies the patterns in each voice
        - **Pitch space**: The range of pitches used in the movement
        - **Motive rhythm**: The rhythm of the movement
    - **Voice**: For example, rhythm, bassline, arpeggiated line, evolving pad, acid line, lead melody etc.
    - **Pattern**: Polyphonic sequence of notes that make up a melody, harmony or rhythm through time
        - **Note**: Single pitch and duration represented in a movement
            - Pitch: The high or low quality of a musical sound
            - Duration: The length of time a musical note is held for (in ticks)


Ticks
=====

Ticks are the fundamental unit of time used to measure duration in a movement. 

- **Second**: Just the common or garden notion of seconds implemented by the device clock.
    - **Minute**: Just the common or garden notion of minutes which is 60 seconds.
    - **BPM**: The amount of beats per minute for the movement to be played at. The tempo.
- **Beat**: A regular pulse for the movement, which aligns to Lerdahl and Jackendoff's notion of tactus.
    - **Ticks**: The unit of time used to measure duration in a movement
    - **Ticks per beat**: The amount of ticks per beat 

- **Wait per tick**: The time in seconds that the player should wait for each tick, determined by the BPM and ticks per beat.
- **Tick delta**: The amount of ticks that the player should wait until the next note or set of notes in the movement needs to be emitted

   
