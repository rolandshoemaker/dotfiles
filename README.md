# dotfiles

well hello, these are my dotfiles and also a dotfile management tool I wrote in *Python* called `dotty.py`. They are seperated
by machine hostname, if you are looking around for certain stuff these hosts run these stacks

* `niya` - `Ubuntu 14.10 + xfce4 + xfwm`
* `moro` - `Ubuntu 14.10 + i3 + conky + urxvt`
* `san` - `OS X 10.10 + nothing special atm`

the common folder contains configs for

* `zsh` - `.zshrc`
* `nano` - `.nanorc`
* various scripts in `.bin`

## `dotty.py`

`dotty.py` is a pretty simple multi machine dotfile management tool designed to be used with `git` to handle both common and
specific configuration dotfiles across various machines. It uses a pretty simple *JSON* configuration file `config.json` or
the configuration file specified using `-c` or `--config`.

	$ dotty.py
	Usage: dotty.py [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

	Options:
	  -c, --config TEXT  Path to configuration file instead of just using
	                     config.json.
	  -o, --overwrite    Overwrite files instead of failing.
	  -x                 Hide the header.
	  --help             Show this message and exit.

	Commands:
	  check_config  Whats your dotty.py config file say.
	  in            Collect local configuration files.
	  out           Distribute configuration files locally.
	  pull          Pull most recent commit using git.
	  push          Commit and push changes using git.

`dotty.py` uses the *Python* [click](http://click.pocoo.org/) cli library which allows super awesome command chaining (or single
command invocation) allowing things like this

	$ ./dotty.py -o pull out # ...excuse me

will pull the most recent commit from where ever your `git` remote points too and then copy the files to the right local
directories as specificed in the config.json file (`dotty.py` will do user expansion so you can use paths like `~/.zshrc`
safely for common ***and*** machine specific files).

or 

	$ ./dotty.py -o in push "the changes made to the files"

which will copy all the local config files to the dotfile folder and then commit the changes with the provided message
and then push to the remote.
