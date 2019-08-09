from .regex import status_regex
import re

class Status(object):
    @staticmethod
    def match(line):
        return re.match(status_regex.encode(), line)
    @staticmethod
    def is_match(line):
        return bool(Status.match(line))
    @staticmethod
    def enum(line):
        return Status.match(line).groups()[0]
    @staticmethod
    def is_error(line):
        return Status.enum(line).startswith(b'VI_ERROR')
