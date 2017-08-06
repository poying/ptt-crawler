import re
from setuptools import setup, find_packages


setup(
    name='ptt_crawler',
    version='2.2.1',
    url='https://github.com/poying/ptt-crawler',
    license='MIT',
    author='Po-Ying Chen, M157q',
    author_email='poying.me@gmail.com',
    packages=find_packages(),
    scripts=['bin/ptt'],
    platforms='any',
    install_requires=[
        'pynsq',
        'clime',
        'tornado',
        'elasticsearch',
        'requests>=2.5.1',
        'beautifulsoup4',
        'python-dateutil',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Traditional)',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
