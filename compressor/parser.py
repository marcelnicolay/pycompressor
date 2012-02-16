# encoding: utf-8
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