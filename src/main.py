from collections import deque
import climax
from midisync import Tempo

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
@climax.argument('interface_name', help='the interface name to bind to')
def initialise_event_loop(interface_name):
    print(f"Configured to sync from {interface_name}")

    tempo = Tempo(120)

    looper = Loop(["C", "D", "C", "G"])

    looping_call = LoopingCall(run_sequencer, looper)
    looping_call.start(tempo.get_beat_duration())

    # Start the event loop
    reactor.run()


if __name__ == '__main__':
    initialise_event_loop()
