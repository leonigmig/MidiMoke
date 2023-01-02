import climax
from collections import deque
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import time

def my_callback(arg1, arg2):
  print(arg1, arg2)


def run_sequencer(sequencer):
    print("Running sequencer")


@climax.command()
@climax.argument('interface_name', help='the interface name to bind to')
def initialise_event_loop(interface_name):
    print(f"Configured to sync from {interface_name}")

    looping_call = LoopingCall(run_sequencer, None)
    looping_call.start(1.0)

    reactor.callLater(5, my_callback, "Hello", "world")
    # Start the event loop
    reactor.run()
    





if __name__ == '__main__':
    initialise_event_loop()

