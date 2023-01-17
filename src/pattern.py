import struct


class GenericEvent(object):
    '''
    The event class from which specific events are derived
    '''
    evtname = None
    sec_sort_order = 0

    def __init__(self, tick, insertion_order):
        self.tick = tick
        self.insertion_order = insertion_order

    def __eq__(self, other):
        '''
        Equality operator.
        In the processing of the event list, we have need to remove duplicates.
        To do this we rely on the fact that the classes are hashable, and must
        therefore have an equality operator (__hash__() and __eq__() must both
        be defined).
        Some derived classes will need to override and consider their specific
        attributes in the comparison.
        '''
        return (self.evtname == other.evtname and self.tick == other.tick)

    def __hash__(self):
        '''
        Return a hash code for the object.
        This is needed in order to allow GenericObject classes to be used
        as the key in a dict or set. duplicate objects are removed from
        the event list by storing all the objects in a set, and then
        reconstructing the list from the set.  The only real requirement
        for the algorithm is that the hash of equal objects must be equal.
        There is probably great opportunity for improvements in the hashing
        function.
        '''
        # Robert Jenkin's 32 bit hash.
        a = int(self.tick)
        a = (a + 0x7ed55d16) + (a << 12)
        a = (a ^ 0xc761c23c) ^ (a >> 19)
        a = (a + 0x165667b1) + (a << 5)
        a = (a + 0xd3a2646c) ^ (a << 9)
        a = (a + 0xfd7046c5) + (a << 3)
        a = (a ^ 0xb55a4f09) ^ (a >> 16)
        return a


def sort_events(event):
    '''
    .. py:function:: sort_events(event)

        The key function used to sort events (both MIDI and Generic)

        :param event: An object of type :class:`MIDIEvent` or (a derrivative)
            :class:`GenericEvent`

        This function should be provided as the ``key`` for both
        ``list.sort()`` and ``sorted()``. By using it sorting will be as
        follows:

        * Events are ordered in time. An event that takes place earlier will
          appear earlier
        * If two events happen at the same time, the secondary sort key is
          ``sec_sort_order``. Thus a class of events can be processed earlier
          than another. One place this is used in the code is to make sure that
          note off events are processed before note on events.
        * If event time and event ordinality are the same, they are sorted in
          the order in which they were originally added to the list. Thus, for
          example, if one is making an RPN call one can specify the controller
          change events in the proper order and be sure that they will end up
           in
          the file that way.
    '''

    return (event.tick, event.sec_sort_order, event.insertion_order)


def writeVarLength(i):
    '''
    Accept an integer, and serialize it as a MIDI file variable length quantity
    Some numbers in MTrk chunks are represented in a form called a variable-
    length quantity.  These numbers are represented in a sequence of bytes,
    each byte holding seven bits of the number, and ordered most significant
    bits first. All bytes in the sequence except the last have bit 7 set,
    and the last byte has bit 7 clear.  This form allows smaller numbers to
    be stored in fewer bytes.  For example, if the number is between 0 and
    127, it is thus represented exactly as one byte.  A number between 128
    and 16383 uses two bytes, and so on.
    Examples:
    Number  VLQ
    128     81 00
    8192    C0 00
    16383   FF 7F
    16384   81 80 00
    '''
    if i == 0:
        return [0]

    vlbytes = []
    hibit = 0x00  # low-order byte has high bit cleared.
    while i > 0:
        vlbytes.append(((i & 0x7f) | hibit) & 0xff)
        i >>= 7
        hibit = 0x80
    vlbytes.reverse()  # most-significant byte first, least significant last
    return vlbytes


