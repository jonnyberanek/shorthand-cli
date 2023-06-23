from collections import namedtuple

CommandInput = namedtuple("Args", ["group", "action", "args"])

def parseInput(args):
  if (len(args) == 0):
    return None
  return CommandInput(
    args[0],
    "help" if len(args) < 2 else args[1],
    args[2:]
  )