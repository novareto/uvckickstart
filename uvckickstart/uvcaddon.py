import re
import sys
import optparse
from paste.script import command


from zopeskel.base import var
from zopeskel.basic_namespace import BasicNamespace

class UVCAddOn(BasicNamespace):
    _template_dir = 'templates/uvcaddon'
    summary = "Create a AddOn for UVCSite"
    required_templates = []
    use_cheetah = True

#
## Runner
#



def main():
    usage = "usage: %prog PROJECT"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--svn-repository', dest="repos", default=None,
                      help="Import project to given repository location (this "
                      "will also create the standard trunk/ tags/ branches/ "
                      "hierarchy).")
    parser.add_option('--registry', dest="registry", default='uvcsite',
                      help="Please specify a different registry. "
                      "If you not want a uvcsite-plugin. ")
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
    extra_args = []
    exit_code = runner.run(option_args + ['-t', 'uvcaddon', project]
                           + extra_args)
    sys.exit(exit_code)

