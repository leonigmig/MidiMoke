import climax
from collections import deque
from twisted.internet import reactor
import time

def my_callback(arg1, arg2):
  print(arg1, arg2)

@climax.command()
@climax.argument('interface_name', help='the interface name to bind to')
def initialise_event_loop(interface_name):
    print(f"Looking for {interface_name}")

    # Schedule the callback to be called in 5 seconds
    reactor.callLater(5, my_callback, "Hello", "world")
    # Start the event loop
    reactor.run()
    

    try:
        midi_device, port_name = open_midiinput(2)
        print(port_name)
    except (EOFError, KeyboardInterrupt):
        return 1

    midi_dispatcher = MIDIDispatcher()
    midi_device.set_callback(midi_dispatcher)
    midi_device.ignore_types(timing=False)

    try:
        print("Waiting for clock sync...")
        while True:
            time.sleep(1)

            if midi_dispatcher.running:
                if midi_dispatcher.sync:
                    print("%.2f bpm" % midi_dispatcher.bpm)
                else:
                    print("%.2f bpm (no sync)" % midi_dispatcher.bpm)

    except KeyboardInterrupt:
        pass
    finally:
        midi_device.close_port()
        del midi_device


from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START, SONG_STOP)
from rtmidi.midiutil import open_midiinput

class MIDIDispatcher:
    def __init__(self, bpm=None):
        self.bpm = bpm if bpm is not None else 120.0
        self.sync = False
        self.running = True
        self._samples = deque()
        self._last_clock = None

    def __call__(self, event, data=None):
        msg, _ = event

        if msg[0] == TIMING_CLOCK:
            now = time.time()

            if self._last_clock is not None:
                self._samples.append(now - self._last_clock)

            self._last_clock = now

            if len(self._samples) > 24:
                self._samples.popleft()

            if len(self._samples) >= 2:
                self.bpm = 2.5 / (sum(self._samples) / len(self._samples))
                self.sync = True

        elif msg[0] in (SONG_CONTINUE, SONG_START):
            self.running = True
            print("START/CONTINUE received.")
        elif msg[0] == SONG_STOP:
            self.running = False
            print("STOP received.")


if __name__ == '__main__':
    initialise_event_loop()

