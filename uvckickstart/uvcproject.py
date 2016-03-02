from grokproject import GrokProject
from paste.script import command
import optparse
import pkg_resources
import re
import subprocess
import sys
import os.path


def run_command(*args):
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.wait() != 0:
        raise RuntimeError("Error running command: %s" % ' '.join(args))


def is_svn_working_copy(path):
    try:
        run_command('svn', 'info', path)
    except RuntimeError:
        return False
    return True


class UVCProject(GrokProject):
    _template_dir = 'templates/uvcproject'
    summary = "An extranet template"

    def pre(self, cmd, output_dir, vars):
        super(UVCProject, self).pre(cmd, output_dir, vars)
        if is_svn_working_copy(output_dir):
            run_command('svn', 'ps', 'svn:ignore', 'buildout.cfg', output_dir)

    def post(self, cmd, output_dir, vars):
        # As the template adds the file although we want to ignore it, we have
        # to mark it deleted again. Grrr.
        if is_svn_working_copy(output_dir):
            run_command('svn', 'rm', '--keep-local',
                        os.path.join(output_dir, 'buildout.cfg'))
        super(UVCProject, self).post(cmd, output_dir, vars)

#
## Runner
#

project_name_re=re.compile('[a-zA-Z_][a-zA-Z0-9_]*')

def main():
    usage = "usage: %prog [options] PROJECT"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--svn-repository', dest="repos", default=None,
                      help="Import project to given repository location (this "
                      "will also create the standard trunk/ tags/ branches/ "
                      "hierarchy).")
    parser.add_option('--grokversion', dest="grokversion", default=None,
                      help="Specify the Grok version to use. GROKVERSION is "
                      "a string like 0.14.1, 1.0a1 or similar. If not given, "
                      "the latest version found on the grok website is used.")
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose",
                      default=False, help="Be verbose.")
    parser.add_option('--version', action="store_true", dest="version",
                      default=False, help="Show grokproject version.")

    # Options that override the interactive part of filling the templates.
    for var in GrokProject.vars:
        option_name = '--'+var.name.replace('_', '-')
        if not parser.has_option(option_name):
            parser.add_option(
                option_name, dest=var.name,
                help=var.description)

    options, args = parser.parse_args()

    if options.version:
        print get_version()
        return 0

    if len(args) != 1:
        parser.print_usage()
        return 1

    # create sandbox using paste.script
    project = args[0]
    commands = command.get_commands()
    cmd = commands['create'].load()
    runner = cmd('create')

    option_args = []
    if options.repos is not None:
        option_args.extend(['--svn-repository', options.repos])
    if not options.verbose:
        option_args.append('-q')

    # Process the options that override the interactive part of filling
    # the templates.
    extra_args = []
    for var in GrokProject.vars:
        supplied_value = getattr(options, var.name)
        if supplied_value is not None:
            extra_args.append('%s=%s' % (var.name, supplied_value))
    if options.grokversion:
        extra_args.append('grokversion=%s' % options.grokversion)

    extra_args.append('version_url=False') # = False
    # Assert that the project name is a valid Python identifier
    if not (project_name_re.match(project).group() == project):
        print
        print "Error: The chosen project name is not a invalid " \
              "package name: %s." % project
        print "Please choose a different project name."
        sys.exit(1)

    # Create the project
    else:
        exit_code = runner.run(option_args + ['-t', 'uvcproject', project]
                           + extra_args)
    sys.exit(exit_code)

def get_version():
    info = pkg_resources.get_distribution('grokproject')
    if info.has_version and info.version:
        return info.version
    return 'Unknown'
