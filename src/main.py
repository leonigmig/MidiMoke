import sys

from rich import print
import climax

from midisync import Tempo
from movement import make_movement
from pattern import Pattern
from midiport import MidiPort
from player import Player


def make_test_pattern():
    pattern = Pattern()
    pattern.addNote(
        pitch=60, tick=1, duration=1, volume=100)
    pattern.addNote(
        pitch=60, tick=2, duration=1, volume=100)
    pattern.addNote(
        pitch=64, tick=1, duration=1, volume=100)
    pattern.addNote(
        pitch=64, tick=2, duration=2, volume=100)
    pattern.addNote(
        pitch=72, tick=3, duration=1, volume=100)
    return pattern


def play_at_this_speed_to_this_midibus(bpm, out):
    """Core time loop for playing a movement."""

    sys.setrecursionlimit(2000)

    movement = make_movement(make_test_pattern(), 3)
    try:
        player = Player(
            bpm,
            movement,
            out
        )

        player.play(0)

    except RecursionError as e:
        print(e)
        print("That's enough of that!")


@climax.command()
@climax.argument('midi_in', help='transport, sync, event midi port to bind to')
@climax.argument('midi_out', help='primary midi output bus for notes, events')
def initialise_event_loop(midi_in, midi_out):
    """Connect to MIDI, prepare access to device hardware clock,
    load movement and app settings from configuration then play."""

    print("[italic blue]Blue Butterly alphav0.1[/italic blue] 🦋✨")

    bpm = Tempo(120)
    out = MidiPort(midi_out)

    play_at_this_speed_to_this_midibus(bpm, out)


if __name__ == '__main__':
    initialise_event_loop()
