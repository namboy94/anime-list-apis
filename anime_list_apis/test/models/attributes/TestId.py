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
from anime_list_apis.models.attributes.Id import Id, IdType


class TestId(TestCase):
    """
    Tests the Id Attribute class
    """

    def test_invalid_constructor_parameters(self):
        """
        Tests using invalid parameter types with the constructor
        :return: None
        """
        for parameters in [
            ([],),
            (100,)
        ]:
            try:
                Id(*parameters)
                self.fail()
            except TypeError:
                pass

    def test_fetching_different_id_types(self):
        """
        Tests generating an ID using the constructor and fetching the
        different IDs
        :return: None
        """
        _id = Id({
            IdType.MYANIMELIST: 1,
            IdType.ANILIST: 2,
            IdType.KITSU: 3
        })
        self.assertEqual(1, _id.get(IdType.MYANIMELIST))
        self.assertEqual(2, _id.get(IdType.ANILIST))
        self.assertEqual(3, _id.get(IdType.KITSU))

    def test_unfilled_entries(self):
        """
        Tests that unfilled ID entries lead to Null values for the respective
        IDs
        :return: None
        """
        _id = Id({IdType.MYANIMELIST: 1})
        self.assertEqual(1, _id.get(IdType.MYANIMELIST))
        self.assertEqual(None, _id.get(IdType.ANILIST))
        self.assertEqual(None, _id.get(IdType.KITSU))

    def test_setting_ids(self):
        """
        Tests manually setting IDs after construction
        :return: None
        """
        _id = Id({IdType.MYANIMELIST: 1})
        _id.set(100, IdType.MYANIMELIST)
        _id.set(200, IdType.ANILIST)
        _id.set(300, IdType.KITSU)
        self.assertEqual(100, _id.get(IdType.MYANIMELIST))
        self.assertEqual(200, _id.get(IdType.ANILIST))
        self.assertEqual(300, _id.get(IdType.KITSU))

    def test_setting_invalid_ids(self):
        """
        Tests setting ids that are invalid types
        :return: None
        """
        _id = Id({IdType.MYANIMELIST: 1})

        for value in [None, "100", 100.0, True]:
            try:
                # noinspection PyTypeChecker
                _id.set(value, IdType.ANILIST)
                self.fail()
            except TypeError:
                pass

    def test_no_entries(self):
        """
        Tests that the constructor raises a ValueError when no ID at all is
        provided
        :return: None
        """
        try:
            Id({})
            self.fail()
        except ValueError:
            pass

    def test_no_valid_entries(self):
        """
        Tests that providing None values as the only IDs still result in
        a ValueError
        :return: None
        """
        try:
            # noinspection PyTypeChecker
            Id({IdType.MYANIMELIST: None})
            self.fail()
        except ValueError:
            pass

    def test_serialization(self):
        """
        Tests serializing an ID object
        :return: None
        """
        ob = Id({IdType.MYANIMELIST: 1, IdType.ANILIST: 2})
        data = ob.serialize()

        self.assertEqual(
            data,
            {"MYANIMELIST": 1, "ANILIST": 2, "KITSU": None}
        )

    def test_deserialization(self):
        """
        Tests deserializing an ID object
        :return: None
        """
        self.assertEqual(
            Id.deserialize({"MYANIMELIST": 1, "ANILIST": 2}),
            Id({IdType.MYANIMELIST: 1, IdType.ANILIST: 2})
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        for data in [
            {"A": 1},
            {},
            {"ANILIST": "1"},
            {"Anilist": 1},
            {"ANILIST": None},
            []
        ]:
            try:
                Id.deserialize(data)
                self.fail()
            except (TypeError, ValueError):
                pass

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = Id({IdType.MYANIMELIST: 1, IdType.ANILIST: 2})
        two = Id({IdType.MYANIMELIST: 1, IdType.ANILIST: 2})
        three = Id({IdType.MYANIMELIST: 1})

        self.assertEqual(one, two)
        self.assertNotEqual(two, three)

        self.assertNotEqual(one, "Test")

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        _id = Id({IdType.MYANIMELIST: 1, IdType.ANILIST: 2})
        representation = str(_id)
        serialised = json.loads(representation)
        self.assertEqual(_id, Id.deserialize(serialised))
