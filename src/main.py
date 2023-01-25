import sys

from rich.logging import RichHandler
import climax as shell
import logging

from midisync import Tempo
from movement import make_movement
from midiport import MidiPort
from pattern import Pattern
from player import Player


def make_test_pattern():
    """Or demo pattern.
    """
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
    """Core time loop for playing a movement.
    """

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
        log(e)
        log("That's enough of that!")


def init_logging():
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    return logging.getLogger(__name__)


log = init_logging()


@shell.command()
@shell.argument('midi_in', help='transport, sync, event midi port to bind to')
@shell.argument('midi_out', help='primary midi output bus for notes, events')
def initialise_event_loop(midi_in, midi_out):
    """Connect to MIDI, prepare access to device hardware clock,
    load movement and app settings from configuration then play.
    """

    log.info("✨🦋 MIDI Moke alphav0.1 🦋")

    bpm = Tempo(120)
    out = MidiPort(midi_out)

    play_at_this_speed_to_this_midibus(bpm, out)


if __name__ == '__main__':
    initialise_event_loop()
