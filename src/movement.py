# from functools import partial, reduce


def make_movement(pattern_1, pattern_2, length=float("inf")):
    def movement(tick):
        nonlocal pattern_1, pattern_2, length
        if tick > length:
            return None, None

        loop_tick = tick % pattern_1.tick_length
        print(loop_tick)
        pattern_1.processEventList()
        notes = []
        for item in pattern_1.MIDIEventList:
            if item.tick == loop_tick:
                notes.append(item)
        return notes, 1

    return movement
