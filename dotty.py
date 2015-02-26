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

def copy_files(files, dot_folder, fast_fail=True, reverse=False):
	click.secho("# Copying files for %s" % (dot_folder), bold=True)
	for f, t in files.items():
		f = os.path.join(dot_folder, f)
		if reverse: f, t = t, f
		if os.path.exists(t) and fast_fail:
			click.echo("[%s] %s exists and would be overwritten, failing fast." % (click.style("ERROR", fg="red"), rel_t), err=True)
			exit(1)
		shutil.copy2(f, t)
		click.echo("[%s] copied %s -> %s" % (click.style("OK", fg="green"), f, t))

def call(command):
	cmd = Popen(command, stdout=PIPE, stderr=PIPE)
	output = cmd.communicate()[0]
	rc = cmd.returncode
	if rc > 0:
		click.echo("[%s] \"%s\" exited with code %d. ABORTING" % (click.style("ERROR", fg="red"), command, cmd.returncode))
		exit(rc)
	return output.decode("utf-8")

def in_out(ctx):
	if not ctx.obj["host_only"]:
		copy_files(ctx.obj["config"]["common"], "common", fast_fail=ctx.obj["overwrite"])
	if not ctx.obj["common_only"]:
		if not ctx.obj["config"]["machine_specific"].get(host, None):
			click.echo("[%s] no configuration for %s" % (click.style("ERROR", fg="red"), host), err=True)
			exit(1)
		copy_files(ctx.obj["config"]["machine_specific"][host], host, fast_fail=ctx.obj["overwrite"])

@click.group(chain=True)
@click.option("-c", "--config")
@click.option("-o", "--overwrite")
@click.pass_context
def cli(ctx, config, overwrite):
	if not config:
		config = "config.json"
	with open(config, "r") as f:
		config_f = json.load(f)
	ctx.obj["config"] = config_f
	ctx.obj["overwrite"] = overwrite
	ctx.obj["host"] = platform.node() # ...?

	color = random.choice(["blue", "red", "green", "magenta", "cyan", "yellow"])

	remotes = call(["git", "remote", "-v"]).split("\n")
	cur_hash = call(["git", "rev-parse", "--short", "HEAD"])
	click.secho("#", fg=color)
	click.secho("#        __      __  __       ", fg=color)
	click.secho("#   ____/ /___  / /_/ /___  __", fg=color)
	click.secho("#  / __  / __ \/ __/ __/ / / /", fg=color)
	click.secho("# / /_/ / /_/ / /_/ /_/ /_/ / ", fg=color)
	click.secho("# \__,_/\____/\__/\__/\__, /  ", fg=color)
	click.secho("#                    /____/   ", fg=color)
	click.secho("#", fg=color)
	click.secho("# dotty v%s" % (VERSION), fg=color)
	click.secho("# configuration file: %s" % (config), fg=color)
	click.secho("# git remote fetch: %s" % (remotes[0].split("\t")[1].split(" ")[0]), fg=color)
	click.secho("# git remote push: %s" % (remotes[1].split("\t")[1].split(" ")[0]), fg=color)
	click.secho("# git current commit: %s" % (cur_hash.strip()), fg=color)
	click.secho("#", fg=color)
	click.echo()

@cli.command("in")
@click.option("--common-only")
@click.option("--host-only")
@click.pass_context
def dots_in(ctx, common_only, host_only):
	click.secho("# Collecting files", bold=True)
	ctx.obj["common_only"] = common_only
	ctx.obj["host_only"] = host_only
	in_out(ctx)

@cli.command("out")
@click.option("--common-only")
@click.option("--host-only")
@click.pass_context
def dots_out(ctx, common_only, host_only):
	click.secho("# Distributing files", bold=True)
	ctx.obj["common_only"] = common_only
	ctx.obj["host_only"] = host_only
	in_out(ctx)

@cli.command("pull")
def pull():
	click.secho("# Pulling from git repository", bold=True)
	call(["git", "pull"])

@cli.command("push")
@click.argument("message")
def push(message, add=None):
	click.secho("# Pusing to git repository", bold=True)
	if add == True:
		call(["git", "add", "."])
	elif type(add) == list:
		for a in add:
			call(["git", "add", a])
	call(["git", "commit", "-am", message])
	call(["git", "push"])

@cli.command("check_config")
@click.pass_context
def check_config(ctx):
	host = platform.node()

	click.secho("# Common files", bold=True)
	for f, t in ctx.obj["config"]["common"].items():
		click.echo("\tcommon/%s -> %s" % (f, t))
	click.echo()

	click.secho("# You are on [%s]" % (host), bold=True)
	if len(ctx.obj["config"]["machine_specific"][host].keys()) > 0:
		for f, t in ctx.obj["config"]["machine_specific"][host].items():
				click.echo("\t%s/%s -> %s" % (host, f, t))
	else:
		click.echo("\tno files for %s" % (host))
	click.echo()

	for host_spec, files in ctx.obj["config"]["machine_specific"].items():
		if not host_spec == host:
			click.secho("# Files for host '%s'" % (host_spec), bold=True)
			if len(ctx.obj["config"]["machine_specific"][host_spec].keys()) > 0:
				for f, t in ctx.obj["config"]["machine_specific"][host_spec].items():
					click.echo("\t%s/%s -> %s" % (host_spec, f, t))
			else:
				click.echo("\tno files for %s" % (host_spec))	
			click.echo()

if __name__ == '__main__':
    cli(obj={})
