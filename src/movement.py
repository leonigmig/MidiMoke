# from functools import partial, reduce


def make_movement(pattern_1, pattern_2, length=float("inf")):
    def movement(tick):
        nonlocal pattern_1, pattern_2, length
        if tick > length:
            return None, None

        pattern_1.processEventList()
        notes = []
        for item in pattern_1.MIDIEventList:
            if item.tick == tick:
                notes.append(item)
        return notes, 1

    return movement
