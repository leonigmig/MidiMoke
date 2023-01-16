Simple sequencer
----------------

Just a simple event based sequencer

- **Movement**: Overall collection of voices and polyphonic patterns, responsible for dynamically repeating, muting and varying the patterns according to a movement structure, pitch space, and motive rhythm it contains.
    - **Form**: The overall structure of the movement, it defines how the movement repeats, mutates and varies the patterns in each voice
        - **Pitch space**: The range of pitches used in the movement
        - **Motive rhythm**: The rhythm of the movement
    - **Voice**: For example, rhythm, bassline, arpeggiated line, evolving pad, acid line, lead melody etc.
    - **Pattern**: Polyphonic sequence of notes that make up a melody, harmony or rhythm through time
        - **Note**: Single pitch and duration represented in a movement
            - Pitch: The high or low quality of a musical sound
            - Duration: The length of time a musical note is held for (in ticks)

- **Player**: The traversal of a movement to produce music. Responsible for sending the notes and keeping track of how many ticks to sleep in between.
    - **MIDI Port**: The port used to send the notes to the synthesizers
    - **Ticks**: The unit of time used to measure duration in a movement
    - **Wait**: The amount of time the player pauses between emitting notes, when traversing the movement.

Note: The whole structure is immutable, it means the structure once defined cannot be changed.





   
