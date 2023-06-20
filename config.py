import sys
from yaml import load
from yaml.loader import Loader
from os.path import dirname, join, isabs

SETTINGS_FILE = "./settings.yml"

rootDir = dirname(sys.argv[0])

def joinToRoot(path: str):
  return path if isabs(path) else join(rootDir, path)

config = load(open(joinToRoot(SETTINGS_FILE)), Loader)

commandDir = joinToRoot(config["commandDir"])
shellProgram = joinToRoot(config["shellProgram"])