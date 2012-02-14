from compressor.minifier.js import jsmin
from compressor.minifier.css import minimalize
from compressor.filter import Filter

from subprocess import Popen, PIPE, STDOUT

import shlex
import os
import re
import traceback

class Template(object):
    

    def __init__(self, template_path, config, cli):

        self.config = config
        self.cli = cli
        
        self.template_path = template_path.replace(self.config['path']['template']+"/", "")
        
        template_filename = os.path.splitext(os.path.basename(self.template_path))[0]
        self.js_name = template_filename+".min.js"
        self.css_name = template_filename+".min.css"
        
        self.content = self.read(template_path)
        
        self.cli.msg(template_path)
        
    def read(self, file_path):
        
        content = ""
        with open(file_path, 'r') as f:
            content = "".join([l for l in f]) # read lines, is memory efficient and fast
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
        
        for script in re.findall('\<script[^>]*></script>',self.content):
            search = re.search('src="(?P<value>[^"]*)"', script)
            if search:
                file_path = self.search_file_path(self.config['pattern']['js'], search.groupdict()['value'])
                if file_path:
                    scripts.append((file_path, script))
        
        return scripts
        
    def get_links(self):
        links = []
        
        for link in re.findall('\<link[^>]*/>',self.content):
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
                self.cli.msg("\t[OK]\t"+script_path, "GREEN")
            except IOError, io:
                self.cli.msg("\t[FAIL]\t"+script_path, "RED")
        
        return "".join(scripts_content)
        
    def get_merged_links(self):
        links = self.get_links()

        links_content = []

        for src, tag in links:
            link_path = os.path.join(self.config.get('path').get('css'), src)
            
            try:
                links_content.append(self.read(link_path))
                self.cli.msg("\t[OK]\t"+link_path, "GREEN")
            except IOError, io:
                self.cli.msg("\t[FAIL]\t"+link_path, "RED")

        return "".join(links_content)
        
    def yuicompressor(self, file_path):
        process = Popen(['yuicompressor', '-o', file_path, file_path], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        
        if not stderr:
            self.cli.msg("\t[OK] "+file_path, "GREEN")
        else:
            self.cli.msg("\t[FAIL] "+file_path, "RED")
            self.cli.error_and_exit(stderr)
    
    def compress_js(self):
        if self.js:
            js_path = os.path.join(self.config['output']['js'], self.js_name)            
            self.write(js_path, self.js)
            self.yuicompressor(js_path)
        
    def compress_css(self):
        if self.css:
            css_path = os.path.join(self.config['output']['css'], self.css_name)
            self.write(css_path, self.css)
            self.yuicompressor(css_path)
            
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