# powerranger

A ranger-inspired file manager for PowerShell.

## Installation

You'll need Python 3.8 or higher. Install or update with:

```shell
pip install --user --upgrade powerranger
```

## Usage

This program is intended to run on Windows. From `powershell.exe` or
`cmd.exe`, you can run:

```cmd
python -m powerranger
```

If you want to run from Git Bash and get an error saying "Rediration not
supported", you can use `winpty` to start the program instead:

```shell
winpty python -m powerranger
```

Or, ideally, bind this command to an alias or function in bash.

## License

MIT
