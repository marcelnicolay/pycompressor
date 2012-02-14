from compressor.minifier.js import jsmin
from compressor.minifier.css import minimalize
import os
import re

class Template(object):
    

    def __init__(self, template_path, config, cli):

        self.config = config
        self.cli = cli
        
        self.template_path = template_path.replace(self.config['path']['template']+"/", "")
        
        template_filename = os.path.splitext(os.path.basename(self.template_path))[0]
        self.js_name = template_filename+".min.js"
        self.css_name = template_filename+".min.css"
        
        self.content = self.read(template_path)
        
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
            
    def get_scripts(self):
        scripts = []
        
        for script in re.findall('\<script[^>]*></script>',self.content):
            search = re.search('src="(?P<value>[^"]*)"', script)
            if search and self.config.get('pattern').get('js') in search.groupdict()['value']:
                src = search.groupdict()['value'].replace(self.config['pattern']['js'] + '/', '')
                scripts.append((src, script))
        
        return scripts
        
    def get_links(self):
        links = []
        
        for link in re.findall('\<link[^>]*/>',self.content):
            search = re.search('href="(?P<value>[^"]*)"', link)	
            if search and self.config.get('pattern').get('css') in search.groupdict()['value']:
                src = search.groupdict()['value'].replace(self.config['pattern']['css'] + '/', '')
                links.append((src, link))
        
        return links

    def compress_scripts(self):
        scripts = self.get_scripts()
        
        scripts_content = []
        
        for src, tag in scripts:
            script_path = os.path.join(self.config.get('path').get('js'), src)
            
            try:
                scripts_content.append(self.read(script_path))
                self.cli.msg("[OK]\t"+script_path)
            except IOError, io:
                self.cli.msg("[FAIL]\t"+script_path, "RED")
        
        return jsmin("".join(scripts_content))
        
    def compress_links(self):
        links = self.get_links()

        links_content = []

        for src, tag in links:
            link_path = os.path.join(self.config.get('path').get('css'), src)
            
            try:
                links_content.append(self.read(link_path))
                self.cli.msg("[OK]\t"+link_path)
            except IOError, io:
                self.cli.msg("[FAIL]\t"+link_path, "RED")

        return minimalize("".join(links_content))
        
    def filter_tags(self):
        scripts = self.get_scripts()
        links = self.get_links()
        
        script_matches = [match for src,match in scripts]
        link_matches = [match for src,match in links]
        
        if link_matches:
            css_url = "/".join((self.config['filter']['url']['css'], self.css_name))
            self.content = re.sub(link_matches.pop(), '<link type="text/css" href="%s" rel="stylesheet" />' % css_url, self.content)

        if script_matches:
            js_url = "/".join((self.config['filter']['url']['js'], self.js_name))
            self.content = re.sub(script_matches.pop(), '<script type="text/javascript" src="%s" ></script>' % js_url, self.content)
        
        # remove as outras
        for match in script_matches + link_matches:
            self.content = re.sub(match, "", self.content)
        
    def filter(self):
        
        # get compressed files
        js_minified = self.compress_scripts()
        css_minified = self.compress_links()

        # write css and js
        if js_minified:
            self.write(os.path.join(self.config['output']['js'], self.js_name), js_minified)
        if css_minified:
            self.write(os.path.join(self.config['output']['css'], self.css_name), css_minified)
        
        # filter tags in template content
        self.filter_tags()
        self.write(os.path.join(self.config['output']['template'], self.template_path), self.content)