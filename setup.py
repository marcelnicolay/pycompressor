# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from compressor import __version__

setup(
    name = 'compressor',
    version = __version__,
    description = "compressor",
    long_description = open('README.md').read(),
    keywords = ['compressor'],
    author = 'Marcel Nicolay',
    author_email = 'marcel.nicolay@gmail.com',
    url = 'http://github.com/marcelnicolay/pycompressor',
    license = 'OSI',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Natural Language :: English',
                   'Natural Language :: Portuguese (Brazilian)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   ],
    requires=['PyYAML'],
    packages = find_packages(),
    package_dir = {"compressor": "compressor"},
    include_package_data = True,
    test_suite="nose.collector",
    entry_points = {
        'console_scripts': [
            'compressor = compressor.runner:run',
        ],
    },
    
)
