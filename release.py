#!/usr/bin/env python3
import re
import sys

#
# a basic release automation script
#
# This should only be called from the Makefile
#

VERSION_FILE = 'VERSION'

help_message = ("The argument must be formatted as either 'major', 'minor', 'patch' or 'X.X.X'\n"
                "\n"
                "If one of the first three options is used than that part of the version will\n"
                "be incremented and all lesser parts of the version will be reset to 0.")


def read_version():
    with open(VERSION_FILE, 'r') as fp:
        return tuple(map(int, fp.read().split('.')))


def write_version(major, minor, patch):
    with open(VERSION_FILE, 'w') as fp:
        fp.write(f'{major}.{minor}.{patch}')


def main():
    # when called from the makefile we expect only 1 arg
    assert len(sys.argv) == 2

    arg = sys.argv[1]

    major, minor, patch = read_version()
    print(f'Previous version set to {major}.{minor}.{patch}')

    if arg == 'help':
        print(help_message)
        exit(0)
    elif arg == 'major':
        major += 1
        minor = 0
        patch = 0
    elif arg == 'minor':
        minor += 1
        patch = 0
    elif arg == 'patch':
        patch += 1
    # of form X.X.X
    elif re.match('^\d*\.\d*\.\d*$', arg):
        major, minor, patch = tuple(arg.split('.'))
    else:
        print(help_message)
        exit(1)

    write_version(major, minor, patch)
    print(f'New version successfully set to {major}.{minor}.{patch}. To finish release, commit\n'
          'changes. Then create a release on github with this version number. Travis will\n'
          'automatically upload to PyPI')


if __name__ == '__main__':
    main()
