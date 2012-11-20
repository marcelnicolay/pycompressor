# coding: utf-8
# <pycompressor - compress and merge static files (css,js) in html files>
# Copyright (C) <2012>  Marcel Nicolay <marcel.nicolay@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from compressor.filter import Filter
from subprocess import Popen, PIPE
import os
import re
import time


class Template(object):

    def __init__(self, template_path, config, cli):

        self.config = config
        self.cli = cli
        self.template_path = template_path.replace(self.config['path']['template'] + "/", "")

        template_filename = os.path.splitext(os.path.basename(self.template_path))[0]

        (options, args) = self.cli.parse()
        self.js_name = "{}{}.{}".format(options.prefix, template_filename, "js")
        self.css_name = "{}{}.{}".format(options.prefix, template_filename, "css")

        self.content = self.read(template_path)

        self.cli.msg(template_path)

    def read(self, file_path):
        content = ""
        with open(file_path, 'r') as f:
            content = "".join([l for l in f])  # read lines, is memory efficient and fast
        return content

    def write(self, file_output, content):
        file_path = os.path.dirname(file_output)
        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        f = open(file_output, "w")
        try:
            f.write(content)
        finally:
            f.close()

    def search_file_path(self, pattern, content):
        match = re.search(pattern, content)
        if match:
            return match.groupdict().get('file')

        return None

    def get_scripts(self):
        scripts = []
        for script in re.findall('\<script[^>]*></script>', self.content):
            search = re.search('src="(?P<value>[^"]*)"', script)
            if search:
                file_path = self.search_file_path(self.config['pattern']['js'], search.groupdict()['value'])
                if file_path:
                    scripts.append((file_path, script))

        return scripts

    def get_links(self):
        links = []
        for link in re.findall('\<link[^>]*/>', self.content):
            search = re.search('href="(?P<value>[^"]*)"', link)
            file_path = self.search_file_path(self.config['pattern']['css'], search.groupdict()['value'])
            if file_path:
                links.append((file_path, link))

        return links

    def get_merged_scripts(self):
        scripts = self.get_scripts()
        scripts_content = []

        for src, tag in scripts:
            script_path = os.path.join(self.config.get('path').get('js'), src)
            try:
                scripts_content.append(self.read(script_path))
                self.cli.msg("\t[OK]\t" + script_path, "GREEN")
            except IOError:
                self.cli.msg("\t[FAIL]\t" + script_path, "RED")

        return "".join(scripts_content)

    def get_merged_links(self):
        links = self.get_links()

        links_content = []

        for src, tag in links:
            link_path = os.path.join(self.config.get('path').get('css'), src)
            try:
                links_content.append(self.read(link_path))
                self.cli.msg("\t[OK]\t" + link_path, "GREEN")
            except IOError:
                self.cli.msg("\t[FAIL]\t" + link_path, "RED")

        return "".join(links_content)

    def _run_process(self, process, msg):
        stdout, stderr = process.communicate()
        if not stderr:
            self.cli.msg("\t[OK] " + msg, "GREEN")
        else:
            self.cli.msg("\t[FAIL] " + msg, "RED")
            self.cli.error_and_exit(stderr)

    def yuicompressor(self, file_path):
        process = Popen(['yuicompressor', '-o', file_path, file_path], stdout=PIPE, stderr=PIPE)
        self._run_process(process, file_path)

    def uglifyjs(self, file_path):
        process = Popen(['uglifyjs2', '-o', file_path, file_path],
            stdout=PIPE, stderr=PIPE)
        self._run_process(process, file_path)

    def cleancss(self, file_path):
        process = Popen(['cleancss', '-o', file_path, file_path],
            stdout=PIPE, stderr=PIPE)
        self._run_process(process, file_path)

    def compress_js(self):
        if self.js:
            js_path = os.path.join(self.config['output']['js'], self.js_name)
            self.write(js_path, self.js)
            time.sleep(1)
            self.uglifyjs(js_path)

    def compress_css(self):
        if self.css:
            css_path = os.path.join(self.config['output']['css'], self.css_name)
            self.write(css_path, self.css)
            time.sleep(1)
            self.cleancss(css_path)

    def compress(self):
        # get compressed files
        self.cli.msg("\tmerging...")
        self.js = self.get_merged_scripts()
        self.css = self.get_merged_links()

        # filter content
        compressor_filter = Filter(self.config, self)
        compressor_filter.apply()

        # save
        self.cli.msg("\tcompress...")
        self.compress_js()
        self.compress_css()

        self.write(os.path.join(self.config['output']['template'], self.template_path), self.content)
