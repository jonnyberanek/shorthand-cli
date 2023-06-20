from subprocess import CompletedProcess, run as runSubprocess

from input import CommandInput
from result import Result, ResultError
from yaml_api import getCommands, getCommand

class CommandRunner():

  def __init__(self, commandDir: str, shellProgram: str) -> None:
    self.commandDir = commandDir
    self.shellProgram = shellProgram

  def runHelp(self, group):
    print(f'Commands in group "{group}":')
    try:
      for k,v in getCommands(self.commandDir, group):
        print(f"- {k}: {v}")
    except FileNotFoundError as e:
      raise ResultError.makeWithResult(1, f'"{group} file may not exist: {e}"')

  def runCommand(self, input: CommandInput) -> Result:

    command = parseCommand(self.commandDir, input.group, input.action)

    hydratedCommand = hydrateCommand(
      command.command,
      input.args
    )

    process = runSubprocess(
      [self.shellProgram, "-c", hydratedCommand],
      capture_output=True,
      text=True,
      shell=True,
    )
    return parseCommandResult(process)

def parseCommandResult(process: CompletedProcess[str]):
    if(process.returncode == 0):
      out = ""
      if(process.stderr != None and process.stderr != ""):
        out += f'{process.stderr}\n'
      out += process.stdout
      return Result(0, out)
    return Result(process.returncode, str(process.stderr))

def parseCommand(dir, group, action):
  try:
    return getCommand(dir, group, action)
  except KeyError:
    raise ResultError.makeWithResult(1, f'"{action}" does not exist.')
  except FileNotFoundError as e:
    raise ResultError.makeWithResult(1, f'"{group}" file may not exist: {e}')

def hydrateCommand(command, args):
  try:
    return command.format(*args)
  except IndexError:
    raise ResultError.makeWithResult(1, "Error: Not enough arguments to satisfy:\n"+command)