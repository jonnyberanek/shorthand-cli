from os.path import join

from yaml import load
from yaml.loader import Loader

from dataclasses import dataclass

@dataclass
class Command:
  command: str

def parseCommandFile(filePath):
  return load(open(filePath), Loader)

def getCommandGroupPath(dir, group):
  return join(dir, f"{group}.yml")

def getCommand(dir, group, action) -> Command:
  input = parseCommandFile(getCommandGroupPath(dir, group))["commands"][action]
  if isinstance(input, str):
    return Command(input)
  return Command(**input) 

def getCommands(dir, group):
  return parseCommandFile(getCommandGroupPath(dir, group))["commands"].items()