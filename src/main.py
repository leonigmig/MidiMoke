import climax
from rich import print
from midisync import Tempo
from movement import make_movement
from pattern import Pattern
from midiport import MidiPort
from player import Player


@climax.command()
@climax.argument('sync_port', help='the sync port name to bind to')
@climax.argument('out_port', help='the out port name to bind to')
def initialise_event_loop(sync_port, out_port):
    print("[italic blue]Running[/italic blue] 🦋✨")
    print(f"Sync and control port: {sync_port}")
    print(f"Output port: {out_port}")

    tempo = Tempo(120)
    out_port = MidiPort(out_port)

    pattern_1 = Pattern()
    pattern_1.addNote(
        pitch=60, tick=1, duration=1, volume=100)
    pattern_1.addNote(
        pitch=60, tick=2, duration=1, volume=100)
    pattern_1.addNote(
        pitch=64, tick=1, duration=1, volume=100)
    pattern_1.addNote(
        pitch=64, tick=2, duration=2, volume=100)

    movement = make_movement(pattern_1, 3)

    player = Player(tempo, movement, out_port)

    player.play(0)


if __name__ == '__main__':
    initialise_event_loop()
