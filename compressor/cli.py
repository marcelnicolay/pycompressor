# coding: utf-8
# <pycompressor - compress and merge static files (css,js) in html files>
# Copyright (C) <2012>  Marcel Nicolay <marcel.nicolay@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from optparse import OptionParser
import sys


class CLI(object):

    color = {
        "PINK": "",
        "BLUE": "",
        "CYAN": "",
        "GREEN": "",
        "YELLOW": "",
        "RED": "",
        "END": "",
    }

    @staticmethod
    def show_colors():
        CLI.color = {
            "PINK": "\033[35m",
            "BLUE": "\033[34m",
            "CYAN": "\033[36m",
            "GREEN": "\033[32m",
            "YELLOW": "\033[33m",
            "RED": "\033[31m",
            "END": "\033[0m",
        }

    def __init__(self):
        self.__config_parser()

    def __config_parser(self):
        self.__parser = OptionParser(usage="usage: %prog [options] start")

        self.__parser.add_option("-c", "--config",
                dest="config_file",
                default="compressor.yaml",
                help="Use a specific config file. If not provided, will search for 'compressor.yaml' in the current directory.")
        self.__parser.add_option("-s", "--sync",
                dest="sync",
                action="store_true",
                default=False,
                help="Sync files with S3")
        self.__parser.add_option("-v", "--version",
                action="store_true",
                dest="compressor_version",
                default=False,
                help="Displays compressor version and exit.")

        self.__parser.add_option("--color",
                action="store_true",
                dest="show_colors",
                default=False,
                help="Output with beautiful colors.")

        self.__parser.add_option("--prefix",
                dest="prefix",
                default="min",
                help="Use prefix in output js and css.")

    def get_parser(self):
        return self.__parser

    def parse(self):
        return self.__parser.parse_args()

    def error_and_exit(self, msg):
        self.msg("[ERROR] %s\n" % msg, "RED")
        sys.exit(1)

    def info_and_exit(self, msg):
        self.msg("%s\n" % msg, "BLUE")
        sys.exit(0)

    def msg(self, msg, color="CYAN"):
        print "%s%s%s" % (self.color[color], msg, self.color["END"])