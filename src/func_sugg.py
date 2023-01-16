import time
# from functools import partial, reduce


def play_song(song_func, state, tick=0):
    """
    A higher-order function that plays the song by calling the song_func with
    the current tick and state
    """
    if tick >= state["end_tick"]:
        return
    note, new_state = song_func(tick, state)
    print("tick:", tick)
    print("Playing note:", note)
    time.sleep(note["duration"])
    play_song(song_func, new_state, tick + 1)


def make_movement(voice_1, voice_2, length=float("inf")):
    def song_closure(tick):
        if tick >= length:
            return None, None

        return 1, 1

    return song_closure


def song(tick, state):
    """
    A recursive function that represents the song. It takes a current tick and
     state as parameters and returns the next note to play
    """
    if tick >= state["end_tick"]:
        return None

    current_note = state["notes"][tick % len(state["notes"])]
    new_state = {"end_tick": state["end_tick"], "notes": state["notes"]}
    return {"pitch": current_note["pitch"],
            "duration": current_note["duration"]}, new_state


# Define the notes and structure of the song
notes = [
    {"pitch": 60, "duration": 0.5},
    {"pitch": 62, "duration": 0.5},
]

# song_state = {"end_tick": float("inf"), "notes": notes}
song_state = {"end_tick": 4, "notes": notes}

# play the song
# play_song(song, song_state)
