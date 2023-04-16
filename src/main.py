from rich.logging import RichHandler
import climax as shell
import logging

from mididevice import MidiDevice
from m21 import get_stream
from player import Player


def init_logging():
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    return logging.getLogger(__name__)


log = init_logging()


@shell.command()
@shell.argument('midi_device', help='transport, sync, event midi port to bind to')
def initialise_event_loop(midi_device):
    """
    Configure and initialise the event loop.
    """

    log.info("✨🦋 MIDI Moke - software midi friend - 🦋✨")

    player = Player(
        get_stream(),
        MidiDevice(midi_device)
    )

    player.start()


if __name__ == '__main__':
    initialise_event_loop()   # type: ignore
