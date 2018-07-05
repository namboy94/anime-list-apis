"""LICENSE
Copyright 2018 Hermann Krumrey <hermann@krumreyh.com>

This file is part of anime-list-apis.

anime-list-apis is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

anime-list-apis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with anime-list-apis.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import json
from unittest import TestCase
from anime_list_apis.models.attributes.Date import Date


class TestDate(TestCase):
    """
    Tests the Date Attribute class
    """

    def test_invalid_constructor_parameters(self):
        """
        Tests using invalid parameter types with the constructor
        :return: None
        """
        for parameters in [
            (1, 1, None),
            (1, None, 1),
            (None, 1, 1),
            ("", 1, 1),
            (True, 1, 1)
        ]:
            try:
                Date(*parameters)
                self.fail()
            except TypeError:
                pass

    def test_serialization(self):
        """
        Tests serializing a Date object
        :return: None
        """
        ob = Date(2018, 1, 2)
        data = ob.serialize()

        self.assertEqual(
            data,
            {"year": 2018, "month": 1, "day": 2}
        )

    def test_deserialization(self):
        """
        Tests deserializing a Date object
        :return: None
        """
        self.assertEqual(
            Date.deserialize({"year": 2018, "month": 1, "day": 2}),
            Date(2018, 1, 2)
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        for data in [
            {"year": 2018, "month": 1, "day": None},
            {"year": None, "month": 1, "day": 2},
            {"year": 2018, "month": None, "day": 2},
            {"year": 2018, "month": 1},
            {"year": 2018, "day": 2},
            {"month": 1, "day": 2},
            []
        ]:
            try:
                Date.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = Date(2018, 1, 2)
        two = Date(2018, 1, 2)
        three = Date(2018, 2, 2)
        four = Date(2018, 1, 1)
        five = Date(2017, 1, 2)

        self.assertNotEqual(one, "Test")
        self.assertEqual(one, two)
        self.assertNotEqual(two, three)
        self.assertNotEqual(two, four)
        self.assertNotEqual(two, five)
        self.assertNotEqual(three, four)
        self.assertNotEqual(four, five)
        self.assertNotEqual(three, five)

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        date = Date(2018, 1, 2)
        representation = str(date)
        serialised = json.loads(representation)
        self.assertEqual(date, Date.deserialize(serialised))
