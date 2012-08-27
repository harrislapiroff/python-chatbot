#!/usr/bin/env python

import os
from setuptools import setup, find_packages

version = __import__('chatbot').VERSION

setup(
		name='chatbot',
		version='.'.join([str(v) for v in version]),
		description='Extensible IRC chatbot written in python.',
		license='BSD',
		packages=find_packages(),
		include_package_data=True,
		zip_safe=False,
		install_requires=[
			'twisted',
		],
	)
