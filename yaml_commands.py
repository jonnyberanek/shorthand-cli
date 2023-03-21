import subprocess
from os import listdir
from os.path import isfile, join
from sys import argv

from yaml import load
from yaml.loader import Loader


def parseCommandFile(filePath):
  return load(open(filePath), Loader)

def getCommandGroupPath(dir, group):
  return join(dir, f"{group}.yml")

def getCommand(dir, group, action):
  return parseCommandFile(getCommandGroupPath(dir, group))["commands"][action]

def getCommands(dir, group):
  return parseCommandFile(getCommandGroupPath(dir, group))["commands"].items()