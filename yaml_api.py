from dataclasses import dataclass
from os.path import join, exists, isfile
from typing import Literal, Union

from yaml import load
from yaml.loader import Loader

COMMANDS = 'commands'

@dataclass
class Command:
  command: str

def parseCommandFile(filePath):
  return load(open(filePath), Loader)

def getCommandGroupPath(dir, group):
  return join(dir, f"{group}.yml")

def groupExists(dir, group) -> Union[Literal['none'], Literal['invalid'], Literal['valid']]:
  file = getCommandGroupPath(dir, group)
  if not exists(file) or not isfile(file):
    return 'none'
  data = parseCommandFile(file)
  if data is None or data[COMMANDS] is None:
    return 'invalid'
  return 'valid'

def getCommand(dir, group, action) -> Command:
  input = parseCommandFile(getCommandGroupPath(dir, group))[COMMANDS][action]
  if input is None:
    raise TypeError('Invalid command: Must be a string or object with property "command: str"')
  if isinstance(input, str):
    return Command(input)
  return Command(**input) 

def getCommands(dir, group):
  return parseCommandFile(getCommandGroupPath(dir, group))[COMMANDS].items()