from subprocess import CompletedProcess, run as runSubprocess

from input import CommandInput
from result import Result, ResultError
from yaml_api import getCommands, getCommand, groupExists

EXAMPLE = "\ncommands:\n  hello: echo Hello {0}! - From shorthand"

class CommandRunner():

  def __init__(self, commandDir: str, shellProgram: str) -> None:
    self.commandDir = commandDir
    self.shellProgram = shellProgram

  def runHelp(self):
    print('Usage: short [<group> [<command>]] ')
    match groupExists(self.commandDir, 'hand'):
      case 'none':
        print(f'No hand.yml found. Get started by creating a hand.yml in {self.commandDir} for your general commands like the following:{EXAMPLE}\n\nUse this by typing `short hand hello World`. You can also create additional YAML files for separate groups of commands in the same location.\n\nTo modify settings like the location of the "commands" directory, edit settings.yml, in the same directory as this program.')
      case 'invalid':
        print(f'Looks like hand.yml is invalid. Ensure that it has a "commands" block followed by a valid command. Example:{EXAMPLE}')
      case 'valid':
        print("")
        self.runGroupHelp("hand")

  def runGroupHelp(self, group):
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