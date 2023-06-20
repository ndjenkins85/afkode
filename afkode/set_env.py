# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""This script helps imports on Pythonista or MacOS"""
import logging
import os
import sys

try:
    import console

    sys.path.append(os.path.abspath(".."))
    mode = "Running on iOS (pythonista)"
except ModuleNotFoundError:
    import importlib_resources

    folder_parts = importlib_resources.files("afkode").parts
    if "site-packages" in folder_parts:
        mode = "Running on MacOS as installed software"
    else:
        mode = "Running on MacOS (poetry-python)"

from afkode import globals, utils

utils.setup_logging(log_level=globals.LOG_LEVEL)
logging.info(mode)
