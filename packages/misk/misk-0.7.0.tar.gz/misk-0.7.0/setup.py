#!/usr/bin/env python3
# This file is a part of misk and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/misk/blob/master/LICENSE.txt for the full license text.
# SPDX-License-Identifier: MIT

# set up based on this: https://thucnc.medium.com/how-to-publish-your-own-python-package-to-pypi-4318868210f9
# windows:
# py setup.py sdist bdist_wheel && twine upload dist/* && rmdir /S /Q dist

from setuptools import setup, find_packages

README = ''
with open('README.md', encoding='utf-8') as file:
	README = file.read()

CHANGELOG = ''
with open('CHANGELOG.md', encoding='utf-8') as file:
	CHANGELOG = file.read().strip()

setup_args = dict(
	name=r'misk',
	version=r'0.7.0',
	description=r'Miscellaneous useful bits for python 3.',
	long_description_content_type=r'text/markdown',
	long_description=f'{README}\n\n{CHANGELOG}'.strip(),
	license=r'MIT',
	packages=find_packages(),
	author=r'Mark Gillard',
	author_email=r'mark.gillard@outlook.com.au',
	keywords=['utilities'], # ???
	url=r'https://github.com/marzer/misk',
	download_url=r'https://pypi.org/project/misk/',
	project_urls={
		r'Source': r'https://github.com/marzer/misk',
		r'Tracker': r'https://github.com/marzer/misk/issues'
	},
	python_requires=r'>=3'
)

install_requires = None
with open('requirements.txt', encoding='utf-8') as file:
	install_requires = file.read().strip().split()

if __name__ == '__main__':
	setup(**setup_args, install_requires=install_requires)
