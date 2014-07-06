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


    def test_get_schedule(self):
    	utils.get_schedule(3)
    

    def test_get_game_threads(self):
    	utils.get_game_threads()


    def test_get_standings(self):
    	utils.get_standings()


if __name__ == '__main__':
    unittest.main()