class Pattern():
    def __init__(self):
        '''Initialize the MIDITrack object.
        '''
        self.headerString = struct.pack('cccc', b'M', b'T', b'r', b'k')
        self.dataLength = 0  # Is calculated after the data is in place
        self.MIDIdata = b""
        self.eventList = []
        self.MIDIEventList = []

    def addNoteByNumber(self, channel, pitch, tick, duration, volume,
                        annotation=None, insertion_order=0):
        '''
        Add a note by chromatic MIDI number
        '''
        self.eventList.append(NoteOn(channel, pitch, tick, duration, volume,
                                     annotation=annotation,
                                     insertion_order=insertion_order))

        # This event is not in chronological order. But before writing all the
        # events to the file, I sort self.eventlist on (tick, sec_sort_order,
        #  insertion_order)
        # which puts the events in chronological order.
        self.eventList.append(NoteOff(channel, pitch, tick + duration, volume,
                                      annotation=annotation,
                                      insertion_order=insertion_order))

    def processEventList(self):
        '''
        Process the event list, creating a MIDIEventList,
        which is then sorted to be in chronological order by start tick.
        '''
        self.removeDuplicates()
        self.MIDIEventList = [evt for evt in self.eventList]
        # Assumptions in the code expect the list to be time-sorted.
        self.MIDIEventList.sort(key=sort_events)

    def removeDuplicates(self):
        '''
        Remove duplicates from the eventList.

        This function will remove duplicates from the eventList. This is
        necessary because we the MIDI event stream can become confused
        otherwise.
        '''

        # For this algorithm to work, the events in the eventList must be
        # hashable (that is, they must have a __hash__() and __eq__() function
        # defined).

        s = set(self.eventList)
        self.eventList = list(s)
        self.eventList.sort(key=sort_events)


class NoteOn(GenericEvent):
    '''
    A class that encapsulates a note
    '''
    evtname = 'NoteOn'
    midi_status = 0x90    # 0x9x is Note On
    sec_sort_order = 3

    def __init__(self, channel, pitch, tick, duration, volume,
                 annotation=None, insertion_order=0):
        self.pitch = pitch
        self.duration = duration
        self.volume = volume
        self.channel = channel
        self.annotation = annotation
        super(NoteOn, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.evtname == other.evtname and self.tick == other.tick and
                self.pitch == other.pitch and self.channel == other.channel)

    # In Python 3, a class which overrides __eq__ also needs
    # to provide __hash__,
    # because in Python 3 parent __hash__ is not inherited.
    __hash__ = GenericEvent.__hash__

    def __str__(self):
        return 'NoteOn %d at tick %d duration %d ch %d vel %d' % (
            self.pitch, self.tick, self.duration, self.channel, self.volume)

    def serialize(self, previous_event_tick):
        """Return a bytestring representation of the event, in the format
         required for
        writing into a standard midi file.
        """
        midibytes = b""
        code = self.midi_status | self.channel
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', self.pitch)
        midibytes += struct.pack('>B', self.volume)
        return midibytes


class NoteOff (GenericEvent):
    '''
    A class that encapsulates a Note Off event
    '''
    evtname = 'NoteOff'
    midi_status = 0x80  # 0x8x is Note Off
    sec_sort_order = 2  # must be less than that of NoteOn
    # If two events happen at the same time, the secondary sort key is
    # ``sec_sort_order``. Thus a class of events can be processed earlier than
    # another. One place this is used in the code is to make sure that note
    # off events are processed before note on events.

    def __init__(self, channel, pitch, tick, volume,
                 annotation=None, insertion_order=0):
        self.pitch = pitch
        self.volume = volume
        self.channel = channel
        self.annotation = annotation
        super(NoteOff, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.evtname == other.evtname and self.tick == other.tick and
                self.pitch == other.pitch and self.channel == other.channel)

    __hash__ = GenericEvent.__hash__

    def __str__(self):
        return 'NoteOff %d at tick %d ch %d vel %d' % (
            self.pitch, self.tick, self.channel, self.volume)

    def serialize(self, previous_event_tick):
        """Return a bytestring representation of the event, in the format
         required for
        writing into a standard midi file.
        """
        midibytes = b""
        code = self.midi_status | self.channel
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', self.pitch)
        midibytes += struct.pack('>B', self.volume)
        return midibytes
