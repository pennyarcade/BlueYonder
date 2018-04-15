"""
Unittests for Example 3 - simple and solid

"""

import unittest
import simpleandsolid
import sys
import os
import argparse
from pprint import pprint
from testfixtures import LogCapture
import logging
from nose.tools import with_setup



class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    """
    just to overwrite the sys.exit() call to make this thing testable
    """
    def error(self, message):
        #print(message)
        raise ValueError(message)  # reraise an error


class TestSimpleAndSolid(unittest.TestCase):
    def setUp(self):
        self.validparser = simpleandsolid.create_parser()
        self.errorparser = simpleandsolid.create_parser(ErrorRaisingArgumentParser)

        self.conf = {
            'verbosity': logging.WARN,
            'log_level': logging.INFO,
            'log_file': '/tmp/test.log',
            'input_file': 'test/fixtures/sample_input.txt',
            'output_dir': '.',
            'config_file': 'config/simpleandsolid.yml'
        }

    def tearDown(self):
        if os.path.isfile(self.conf['log_file']):
            os.remove(self.conf['log_file'])

    def test_argument_parser_valid_args(self):
        args = [
            '-v', 'debug',
            '-l', 'error',
            '-f', 'test.log',
            '--config_file', 'test_config.yaml',
            '-i', 'urls.txt',
            '-o', './output'
        ]
        result = self.validparser.parse_args(args)

        # test short optional arguments
        self.assertEqual(args[1], result.verbosity)
        self.assertEqual(args[3], result.log_level)
        self.assertEqual(args[5], result.log_file)

        # test long optional argument
        self.assertEqual(args[7], result.config_file)

        # test positional arguments
        self.assertEqual(args[9], result.input_file)
        self.assertEqual(args[11], result.output_dir)

        # test alternative -q switch which should return the constant 'quiet'
        args = [
            '-q',
            '-l', 'error',
            '-f', 'test.log',
            '--config_file',
            'test_config.yaml',
            '-i', 'urls.txt',
            '-o', './output'
        ]
        result = self.validparser.parse_args(args)
        self.assertEqual('quiet', result.quiet)

    def test_argument_parser_no_args(self):
        args = []
        with self.assertRaises(ValueError) as cm:
            self.errorparser.parse_args(args)

        self.assertEqual("too few arguments", cm.exception.message)

    def test_argument_parser_only_optional_args(self):
        args = ['-v', 'debug']
        with self.assertRaises(ValueError) as cm:
            self.errorparser.parse_args(args)

        self.assertEqual("too few arguments", cm.exception.message)

    def test_argument_parser_mutually_exclusive_optional_args(self):
        args = ['-v', 'debug', '-q', 'foo.txt']
        with self.assertRaises(ValueError) as cm:
            self.errorparser.parse_args(args)

        self.assertEqual("argument -q/--quiet: not allowed with argument -v/--verbosity", cm.exception.message)

    def test_logging(self):
        with LogCapture() as l:
            logger = simpleandsolid.setup_logging(self.conf)
            logger.info('testing...')

        l.check(
            ('simpleandsolid', 'INFO', 'testing...')
        )

    def test_logging_config(self):
        logger = simpleandsolid.setup_logging(self.conf)

        # print "\n"
        # pprint(logger.getEffectiveLevel())
        # pprint(logger.handlers)
        # print "\n"

        # there should be 2 handlers after setup
        self.assertEqual(2, len(logger.handlers))

        # and these are:
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)
        self.assertIsInstance(logger.handlers[1], logging.FileHandler)

        # since tis is just setting up standard library functuionality I'll not test every single configured thing.
        # if there was some grave mistage logging would have raised an exception by now

    def test_verify_file_read_existing_file(self):
        self.assertEqual(
            (0, 'File is fine'),
            simpleandsolid.verify_file('test/fixtures/sample_input.txt', os.R_OK, 'text/plain')
        )

    def test_verify_file_read_non_existing_file(self):
        self.assertEqual(
            (66, 'Not a valid path: test/fixtures/idonotexist.txt\n'),
            simpleandsolid.verify_file('test/fixtures/idonotexist.txt', os.R_OK, 'text/plain')
        )

    def test_verify_file_read_existing_path_not_a_file(self):
        self.assertEqual(
            (66, 'Not a valid file: test/fixtures\n'),
            simpleandsolid.verify_file('test/fixtures', os.R_OK, 'text/plain')
        )

    def test_verify_file_read_existing_file_no_permission(self):
        # only works on linux for now
        # the user running the tests should not be root or in the group root. Only root should be able to read the
        # sudoers file. The sudoesr file should reliably exist on most linux systems
        self.assertEqual(
            (77, 'No permission to read file: /etc/sudoers\n'),
            simpleandsolid.verify_file('/etc/sudoers', os.R_OK, 'text/plain')
        )

    def test_verify_file_read_existing_file_wrong_file_type(self):
        self.assertEqual(
            (74, 'Wrong file type "text/plain": test/fixtures/sample_input.txt\n'),
            simpleandsolid.verify_file('test/fixtures/sample_input.txt', os.R_OK, 'video/mp4')
        )

    def test_verify_file_write_existing_valid_path(self):
        self.assertEqual(
            (0, 'File is fine'),
            simpleandsolid.verify_file('test/fixtures/sample_input.txt', os.W_OK, 'irrelevant')
        )

    def test_verify_file_write_existing_valid_path(self):
        self.assertEqual(
            (0, 'File is fine'),
            simpleandsolid.verify_file('test/fixtures/sample_input.txt', os.W_OK, 'irrelevant')
        )

    def test_verify_file_write_non_existing_path(self):
        self.assertEqual(
            (73, 'Not a valid path for output: test/idonotexist\n'),
            simpleandsolid.verify_file('test/idonotexist/sample_input.txt', os.W_OK, 'irrelevant')
        )

    def test_verify_file_write_non_path(self):
        self.assertEqual(
            (73, 'Not a directory: test/fixtures/sample_input.txt\n'),
            simpleandsolid.verify_file('test/fixtures/sample_input.txt/test.txt', os.W_OK, 'irrelevant')
        )

    def test_verify_file_write_path_no_permission(self):
        self.assertEqual(
            (77, 'No permission to write to directory: /root\n'),
            simpleandsolid.verify_file('/root/test.txt', os.W_OK, 'irrelevant')
        )

    def test_verify_configuration_valid_config(self):
        self.assertIsNone(
            simpleandsolid.verify_configuration(self.conf)
        )

    def test_merge_configuration_all_args_set(self):
        class MockArguments(object):
            input_file  = 'arg_input_file'
            output_dir  = 'arg_output_dir'
            verbosity   = 'info'
            log_level   = 'info'
            log_file    = 'arg_log_file'
            config_file = 'arg_config_file'

        empty_conf = {
            'input_file': None,
            'output_dir': None,
            'verbosity': None,
            'log_level': None,
            'log_file': None,
            'config_file': None
        }

        self.assertDictEqual(
            {
                'input_file' : 'arg_input_file',
                'output_dir' : 'arg_output_dir',
                'verbosity'  : logging.INFO,
                'log_level'  : logging.INFO,
                'log_file'   : 'arg_log_file',
                'config_file': 'arg_config_file'
            },
            simpleandsolid.merge_configuration(MockArguments(), empty_conf)
        )

    def test_merge_configuration_no_config_set(self):
        class MockArguments(object):
            input_file  = None
            output_dir  = None
            verbosity   = None
            log_level   = None
            log_file    = None
            config_file = None

        empty_conf = {
            'input_file': None,
            'output_dir': None,
            'verbosity': None,
            'log_level': None,
            'log_file': None,
            'config_file': None
        }

        default = {
            'input_file': 'test/fixtures/sample_input.txt',
            'output_dir': '.',
            'verbosity': logging.WARN,
            'log_level': logging.WARN,
            'log_file': 'logs/general.simpleandsolid.log',
            'config_file': 'config/configuration.simpleandsolid.yaml'
        }

        self.assertDictEqual(
            default,
            simpleandsolid.merge_configuration(MockArguments(), empty_conf)
        )






