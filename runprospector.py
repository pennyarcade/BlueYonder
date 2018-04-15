#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
runprospector.py.

This script runs prospector and processes the output into a github style task list

"""

import subprocess
import os
import time


def main():
    """
    runs prospector and formats its output to use as github markdown checklists
    """
    output = subprocess.check_output(['prospector', '-0'])
    line_number = 0
    summary = False

    processed = ""

    for line in output.split(os.linesep):
        line_number += 1

        if line.startswith('Check'):
            summary = True

        if (line_number < 4) or summary or (len(line.strip()) == 0):
            processed += line + os.linesep
            continue

        indent = len(line) - len(line.lstrip())

        if (indent in (0, 2, 4)) and not summary:
            line = line[:indent] + '[ ] ' + line[indent:]

        processed += line + os.linesep

    outfile = open('metrics/prospector_' + str(time.time()) + '.todo', 'w')
    outfile.write(processed)
    outfile.close()


if __name__ == '__main__':
    main()
