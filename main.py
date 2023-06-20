from sys import argv, exit
from command_runner import CommandRunner
from result import ResultError, Result
from input import parseInput
from config import commandDir, shellProgram

def exitWith(result: ResultError):
  if result.message != None:
    print(result.message)
  exit(result.code)

if __name__ == "__main__":
  try:
    input = parseInput(argv)

    runner = CommandRunner(commandDir, shellProgram)

    if input.action == "help":
      runner.runHelp(input.group)
      exit(0)

    result = runner.runCommand(input)
    exitWith(result)

  except ResultError as e:
    exitWith(e.result)
  except Exception as e:
    exitWith(Result(1, f'Unexpected error occurred: {e}'))
