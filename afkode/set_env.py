# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""This script helps imports on Pythonista or MacOS"""
import logging

try:
    import console
    import os
    import sys
    sys.path.append(os.path.abspath(".."))
    mode = 'Running on iOS (pythonista)'
except ModuleNotFoundError:
    mode = 'Running on MacOS (poetry-python)'
    
from afkode import globals, utils
utils.setup_logging(log_level=globals.LOG_LEVEL)
logging.info(mode)    

