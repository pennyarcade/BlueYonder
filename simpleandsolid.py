#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Blue Yonder Coding Task - Image downloader
3. Simple and solid solution

:author Martin Toennishoff:
:created 2018/04/05:

Usage: quickanddirty.py <path to input file>
"""
# 3rd party modules
import requests
import magic
import yaml

# standard library modules
import argparse
import logging
import os
import sys
import tempfile
import errno
from urlparse import urlparse


def create_parser(parserclass=argparse.ArgumentParser):
    """
    create argument parser, handle command line parameters, provide command line help
    Avoid a global default configuration by setting default values here
    Factory method

    @see: https://stackoverflow.com/questions/39028204/using-unittest-to-test-argparse-exit-errors

    :param parserclass: set the argument parser class in an optional parameter to be able to switch it out for testing
    :return:
    """
    parser = parserclass('Download images from urls provided to local storage')

    # No defaults so every empty value is returned as None
    parser.add_argument(
        '-i'
        '--input_file',
        help='Input file: Plain text list of urls; one per line',
        type=lambda s: s.strip()
    )

    # positional argument: Output directory, no default this parameter is mandatory
    parser.add_argument(
        '-o',
        '--output_dir',
        help='Output directory: downloaded files will be written here; write permissions needed',
        type=lambda s: s.strip()
    )

    # verbosity level
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-v',
        '--verbosity',
        help='Set verbosity level for screen output: [none, debug, info, warn, error]',
        choices=['quiet', 'debug', 'info', 'warn', 'error'],
        type=lambda s: s.strip().lower()
    )
    verbosity.add_argument(
        '-q',
        '--quiet',
        help='No output to screen. Same as "--verbosity none"',
        action='store_const',
        const='quiet'
    )

    parser.add_argument(
        '-l',
        '--log_level',
        help='Set verbosity level for log output: [none, debug, info, warn, error]',
        choices=['quiet', 'debug', 'info', 'warn', 'error'],
        type=lambda s: s.strip().lower()
    )
    parser.add_argument(
        '-f',
        '--log_file',
        help='Set file to write logs to',
        type=lambda s: s.strip()
    )
    parser.add_argument(
        '-c',
        '--config_file',
        help='Set file to read config from. Has to be valid YAML format.',
        type=lambda s: s.strip()
    )

    return parser


def setup_logging(config):
    """
    Setup and configure logging environment
    Factory method

    :param config: dictionary with configuration values
    :return: logger object
    """
    logger = logging.getLogger(__name__)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(config['verbosity'])
    # use a very simple log format for console output
    # Todo: maybe make this configurable later
    console_handler.setFormatter('%(levelname)s:%(module)s - %(message)s')

    file_handler = logging.FileHandler(config['log_file'])
    file_handler.setLevel(config['log_level'])
    # use a more detailed log format for file output leaning on the PHP error log format
    # [12-Jun-2011 12:58:55] PHP Notice:  Undefined variable: test in C:\www\phpinfo.php on line 2\r\r\n
    # Todo: maybe make this configurable later
    file_handler.setFormatter(
        '[%(asctime)s] %(levelname)s: %(module)s: %(funcName)s: %(message)s in %(pathname)s on line %(lineno)d'
    )

    # getLogger() returns references to the same object but handlers may be duplicated. So only add handlers if there
    # are none. This issue arrises only in unittests since this function is only called once in the script
    # @see: https://stackoverflow.com/questions/6333916/python-logging-ensure-a-handler-is-added-only-once
    if not len(logger.handlers):
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


def verify_file(filename, permission, mime_type):
    """
    Check if input/output file is a valid path and is suitable for reading/writing

    Taking typical linux exit codes from stack overflow
    @see: https://stackoverflow.com/questions/1101957/are-there-any-standard-exit-status-codes-in-linux

    > #define EX_OK           0       /* successful termination */
    > #define EX__BASE        64      /* base value for error messages */
    > #define EX_USAGE        64      /* command line usage error */
    > #define EX_DATAERR      65      /* data format error */
    > #define EX_NOINPUT      66      /* cannot open input */
    > #define EX_NOUSER       67      /* addressee unknown */
    > #define EX_NOHOST       68      /* host name unknown */
    > #define EX_UNAVAILABLE  69      /* service unavailable */
    > #define EX_SOFTWARE     70      /* internal software error */
    > #define EX_OSERR        71      /* system error (e.g., can't fork) */
    > #define EX_OSFILE       72      /* critical OS file missing */
    > #define EX_CANTCREAT    73      /* can't create (user) output file */
    > #define EX_IOERR        74      /* input/output error */
    > #define EX_TEMPFAIL     75      /* temp failure; user is invited to retry */
    > #define EX_PROTOCOL     76      /* remote error in protocol */
    > #define EX_NOPERM       77      /* permission denied */
    > #define EX_CONFIG       78      /* configuration error */

    """
    path = os.path.abspath(filename)

    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        # File is to be opened for reading and therefore has to exist
        if permission == os.R_OK and not os.path.exists(path):
            return 66, 'Not a valid path: %s\n' % (filename)
        # File is to be opened for reading and therefore has be a valid file
        elif permission == os.R_OK and not os.path.isfile(path):
            return 66, 'Not a valid file: %s\n' % (filename)
        # check file permission for reading
        elif permission == os.R_OK and not os.access(path, permission):
            return 77, 'No permission to read file: %s\n' % (filename)
        # check the file type for files opened for reading
        elif permission == os.R_OK and not m.id_filename(path) == mime_type:
            return 74, 'Wrong file type "%s": %s\n' % (m.id_filename(path), filename)
        # when writing a file the target directory has to exist
        elif permission == os.W_OK and not os.path.exists(os.path.dirname(path)):
            return 73, 'Not a valid path for output: %s\n' % (os.path.dirname(filename))
        # when writing a file the path has to resolve to a directory
        elif permission == os.W_OK and not os.path.isdir(os.path.dirname(path)):
            return 73, 'Not a directory: %s\n' % (os.path.dirname(filename))
        # when writing a file the directory has to be writeable
        elif permission == os.W_OK and os.path.isdir(os.path.dirname(path)):
            # work around wonky behaviour of os.access()
            try:
                testfile = tempfile.TemporaryFile(dir=os.path.dirname(path))
                testfile.close()
            except OSError as e:
                # catch access error
                if e.errno == errno.EACCES:
                    return 77, 'No permission to write to directory: %s\n' % (os.path.dirname(filename))
                # all other errors reraise exception for unexpected error
                e.filename = os.path.dirname(filename)
                raise

        return 0, 'File is fine'


def verify_configuration(config, exitfunc=sys.exit):
    """
    Sanity check configuration in command line arguments or config file; log and exit on errors
    This happens before logging is set up so use stderr to output error message and terminate script

    Todo: Not quite sure how to tet this properly yet...

    :param config: dictionary of config values
    :param exitfunc: make the sys.exit call overwriteable for unittesting
    :return:
    """
    # check for valid input file or abort
    status = verify_file(config['input_file'], os.R_OK, 'text/plain')
    if status[0] != 0:
        sys.stderr.write(status[1])
        exitfunc(status[0])

    # check for a valid log directory to write logfile to
    status = verify_file(config['log_file'], os.W_OK, '')
    if status[0] != 0:
        sys.stderr.write(status[1])
        exitfunc(status[0])

    # check for a valid log directory to write logfile to
    status = verify_file(config['output_dir'], os.W_OK, '')
    if status[0] != 0:
        sys.stderr.write(status[1])
        exitfunc(status[0])

    # skip checking config file that is already handled

    if config['verbosity'] not in [logging.FATAL, logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR]:
        sys.stderr.write('Error: Invalid verbosity level')
        exitfunc(status[0])

    if config['log_level'] not in [logging.FATAL, logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR]:
        sys.stderr.write('Error: Invalid log level')
        exitfunc(status[0])


def merge_configuration(args, config):
    """
    merge configuration by priority
    <command line arguments> override <configuration file> override <default configuration>

    :param args: command line arguments object
    :param config: configuration dictionary from file
    :return: merged configuration dictionary
    """
    # At the moment I seem to need to put the default config here for comparison to get the merge priorities right
    default = {
        'input_file': 'test/fixtures/sample_input.txt',
        'output_dir': '.',
        'verbosity': logging.WARN,
        'log_level': logging.WARN,
        'log_file': 'logs/general.simpleandsolid.log',
        'config_file': 'config/configuration.simpleandsolid.yaml'
    }

    map_log_levels = {
        'quiet': logging.FATAL,
        'debug': logging.DEBUG,
        'info':  logging.INFO,
        'warn':  logging.WARN,
        'error': logging.ERROR
    }

    if args.input_file is not None:
        default['input_file'] = args.input_file
    elif config['input_file'] is not None:
        default['input_file'] = config['input_file']

    if args.output_dir is not None:
        default['output_dir'] = args.output_dir
    elif config['output_dir'] is not None:
        default['output_dir'] = config['output_dir']

    if args.verbosity is not None:
        default['verbosity'] = map_log_levels[args.verbosity]
    elif config['verbosity'] is not None:
        default['verbosity'] = map_log_levels[config['verbosity']]

    if args.quiet is not None:
        default['verbosity'] = logging.FATAL

    if args.log_level is not None:
        default['log_level'] = map_log_levels[args.log_level]
    elif config['log_level'] is not None:
        default['log_level'] = map_log_levels[config['log_level']]

    if args.log_file is not None:
        default['log_file'] = args.output_dir
    elif config['log_file'] is not None:
        default['log_file'] = config['log_file']

    if args.config_file is not None:
        default['config_file'] = args.config_file
    elif config['config_file'] is not None:
        default['config_file'] = config['config_file']

    return default


def configure():
    """
    get configuration and verify config values

    Todo: not sure how to test this properly but all important components are covered

    :return:
    """
    # first get command line options. They override all other config
    args = create_parser().parse_args(sys.argv[1:])
    conf = load_config_file(args)
    conf = merge_configuration(args, conf)
    verify_configuration(conf)
    log = setup_logging(conf)

    return conf, log


def load_config_file(args):
    """
    Try to load a configuration from a yaml file
    This is very error tolerant because a config file is optional and missing values are taken
    from parameters or default config

    :param args:
    :return:
    """
    # return this in case of error
    empty_conf = {
        'input_file': None,
        'output_dir': None,
        'verbosity': None,
        'log_level': None,
        'log_file': None,
        'config_file': None
    }

    filename = 'config/config_simpleandsolid.yml'
    if args.config_file != None:
        filename = args.config_file

    try:
        # don't even try to check if the file exists beforehand we will get an exception
        with open(filename, 'r') as stream:
            try:
                parsed = yaml.load(stream)

                # Todo: decide on a config format and parse it into the config dictionary

            except yaml.YAMLError as exc:
                # if we can open the file but its not parsable yaml
                return empty_conf

    except IOError() as exc:
        # if we can't even open the file
        return empty_conf

    return conf


def download_images(config, logger, exitfunc=sys.exit):
    """
    Main loop, iterate over input file and process it line by line, downloading the images

    :param config: dictionary of configuration values
    :param logger: logger for input and output
    :param exitfunc: make the sys.exit call overwriteable for testing
    :return: None
    """
    # open input file for reading line by line
    try:
        with open(config['input_file'], 'r') as infile:
            for line in infile.readlines():
                process_line(line, config, logger)
    except IOError as exc:
        # This really should never happen after all that input verification
        logger.error('Exception opening input file for reading: %s' % (str(exc)))
        exitfunc(74)


def generate_filename(url, output_dir):
    """
    generate a sensible filename from an url and prepend output directory

    :param url: a url to process
    :param output_dir: directory to write the file to
    :return:
    """
    parsed = urlparse(url)
    return os.path.join(
        output_dir,
        parsed[1].replace(".", "_").replace(":", "_") + parsed[2].replace("/", '_')
    )


def write_file(response, outfile):
    """
    Open output file for writing binary and write image chunkwise

    :param response:
    :param outfile:
    :return:
    """
    with open(outfile, 'wb') as f:
        # use iter_content() to force response body decoding and write 4kb chunks to output file
        for chunk in response.iter_content(4096):
            f.write(chunk)


def process_line(line, config, logger):
    """
    process a line of input, i.e. a single url

    :param line: a line of input containing a url
    :param config: the config dictionary
    :param logger: the logger for output
    :return:
    """
    logger.info("Loading %s ... " % line)

    # request the url via GET
    r = requests.get(line, stream=True)

    # generate a unique-ish filename that includes source information
    outfile = generate_filename(line, config['output_dir'])

    # If it worked then
    if r.status_code == 200:
        logger.info("S:%d writing file %s ... " % (r.status_code, outfile))
        write_file(r, outfile)
        logger.debug("done...")

    # Status other than 200 = OK so request failed
    else:
        logger.warn("S:%d ERROR downloading %s\n" % (r.status_code, line))


# Program starts off here
if __name__ == "__main__":
    conf, log = configure()
    download_images(conf, log)
