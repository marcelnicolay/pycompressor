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
from compressor.cli import CLI
from compressor.parser import CompressorParser

import codecs
import sys
import traceback
import compressor

# fixing print in non-utf8 terminals
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def run():
    cli = CLI()
    try:
        (options, args) = cli.parse()

        if options.compressor_version:
            msg = 'compressor v%s' % compressor.__version__
            cli.info_and_exit(msg)

        if options.show_colors:
            CLI.show_colors()

        CompressorParser(options, cli)

    except KeyboardInterrupt:
        cli.info_and_exit("\nExecution interrupted by user...")
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        cli.error_and_exit(str(e))

if __name__ == '__main__':
    run()
