# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""This script helps imports on Pythonista or MacOS"""
import logging

try:
    import console
    import os
    import sys
    sys.path.append(os.path.abspath(".."))
    from afkode import utils
    utils.setup_logging()
    logging.info('Running on iOS (pythonista)')
except ModuleNotFoundError:
    from afkode import utils
    utils.setup_logging()
    logging.info('Running on MacOS (poetry-python)')
