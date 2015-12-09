#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rs_data_readers.skeleton import fib

__author__ = "Andreea Plocon"
__copyright__ = "Andreea Plocon"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
