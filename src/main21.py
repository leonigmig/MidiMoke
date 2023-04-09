import sys

from rich.logging import RichHandler
import climax as shell
import logging

from midiport21 import MidiPort
from m21 import get_stream
from player21 import Player


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
    """
    Configure and initialise the event loop.
    """

    log.info("✨🦋 MIDI Moke alphav0.2 🦋✨")

    midi_port = MidiPort(midi_out)
    sys.setrecursionlimit(2000)

    try:
        player = Player(
            get_stream(),
            midi_port
        )

        player.start()

    except RecursionError as e:
        log(e)
        log("That's enough of that!")


if __name__ == '__main__':
    initialise_event_loop()
