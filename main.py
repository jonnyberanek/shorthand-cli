import subprocess
from sys import argv

def aapt_apk(args):
  process = subprocess.run(
    "aapt dump badging".split(" ") + args,
    capture_output=True,
    text=True
  )
  if(process.returncode == 0):
    print("\n".join(str(process.stdout).split("\n")[:3]))
  else:
    print(str(process.stderr))
    exit(process.returncode)

commands = [aapt_apk]

def getCliName(fn):
  return(" ".join (fn.__name__.split("_")))

if __name__ == "__main__":
  target = None
  for c in commands:
    if getCliName(c) == f"{argv[1]} {argv[2]}":
      target = c
      break
  
  if target == None:
    validCommands = ", ".join(getCliName(c) for c in commands)
    print(f"Not a valid command! Please use one of the following:\n\t{validCommands}")
    exit(1)

  target(argv[3:])