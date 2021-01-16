# https://github.com/pytest-dev/pytest/issues/2421
from __future__ import absolute_import

import os
import sys

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app
