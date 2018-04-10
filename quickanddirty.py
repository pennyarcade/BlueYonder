#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Blue Yonder Coding Task - Image downloader
1. Quick and dirty solution

This is just a shortest possible proof of concept. There is no error handling, logging, input verification etc.
The code is practically untestable since there are no functions.

:author Martin Toennishoff:
:created 2018/04/05:

Usage: quickanddirty.py <path to input file>
"""

import requests
import sys
from urlparse import urlparse
from os import linesep


# hardcode output path for quick and dirty solution
output_path = "/var/www/blueyonder/images/"

if __name__ == "__main__":
    # assume the only argument is a valid filename
    filename = sys.argv[1]

    # open input file for reading line by line
    with open(filename, 'r') as infile:
        for line in infile.readlines():
            sys.stdout.write("Loading %s ... " % line)
            # request the url via GET
            r = requests.get(line, stream=True)

            # generate a unique-ish filename that includes source information
            parsed = urlparse(line)
            outfile = parsed[1].replace(".", "_").replace(":", "_") + parsed[2].replace("/", '_')

            # If it worked then
            if r.status_code == 200:
                sys.stdout.write("S:%d writing file %s ... " % (r.status_code, outfile))
                # open output file for writing binary
                with open(output_path + outfile, 'wb') as f:
                    # use iter_content() to force respons body decoding ant write 4kb chunks to output file
                    for chunk in r.iter_content(4096):
                        f.write(chunk)
                sys.stdout.write("done" + linesep)
            # Status other than 200 = OK so request failed
            else:
                sys.stdout.write("S:%d ERROR downloading %s\n" % (r.status_code, line))
