#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests
--------------

Tests for the `searchfda` module.

"""
import unittest

import utils

class SearchNBATest(unittest.TestCase):
    def test_fetch_openfda(self):
    	utils.fetch_openfda()


    def test_fetch_search(self):
    	utils.fetch_search("search")


    def test_fetch_results(self):
    	utils.fetch_results("search","category","view")


if __name__ == '__main__':
    unittest.main()
