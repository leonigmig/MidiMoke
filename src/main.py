from collections import deque
import climax
from rich import print
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
@climax.argument('sync_port', help='the sync port name to bind to')
@climax.argument('out_port', help='the out port name to bind to')
def initialise_event_loop(sync_port, out_port):
    print("[italic blue]Running[/italic blue] 🦋✨")
    print(f"Sync and control port: {sync_port}")
    print(f"Output port: {out_port}")

    tempo = Tempo(120)
    out_port = MidiPort(out_port)

    voice = Voice(out_port)

    l1 = [60, 61, 60, 62, 72, 74, 73, 71]
    # l2 = [60, 61, 60, 62, 64, 62, 60, 61]

    looper = Loop(l1, voice)

    looping_call = LoopingCall(run_sequencer, looper)
    looping_call.start(tempo.get_beat_duration())

    # Start the event loop
    reactor.run()


if __name__ == '__main__':
    initialise_event_loop()
