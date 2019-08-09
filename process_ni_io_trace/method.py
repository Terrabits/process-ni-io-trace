from   .regex import action_regex, method_regex
import csv
import re

# regex
is_method_regex = action_regex.format(method='').encode()

class Method(object):
    def __init__(self, name, completing=False, args=[]):
        self.name       = name
        self.completing = completing
        self.args       = args
        self.regex      = method_regex.format(name=self.name).encode()

    @staticmethod
    def is_method(line):
        return bool(re.match(is_method_regex, line))
    @staticmethod
    def is_completing(match):
        groups = match.groups()
        if len(groups) < 1:
            return False
        return bool(match.groups()[1])
    def is_match(self, line):
        match = re.match(self.regex, line)
        if not match:
            return None
        return Method.is_completing(match) == self.completing
    def id_args(self, line):
        groups = re.match(self.regex, line).groups()
        assert len(groups) == 3
        id         = int (groups[0])
        completing = bool(groups[1])
        args_str   = groups[2].decode(errors='ignore')
        if not args_str:
            return id, []

        args   = dict()
        values = next(csv.reader([args_str], quotechar='"', delimiter=',', skipinitialspace=True))
        for name, value in zip(self.args, values):
            args[name] = value.strip()
        return id, args
