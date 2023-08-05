"""Main TUI implementation for yeectl

Author: Bean Robinson  
Created: 
"""

import os
import py_cui
import yeelight
from yeectl import findBulbs, YeectlApp

__version__ = 'v0.0.1'

def main():
    root = py_cui.PyCUI(3, 5)
    wrapper =  YeectlApp(root)
    root.set_title('YEECTL')
    root.toggle_unicode_borders()
    root.start()
