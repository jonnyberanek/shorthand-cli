from collections import namedtuple
from dataclasses import dataclass
import subprocess
from sys import argv, exit

from yaml_commands import getCommand, getCommands

# TODO: trim lines func

Args = namedtuple("Args", ["group", "action", "passthroughArgs"])

@dataclass
class Result:
  code: int
  message: str = None

class ResultError(Exception):

  def __init__(self, result: Result, *args) -> None:
    super().__init__(result.message, *args)
    self.result = result
  
  def makeWithResult(code, message):
    return ResultError(Result(code, message))

def parseArgs(args):
  return Args(
    args[1],
    "help" if len(args) < 3 else args[2],
    args[3:]
  )

def parseCommand(dir, group, action):
  try:
    return getCommand(dir, group, action)
  except KeyError:
    raise ResultError.makeWithResult(1, f'"{action}" does not exist.')
  except FileNotFoundError as e:
    raise ResultError.makeWithResult(1, f'"{group}" file may not exist: {e}')

def printHelp(dir, group):
  print(f'Commands in group "{group}":')
  try:
    for k,v in getCommands(dir, group):
      print(f"- {k}: {v}\n")
  except FileNotFoundError as e:
    raise ResultError.makeWithResult(1, f'"{group} file may not exist: {e}"')

def exitWith(result: Result):
  if result.message != None:
    print(result.message)
  exit(result.code)

def hydrateCommand(command, args):
  try:
    return command.format(*args)
  except IndexError:
    raise ResultError.makeWithResult(1, "Error: Not enough arguments to satisfy:\n"+command)

def parseCommandResult(process):
  if(process.returncode == 0):
    return Result(0, str(process.stdout))
  return Result(process.returncode, str(process.stderr))


commandDir = "C:\\Users\\jberanek\\Projects\\Tools\\utility-scripts\\shorthand\\commands"

if __name__ == "__main__":
  try:
    args = parseArgs(argv)

    if args.action == "help":
      printHelp(commandDir, args.group)
      exit(0)

    hydratedCommand = hydrateCommand(
      parseCommand(commandDir, args.group, args.action),
      args.passthroughArgs
    )

    process = subprocess.run(
      hydratedCommand,
      capture_output=True,
      text=True
    )  
    exitWith(parseCommandResult(process))

  except ResultError as e:
    exitWith(e.result)
  except Exception as e:
    exitWith(Result(1, f'Unexpected error occurred: {e}'))
