# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""This script helps imports on Pythonista or MacOS"""
try:
    import console

    print("Running on iOS (pythonista)")

    import os
    import sys

    sys.path.append(os.path.abspath(".."))

    from afkode import utils

    print(utils.get_base_path())
except ModuleNotFoundError:
    print("Running on MacOS (poetry-python)")
    from afkode import utils

    print(utils.get_base_path())
