import climax
from collections import deque
from midisync import Tempo

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import time



def run_sequencer(sequencer):
    print("Running sequencer")


@climax.command()
@climax.argument('interface_name', help='the interface name to bind to')
def initialise_event_loop(interface_name):
    print(f"Configured to sync from {interface_name}")

    tempo = Tempo(120)

    looping_call = LoopingCall(run_sequencer, None)
    looping_call.start(tempo.get_beat_duration())

    # Start the event loop
    reactor.run()
    





if __name__ == '__main__':
    initialise_event_loop()

