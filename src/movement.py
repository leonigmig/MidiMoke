# from functools import partial, reduce

import logging

from music21 import midi

log = logging.getLogger(__name__)


def make_movement(pattern_1, pattern_2, length=float("inf")):
    """Returns a function that takes a tick and returns a list of events
    to play
    """
    def movement(tick):
        """Returns a list of events to play at a given tick
        """
        nonlocal pattern_1, pattern_2, length

        if tick > length:
            return None, None

        loop_tick = tick % pattern_1.tick_length
        pattern_1.processEventList()
        notes = []
        for item in pattern_1.MIDIEventList:
            if item.tick == loop_tick:
                notes.append(item)

        duration = 1
        log.info("loop tick: %d, played tick: %d, duration: %d",
                 loop_tick, tick, duration)
        return notes, duration

    return movement

def convert_music21_stream(stream):
    # Convert the Music21 stream into a MIDI stream
    midi_stream = midi.translate.streamToMidiFile(stream)

    scaling_factor = 24 / 1024

    result = {}
    tick = 0

    for event in midi_stream.tracks[1].events:
        event.time = round(event.time * scaling_factor)
        if event.isDeltaTime():
            if event.time > 0:
                tick += event.time
        if event.isNoteOn() or event.isNoteOff():
            if tick in result:
                result[tick].append(event)
            else:
                result[tick] = [event]

    return result

