from collections import deque
import climax
from midisync import Tempo
from track import MidiPlayer

from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class Loop(object):
    def __init__(self, data):
        self.data = data
        self.deque = deque(data)

    def get_next_event(self):
        try:
            return self.deque.popleft()
        except IndexError:
            self.deque = deque(self.data)
            return self.get_next_event()


def run_sequencer(sequencer):
    print(sequencer.get_next_event())


@climax.command()
@climax.argument('sync_interface', help='the sync interface name to bind to')
@climax.argument('out_interface', help='the out interface name to bind to')
def initialise_event_loop(sync_interface, out_interface):
    print(f"Configured for sync and control from {sync_interface}")
    print(f"Configured to output to {out_interface}")

    track = MidiPlayer(out_interface)
    while (True):
        track.play_note(60)
    return

    tempo = Tempo(120)

    looper = Loop(["C4", "G4", "C5", "F5"])

    looping_call = LoopingCall(run_sequencer, looper)
    looping_call.start(tempo.get_beat_duration())

    # Start the event loop
    reactor.run()


if __name__ == '__main__':
    initialise_event_loop()
