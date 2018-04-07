"""
Unittests for Example 3 - simple and solid

"""

import unittest
import simpleandsolid


class TestSimpleAndSolid(unittest.TestCase):

    def set_up(self):
        """
        Setup function

        :return:
        """
        pass

    def tear_down(self):
        """
        Tear down function

        :return:
        """

    def test_argument_parser_valid_args(self):
        parser = simpleandsolid.create_parser()

        args = ['urls.txt', '-v debug', '-ll error', '-lf test.log', '--config_file test_config.yaml']
        result = parser.parse_args(args)

        self.assertEqual(args[0], result.input_file)
