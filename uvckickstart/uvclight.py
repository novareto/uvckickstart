from grokproject import GrokProject
from paste.script import command
import optparse
import pkg_resources
import re
import subprocess
import sys
import os.path
from paste.script import templates
from grokproject.utils import run_buildout
from grokproject.utils import ask_var
from paste.script.templates import NoDefault


class UVCLight(templates.Template):
    _template_dir = 'templates/uvclight'
    summary = "An uvclight extranet template"

    def check_vars(self, vars, cmd):
        vars['ppackage'] = vars['package'][:-8]
        return vars

    def post(self, command, output_dir, vars):
        original_dir = os.getcwd()
        os.chdir(vars['project'])
        run_buildout(command.verbose)
        os.chdir(original_dir)

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
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose",
                      default=False, help="Be verbose.")

    options, args = parser.parse_args()


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


    # Assert that the project name is a valid Python identifier
    if not (project_name_re.match(project).group() == project):
        print
        print "Error: The chosen project name is not a invalid " \
              "package name: %s." % project
        print "Please choose a different project name."
        sys.exit(1)


    # Create the project
    else:
        exit_code = runner.run(option_args + ['-t', 'uvclight', project+'_project'])
    sys.exit(exit_code)

