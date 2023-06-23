Shorthand is a CLI tool that turns your complex one-liners into simple shorthand commands.

# Usage
Shorthand works by defining commands in groups listed as YAML files. By default command files are located in the `command/` directory located in the same location as the executable. To create a group and its commands, define one with the desired name and template as follows: 

```yaml
# greet.yml
commands:
  hello: echo Hello world!
```

To use a Shorthand command, use the follow syntax:

```bash
short <group> <command>
```

So the above example would be used as follows: `short greet hello`

## Using arguments
Arguments can be injected into commands via standard Python string format syntax. So in the above example we could add a `goodbye` command which allows for a name to be input:

```yaml
# greet.yml
commands:
  hello: echo Hello world!
  goodbye: echo Goodbye {0}.
```

Resulting in a command that works as follows:
```bash
$ short greet goodbye friend
# outputs:
Goodbye friend.
```

# Building
To build the Shorthand repo, ensure that you have Python 3 and pyinstaller installed. Then use the `gen-exe` script:

```bash
./gen-exe
```

Output files will be located in `dist/`


