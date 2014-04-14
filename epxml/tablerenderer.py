import os
import sys


class Room(object):

    def __init__(self, room_id, room_name):
        self.id = room_id
        self.name = room_name


class Event(object):

    def __init__(self, event_id, event_name):
        self.id = event_id
        self.name = event_name


class HTMLSchedule(object):

    def __init__(self, rooms, start=(0, 0), end=(23, 59), resolution=15 ):
        self.rooms = rooms
        self.start_hour, self.start_minute  = map(int, start.split(':'))
        self.end_hour, self.end_minute  = map(int, end.split(':'))
        self.resolution = resolution
        self.events = list()

    def addEvent(self, event, start, end, room):
        if not isinstance(event, Event):
            raise TypeError('"event" must be Event instance')

        self.events.append(dict(event=event,
                                start=start,
                                end=end,
                                room=room))

    def renderTable(self):
        print '<table border="1">'
        print '<thead>'
        print '<tr>'
        print '<th>Time</th>'
        for room in self.rooms:
            print '<th>{}</th>'.format(room.name)
        print '</tr>'
        print '</thead>'
        print '<tbody>'
        for hour in range(self.start_hour, self.end_hour):
            for minute in range(0, 60, self.resolution):
                print '<tr>'
                print '<td>{:02d}:{:02d}</td>'.format(hour, minute)
                for room in self.rooms:
#                    print room.id
                    pass

                print '</tr>'
        print '</tbody>'
        print '</table>'


if __name__ == '__main__':

    rooms = [Room(u'hall', u'Ballroom'), 
             Room(u'meeting1', u'Meeting room1'),
             Room(u'meeting2', u'Meeting room2')]

    schedule = HTMLSchedule(rooms, '08:00', '18:00', 15)
    schedule.addEvent(Event(u'breakfast', u'Breakfast'), '08:00', '09:00', u'hall')
    schedule.addEvent(Event(u'talk1', u'Talk1'), '09:00', '10:00', u'meeting1')
    schedule.addEvent(Event(u'talk2', u'Talk2'), '09:00', '10:00', u'meeting2')

    schedule.renderTable()


