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
import re


class Filter(object):
    def __init__(self, config, template):
        self.config = config
        self.template = template

    def filter_tags(self):
        scripts = self.template.get_scripts()
        links = self.template.get_links()

        script_matches = [match for src, match in scripts]
        link_matches = [match for src, match in links]

        if link_matches:
            css_url = "/".join((self.config['filter']['url']['css'], self.template.css_name))
            self.template.content = re.sub(link_matches.pop(), '<link type="text/css" href="%s" rel="stylesheet" />' % css_url, self.template.content)

        if script_matches:
            js_url = "/".join((self.config['filter']['url']['js'], self.template.js_name))
            self.template.content = re.sub(script_matches.pop(), '<script type="text/javascript" src="%s" ></script>' % js_url, self.template.content)

        # remove as outras
        for match in script_matches + link_matches:
            self.template.content = re.sub(match, "", self.template.content)

    def filter_images(self, content):
        if self.config['pattern'].get('img'):
            return re.sub("%s(?P<img_path>[^\.]*\.(gif|jpeg|png|jpg|swf))" % self.config['pattern']['img'], "%s\g<img_path>" % self.config['filter']['url']['img'], content)

        return content

    def apply(self):
        self.filter_tags()

        self.template.content = self.filter_images(self.template.content)
        self.template.js = self.filter_images(self.template.js)
        self.template.css = self.filter_images(self.template.css)
