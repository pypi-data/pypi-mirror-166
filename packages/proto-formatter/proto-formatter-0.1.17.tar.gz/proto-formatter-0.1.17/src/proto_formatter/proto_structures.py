from enum import Enum


class Position(Enum):
    LEFT = 'left'
    Right = 'right'
    TOP = 'top'
    BELOW = 'below'


class Comment:
    def __init__(self, text: str, position: Position):
        self.text = text
        self.position = position


class Syntax:
    def __init__(self, value, comments: list):
        self.value = value
        self.comments = comments


class Package:
    def __init__(self, value, comments: list):
        self.value = value
        self.comments = comments


class Import:
    def __init__(self, value, comments: list):
        self.value = value
        self.comments = comments


class Option:
    def __init__(self, name, value, comments: list):
        self.name = name
        self.value = value
        self.comments = comments


class Element:
    def __init__(self, type, name, number, annotation='', label='', comments=[]):
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class MessageElement:
    def __init__(self, type, name, number, annotation='', label='', comments=[]):
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class Message:
    def __init__(self, name, elements=None, comments=None):
        if elements is None:
            elements = []
        if comments is None:
            comments = []
        self.name = name
        self.elements = elements
        self.comments = comments


class ExtendElement:
    def __init__(self, type, name, number, annotation='', label='', comments=None):
        if comments is None:
            comments = []
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class Extend:
    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []
        self.name = name
        self.elements = elements
        self.comments = comments


class OneofElement:
    def __init__(self, type, name, number, annotation='', label='', comments=None):
        if comments is None:
            comments = []
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class Oneof:
    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []
        self.name = name
        self.elements = elements
        self.comments = comments


class EnumElement:
    def __init__(self, name, number, annotation='', comments=None):
        if comments is None:
            comments = []
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class ProtoEnum:
    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []
        self.name = name
        self.elements = elements
        self.comments = comments


#  rpc SeatAvailability (SeatAvailabilityRequest) returns (SeatAvailabilityResponse);
class ServiceElement:
    def __init__(self, label, name, request, response, comments=None):
        if comments is None:
            comments = []
        self.label = label
        self.name = name
        self.request = request
        self.response = response
        self.comments = comments


class Service:
    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []
        self.name = name
        self.elements = elements
        self.comments = comments
