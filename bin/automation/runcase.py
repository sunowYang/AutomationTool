#! /usr/bin/env
#! coding=utf8

import sys
import os


# ********************************Get executing path******************************
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(__file__)
# ********************************************************************************


def run(*kwargs):
    pass


if __name__ == '__main__':
    run(sys[1:])
