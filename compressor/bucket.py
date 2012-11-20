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
import os
import boto


class BucketSync(object):

    def __init__(self, cli, key, secret, bucket_name,
        local_path, bucket_base_path='/', grant='public-read', endpoint='s3.amazonaws.com'):

        self.cli = cli
        self.key = key
        self.secret = secret
        self.bucket_name = bucket_name
        self.grant = grant
        self.bucket_base_path = bucket_base_path.lstrip('/')
        self.local_path = local_path
        self.endpoint = endpoint

    def connect(self):
        self.conn = boto.connect_s3(
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            host=self.endpoint
        )
        self.bucket = self.conn.get_bucket(self.bucket_name)

    def get_remote_keys(self):
        keys = {}
        for key in self.bucket.list(prefix=self.bucket_base_path):
            keys[key.name] = key.size

        return keys

    def get_key_name(self, fullpath):
        key_name = fullpath[len(self.local_path):]
        l = key_name.split(os.sep)
        key_name = '/'.join(l)

        return os.path.join(self.bucket_base_path, key_name.lstrip('/'))

    def upload_file(self, key_name, file_path):
        key = self.bucket.new_key(key_name)
        key.set_contents_from_filename(
            file_path,
            policy=self.grant
        )
        self.cli.msg("\t%s (upload)" % key_name, "GREEN")

    def sync(self):

        self.cli.msg("\tBucketSync start ...")
        self.connect()
        keys = self.get_remote_keys()

        for root, dirs, files in os.walk(self.local_path):

            for fname in files:
                file_path = os.path.join(root, fname)
                key_name = self.get_key_name(file_path)

                if key_name in keys:
                    filesize = os.path.getsize(file_path)
                    if filesize == keys[key_name]:
                        self.cli.msg("\t%s (size matched)" % key_name)
                        continue

                self.upload_file(key_name, file_path)
