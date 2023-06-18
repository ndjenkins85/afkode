'''This script helps imports on Pythonista or MacOS'''
try:
    import console
    print("Running on iOS (pythonista)")
    
    import os
    import sys
    sys.path.append(os.path.abspath('..'))
except ModuleNotFoundError:
    print("Running on MacOS (poetry-python)")

