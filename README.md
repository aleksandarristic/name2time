Name2Time
=========

A simple utility to set the modified and accessed timestamps on files according to their filenames.

I've created this little script in order to make my picture collections more sortable. It will timestamp files in a directory tree according to each file's name. It supports various different file extensions with optional prefixes and suffixes. Also, it uses a datetime.datetime.strptime to extract the time from the filename, so it's easily changeable to suit your needs. Out of the box it supports the following:

* prefixes: ['IMG', 'PIC', 'PANO', 'VID'] or no prefix
* file types (extensions): ['.JPG', '.JPEG', '.MP4']
* date format: %Y%m%d_%H%M%S, eg: 20150131_120017


Installation
============

pip install name2time

OR

Clone the project & run from source


Usage
=====

name2timestamp [--fmt FORMAT] [-y or --yes] DIRECTORY


Download
========
* Download from pypi: https://pypi.python.org/pypi/name2time
* Checkout source: https://github.com/aleksandarristic/name2time/
