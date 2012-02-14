from getpass import getpass
from compressor.cli import CLI
from compressor.parser import CompressorParser

import codecs
import sys
import pycompressor
import traceback


# fixing print in non-utf8 terminals
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def run():
    cli = CLI()
    try:
        (options, args) = cli.parse()

        if options.compressor_version:
            msg = 'compressor v%s' % pycompressor.__version__
            cli.info_and_exit(msg)

        if options.show_colors:
            CLI.show_colors()
            
        parser = CompressorParser(options, cli)
            
    except KeyboardInterrupt:
        cli.info_and_exit("\nExecution interrupted by user...")
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        cli.error_and_exit(str(e))

if __name__ == '__main__':
    run()