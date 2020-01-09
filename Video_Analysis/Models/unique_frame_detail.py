"""This contain frame detail object"""


class FrameDetail(object):
    """class to create the objects with frame details"""

    def __init__(self, frame_position, title_availability, title, content_availability, content, figure, timestamp):
        self.frame_position = frame_position
        self.title_availability = title_availability
        self.title = title
        self.content_availability = content_availability
        self.content = content
        self.figure = figure
        self.timestamp = timestamp
