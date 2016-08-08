#!/usr/bin/env python3

"""Tests for the elementbase class"""

import unittest

from namedstruct.elementbase import ElementBase


# pylint: disable=line-too-long,invalid-name
class TestElementBase(unittest.TestCase):
    """ElementBase module tests"""

    def test_valid(self):
        """Test field formats that are valid ElementBase elements."""

        test_fields = [
            ('a', 'b'),     # signed byte: -128, 127
            ('b', 'H'),     # unsigned short: 0, 65535
            ('c', '10s'),   # 10 byte string
            ('d', 'L'),     # unsigned long: 0, 2^32-1
            ('e', '?'),     # bool: 0, 1
        ]

        for field in test_fields:
            with self.subTest(field):  # pylint: disable=no-member
                out = ElementBase.valid(field)
                self.assertTrue(out)

    def test_not_valid(self):
        """Test field formats that are not valid ElementBase elements."""

        test_fields = [
            ('a', '4x'),    # 4 pad bytes
            ('b', 'z'),     # invalid
            ('c', '1'),     # invalid
            ('d', '9S'),    # invalid (must be lowercase)
            ('e', '/'),     # invalid
        ]

        for field in test_fields:
            with self.subTest(field):  # pylint: disable=no-member
                out = ElementBase.valid(field)
                self.assertFalse(out)
