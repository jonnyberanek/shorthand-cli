from collections import namedtuple

CommandInput = namedtuple("Args", ["group", "action", "args"])

def parseInput(args):
  return CommandInput(
    args[1],
    "help" if len(args) < 3 else args[2],
    args[3:]
  )