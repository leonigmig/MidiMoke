from collections import deque
import climax
from midisync import Tempo
from track import MidiPort, Voice

from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class Loop(object):
    def __init__(self, data, track):
        self.data = data
        self.deque = deque(data)
        self.track = track

    def get_next_event(self):
        try:
            return self.deque.popleft()
        except IndexError:
            self.deque = deque(self.data)
            return self.get_next_event()


def run_sequencer(sequencer):
    sequencer.track.play_note(sequencer.get_next_event())


@climax.command()
@climax.argument('sync_interface', help='the sync interface name to bind to')
@climax.argument('out_interface', help='the out interface name to bind to')
def initialise_event_loop(sync_interface, out_interface):
    print(f"Configured for sync and control from {sync_interface}")
    print(f"Configured to output to {out_interface}")

    out_port = MidiPort(out_interface)

    voice = Voice(out_port)

    tempo = Tempo(120)

    l1 = [60, 61, 60, 62, 72, 74, 73, 71]
    # l2 = [60, 61, 60, 62, 64, 62, 60, 61]

    looper = Loop(l1, voice)

    looping_call = LoopingCall(run_sequencer, looper)
    looping_call.start(tempo.get_beat_duration())

    # Start the event loop
    reactor.run()


if __name__ == '__main__':
    initialise_event_loop()
