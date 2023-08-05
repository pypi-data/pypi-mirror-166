# encoding: utf-8
# SPDX-License-Identifier: LGPL-3.0-only

"""
A tiny compatibility module for cross-Python2/3 code.
"""

from .__dataclass_attrs import *
from .__py_ver import *
from .__str import *


__version_info__ = (1, 2, 0)
__version__ = ".".join(str(x) for x in __version_info__)

__pypi_package__ = "darlog-py23"
__url__ = "https://github.com/Lex-DRL/darlog-py23"
__uri__ = __url__

__author__ = 'Lex Darlog (Lex-DRL)'

__license__ = "LGPL-3.0-only"
__copyright__ = "Copyright (c) 2022 Lex Darlog"
