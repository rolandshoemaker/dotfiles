#!/usr/bin/python3
#
#        __      __  __       
#   ____/ /___  / /_/ /___  __
#  / __  / __ \/ __/ __/ / / /
# / /_/ / /_/ / /_/ /_/ /_/ / 
# \__,_/\____/\__/\__/\__, /  
#                    /____/   
#
# licensed under the MIT license <http://opensource.org/licenses/MIT>

import click

import platform, os, shutil, random, json
from subprocess import Popen, PIPE

VERSION = "0.0.1"

def copy_files(files, dot_folder, overwrite=False, reverse=False):
	click.echo("    Copying files for %s" % (dot_folder))
	if len(files.keys()) > 0: 
		for f, t in files.items():
			f = os.path.join(dot_folder, f)
			if not os.path.exists(f):
				click.echo("        [%s] target file %s doesn't exist" % (click.style("ERROR", fg="red"), f), err=True)
				exit(1)
			if t.startswith("~"):
				t = os.path.expanduser(t)
			if reverse: f, t = t, f
			if os.path.exists(t) and not overwrite:
				click.echo("        [%s] %s exists and would be overwritten and `-o` isn't set, failing fast." % (click.style("ERROR", fg="red"), t), err=True)
				exit(1)
			if os.path.isfile(f):
				shutil.copy2(f, t)
			elif os.path.isdir(f):
				if os.path.exists(t):
					shutil.rmtree(t)
				shutil.copytree(f, t)
			click.echo("        [%s] copied %s -> %s" % (click.style("OK", fg="green"), f, t))
		click.echo()
	else:
		click.echo("        no files to copy for %s\n" % (dot_folder))

def call(command):
	cmd = Popen(command, stdout=PIPE, stderr=PIPE)
	output = cmd.communicate()[0]
	rc = cmd.returncode
	if rc > 0:
		click.echo("\t[%s] \"%s\" exited with code %d. ABORTING" % (click.style("ERROR", fg="red"), command, cmd.returncode))
		exit(rc)
	return output.decode("utf-8")

def in_out(ctx):
	if not ctx.obj["host_only"]:
		copy_files(ctx.obj["config"]["common"], "common", overwrite=ctx.obj["overwrite"])
	if not ctx.obj["common_only"]:
		if ctx.obj["config"]["machine_specific"].get(ctx.obj["host"], None) == None:
			click.echo("[%s] no configuration for %s" % (click.style("ERROR", fg="red"), ctx.obj["host"]), err=True)
			exit(1)
		copy_files(ctx.obj["config"]["machine_specific"][ctx.obj["host"]], ctx.obj["host"], overwrite=ctx.obj["overwrite"])

@click.group(chain=True)
@click.option("-c", "--config")
@click.option("-o", "--overwrite", is_flag=True, default=False)
@click.option("-x", is_flag=True, default=False)
@click.pass_context
def cli(ctx, config, overwrite, x):
	if not config:
		config = "config.json"
	with open(config, "r") as f:
		config_f = json.load(f)

	remotes = call(["git", "remote", "-v"]).split("\n")
	cur_hash = call(["git", "rev-parse", "--short", "HEAD"]).strip()

	ctx.obj["fetch"] = remotes[0].split("\t")[1].split(" ")[0]
	ctx.obj["push"] = remotes[1].split("\t")[1].split(" ")[0]
	ctx.obj["config"] = config_f
	ctx.obj["overwrite"] = overwrite
	ctx.obj["host"] = platform.node() # ...?

	if not x:
		color = random.choice(["blue", "red", "green", "magenta", "cyan", "yellow"])
		click.secho("#", fg=color)
		click.secho("#        __      __  __       ", fg=color)
		click.secho("#   ____/ /___  / /_/ /___  __", fg=color)
		click.secho("#  / __  / __ \/ __/ __/ / / /", fg=color)
		click.secho("# / /_/ / /_/ / /_/ /_/ /_/ / ", fg=color)
		click.secho("# \__,_/\____/\__/\__/\__, /  ", fg=color)
		click.secho("#                    /____/   ", fg=color)
		click.secho("#", fg=color)
		click.secho("# dotty v%s - dotfile management tool ^_^" % (VERSION), fg=color)
		click.secho("# here is: %s" % (ctx.obj["host"]), fg=color)
		click.secho("# configuration file: %s" % (config), fg=color)
		click.secho("# git remote fetch: %s" % (ctx.obj["fetch"]), fg=color)
		click.secho("# git remote push: %s" % (ctx.obj["push"]), fg=color)
		click.secho("# git current commit: %s" % (cur_hash), fg=color)
		click.secho("#", fg=color)
		click.echo()

@cli.command("in")
@click.option("--common-only")
@click.option("--host-only")
@click.pass_context
def dots_in(ctx, common_only, host_only):
	"""Collect local configuration files"""
	click.secho("# Collecting files", bold=True)
	ctx.obj["common_only"] = common_only
	ctx.obj["host_only"] = host_only
	in_out(ctx)

@cli.command("out")
@click.option("--common-only")
@click.option("--host-only")
@click.pass_context
def dots_out(ctx, common_only, host_only):
	"""Distribute configuration files locally"""
	click.secho("# Distributing files", bold=True)
	ctx.obj["common_only"] = common_only
	ctx.obj["host_only"] = host_only
	in_out(ctx)

@cli.command("pull")
def pull():
	"""Pull most recent commit using git"""
	click.secho("# Pulling from git repository", bold=True)
	call(["git", "pull"])
	git_hash = call(["git", "rev-parse", "--short", "HEAD"]).strip()
	click.echo("        [%s] pulled from %s, current git commit %s\n" % (click.style("OK", fg="green"), ctx.obj["fetch"], git_hash))

@cli.command("push")
@click.argument("message")
@click.pass_context
def push(ctx, message, add=None):
	"""Commit and push changes using git"""
	click.secho("# Pusing to git repository", bold=True)
	if add == True:
		call(["git", "add", "."])
	elif type(add) == list:
		for a in add:
			call(["git", "add", a])
	call(["git", "commit", "-am", message])
	call(["git", "push"])
	git_hash = call(["git", "rev-parse", "--short", "HEAD"]).strip()
	click.echo("        [%s] pushed to %s, new git commit %s\n" % (click.style("OK", fg="green"), ctx.obj["push"], git_hash))

@cli.command("check_config")
@click.pass_context
def check_config(ctx):
	"""Whats your dotty.py config file say"""
	host = platform.node()

	click.secho("# Common files", bold=True)
	for f, t in ctx.obj["config"]["common"].items():
		click.echo("        common/%s -> %s" % (f, t))
	click.echo()

	click.secho("# You are on [%s]" % (host), bold=True)
	if len(ctx.obj["config"]["machine_specific"][host].keys()) > 0:
		for f, t in ctx.obj["config"]["machine_specific"][host].items():
				click.echo("        %s/%s -> %s" % (host, f, t))
	else:
		click.echo("        no files for %s" % (host))
	click.echo()

	for host_spec, files in ctx.obj["config"]["machine_specific"].items():
		if not host_spec == host:
			click.secho("# Files for host '%s'" % (host_spec), bold=True)
			if len(ctx.obj["config"]["machine_specific"][host_spec].keys()) > 0:
				for f, t in ctx.obj["config"]["machine_specific"][host_spec].items():
					click.echo("        %s/%s -> %s" % (host_spec, f, t))
			else:
				click.echo("        no files for %s" % (host_spec))	
			click.echo()

if __name__ == '__main__':
    cli(obj={})
