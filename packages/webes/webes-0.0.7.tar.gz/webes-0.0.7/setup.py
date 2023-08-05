#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: two-it2022
:license: Apache License, Version 1.7, see LICENSE file
:copyright: (c) 2022 two-it2022
"""

version = '0.0.7'
'''
with open('__readme__.md', encoding='utf-8') as f:
      long_description = f.read()
'''

long_description = '''Python module for Two It project
                  management platform (TwoIt API wrapper)'''


setup(
      name='webes',
      version=version,

      author='two-it2022',
      author_email='kodland.group@gmail.com',

      description=(
            u'Python module for writing websites.'
            u'Two It 2022 (two-it.netlify.app API wrapper)'
      ),
      long_description=long_description,
      #long_description_content_type='text/markdown',

      url='https://github.com/TwoIt202/Webes',
      download_url='https://github.com/TwoIt202/Webes/raw/6156c6d5a764dba21d6743a90268772df5558fde/webes.zip'.format(
            version
      ),

      license='Apache License, Version 1.7, see LICENSE file',

      packages=['webes'],
      install_requires=['colorama', 'termcolor', 'flask', 'wincom'],

      classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: Implementation :: CPython',
      ]

)