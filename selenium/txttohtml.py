#!/usr/bin/env python3
# coding: utf-8
import subprocess

command = '''python markup.py < %s > %s'''

subprocess.call(command % (from_file, to_file), shell=True)
