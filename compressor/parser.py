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
from compressor.template import Template

import os
import yaml


class CompressorParser(object):

    def __init__(self, options, cli):
        self.set_config(options.config_file)
        self.cli = cli

        self.parse()

    def set_config(self, config_file):
        file_content = open(config_file).read()
        self.config = yaml.load(file_content)

    def parse(self):
        self.cli.msg("Compressor running, looking for templates...")

        self.listdir(self.config.get('path').get('template'))

        (options, args) = self.cli.parse()
        if options.sync:
            from compressor.bucket import BucketSync
            bucket = BucketSync(
                self.cli,
                self.config['sync']['aws_access_key'],
                self.config['sync']['aws_secret_key'],
                self.config['sync']['bucket_name'],
                self.config['sync']['path'],
                self.config['sync']['bucket_base_path']
            )
            bucket.sync()

    def listdir(self, path):
        dirlist = os.listdir(path)
        for fname in dirlist:
            file_path = os.path.join(path, fname)
            if os.path.isdir(file_path):
                self.listdir(file_path)
            else:
                extension = os.path.splitext(os.path.basename(file_path))[1]
                if extension in ('.html'):
                    self.parse_file(file_path)

    def parse_file(self, filename):
        template = Template(filename, self.config, self.cli)
        template.compress()
