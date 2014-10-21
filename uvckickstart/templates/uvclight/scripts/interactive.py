# -*- coding: utf-8 -*-
"""Very generic runner.
"""

import argparse
import os
import sys
from ul.browser.shell import make_shell
from paste.deploy.loadwsgi import ConfigLoader
from infrae.testbrowser.browser import Browser


def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "no": False, "n": False}

    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            value = valid[choice]
            if not value:
                print "Aborting."
            else:
                print "Proceeding...\n\n"
                print "Output :\n"
            return value
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def file_runner(app, browser, pyfile):
    proceed = query_yes_no(
        u'You are about to run the file %r in your environment. \n'
        u'This could result in harmful consequences. \n'
        u'Are you sure you want to proceed ?' % pyfile)
    if proceed:
        app_runner = getattr(app, '__runner__', None)
        _globals = {'__name__': '__main__'}
        if app_runner is None:
            execfile(pyfile, _globals)
        else:
            app_runner(execfile)(pyfile, _globals, dict(app=app, browser=browser))


def shell_runner(app, browser):
    ns = dict(app=app, browser=browser)
    interactive_shell = getattr(app, '__interact__', None)
    if interactive_shell is None:
        print ("The application %r doesn't have a specific __interact__ "
                "debugging method. Spawning a generic one." % app)
        interactive_shell = make_shell
    interactive_shell(banner="Python@ASD-project", **ns)


def runner(app, browser=None, pyfile=None):
    if pyfile is not None:
        return file_runner(app, browser, pyfile)
    shell_runner(app, browser)


parser = argparse.ArgumentParser()
parser.add_argument("ini", help="PythonPaste configuration file")
parser.add_argument("--app", help="Name of the app configuration section")
parser.add_argument("--file", help="python script to run")
parser.add_argument("--browser", help="Fake browser emulation", action="store_true")
args = parser.parse_args()
loader = ConfigLoader(args.ini)

app = args.app and loader.get_app(args.app) or loader.get_app()
browser = args.browser and Browser(app) or None
runner(app, browser, pyfile=args.file)
