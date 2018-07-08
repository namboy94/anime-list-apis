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
from anime_list_apis.models.attributes.Title import Title, TitleType


class TestTitle(TestCase):
    """
    Tests the Title Attribute class
    """

    def test_invalid_constructor_parameters(self):
        """
        Tests using invalid parameter types with the constructor
        :return: None
        """
        for parameters in [
            (True,),
            (None,),
            ({}, 1),
            ({}, None)
        ]:
            try:
                Title(*parameters)
                self.fail()
            except TypeError:
                pass

    def test_title_construction(self):
        """
        Tests constructing the title
        :return: None
        """
        title = Title({
            TitleType.ROMAJI: "Shingeki no Kyojin",
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.JAPANESE: "進撃の巨人"
        })  # Default = ROMAJI

        self.assertEqual(title.get(), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.ENGLISH), "Attack on Titan")
        self.assertEqual(title.get(TitleType.ROMAJI), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.JAPANESE), "進撃の巨人")

    def test_missing_entries(self):
        """
        Tests that missing title entries are replaced with None.
        :return: None
        """
        title = Title({TitleType.ROMAJI: "Shingeki no Kyojin"})
        self.assertEqual(title.get(TitleType.ROMAJI), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.ENGLISH), None)
        self.assertEqual(title.get(TitleType.JAPANESE), None)

    def test_no_entries(self):
        """
        Tests that at least on title is required during initialization
        :return: None
        """
        try:
            Title({})
            self.fail()
        except ValueError:
            pass

    def test_setting_titles(self):
        """
        Tests manually setting title values
        :return: None
        """
        title = Title({TitleType.ROMAJI: "Shingeki no Kyojin"})
        self.assertEqual(title.get(TitleType.ROMAJI), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.ENGLISH), None)
        self.assertEqual(title.get(TitleType.JAPANESE), None)

        title.set("Attack on Titan", TitleType.ENGLISH)
        title.set("進撃の巨人", TitleType.JAPANESE)

        self.assertEqual(title.get(TitleType.ENGLISH), "Attack on Titan")
        self.assertEqual(title.get(TitleType.ROMAJI), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.JAPANESE), "進撃の巨人")

        title.set("AAAAA", TitleType.ROMAJI)
        self.assertEqual(title.get(), "AAAAA")

    def test_setting_titles_with_invalid_types(self):
        """
        Tests that invalid types in title setting parameters raise a TypeError
        :return: None
        """
        title = Title({TitleType.ROMAJI: "Shingeki no Kyojin"})

        for value in [None, 1, 1.1, True]:
            try:
                # noinspection PyTypeChecker
                title.set(value, TitleType.ROMAJI)
                self.fail()
            except TypeError:
                pass

    def test_different_default_title_type(self):
        """
        Tests using a different title type
        :return: None
        """
        title = Title({
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.ROMAJI: "Shingeki no Kyojin"
        }, default=TitleType.ENGLISH)
        self.assertEqual(title.default, TitleType.ENGLISH)

    def test_automatically_using_different_default_title_type(self):
        """
        Tests changing the default title type by not supplying the default
        title type.
        :return: None
        """
        title = Title({
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.JAPANESE: "進撃の巨人"
        })
        self.assertEqual(title.default, TitleType.ENGLISH)
        title = Title({
            TitleType.JAPANESE: "進撃の巨人"
        })
        self.assertEqual(title.default, TitleType.JAPANESE)

    def test_changing_default_title_type(self):
        """
        Tests changing the default title type
        :return: None
        """
        title = Title({
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.ROMAJI: "Shingeki no Kyojin"
        })
        self.assertEqual(title.default, TitleType.ROMAJI)
        title.change_default_title_type(TitleType.ENGLISH)
        self.assertEqual(title.default, TitleType.ENGLISH)

    def test_changing_default_invalid_title_type(self):
        """
        Tests changing the default title type with an invalid title type
        :return: None
        """
        title = Title({
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.ROMAJI: "Shingeki no Kyojin"
        })
        try:
            title.change_default_title_type(TitleType.JAPANESE)
            self.fail()
        except ValueError:
            pass

    def test_serialization(self):
        """
        Tests serializing an ID object
        :return: None
        """
        ob = Title({TitleType.ROMAJI: "SnK", TitleType.ENGLISH: "AoT"})
        data = ob.serialize()

        self.assertEqual(
            data,
            {
                "ROMAJI": "SnK",
                "ENGLISH": "AoT",
                "JAPANESE": None,
                "default": "ROMAJI"
            }
        )

    def test_deserialization(self):
        """
        Tests deserializing an ID object
        :return: None
        """
        data = {"ROMAJI": "SnK", "ENGLISH": "AoT", "default": "ENGLISH"}
        self.assertEqual(
            Title.deserialize(data),
            Title(
                {TitleType.ROMAJI: "SnK", TitleType.ENGLISH: "AoT"},
                default=TitleType.ENGLISH
            )
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        for data in [
            {"A": 1},
            {"ROMAJI": "Hello"},
            {"ANILIST": "1", "default": "ROMAJI"},
            {"ROMAJI": 1, "default": "ROMAJI"},
            {"ROMAJI": None, "default": "ROMAJI"},
            {"Romaji": "Hello", "default": "ROMAJI"},
            []
        ]:
            try:
                Title.deserialize(data)
                self.fail()
            except (TypeError, ValueError):
                pass

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = Title({TitleType.ROMAJI: "SnK", TitleType.ENGLISH: "AoT"})
        two = Title({TitleType.ROMAJI: "SnK", TitleType.ENGLISH: "AoT"})
        three = Title({TitleType.ROMAJI: "SnK", TitleType.ENGLISH: "AoT"},
                      default=TitleType.ENGLISH)
        four = Title({TitleType.ENGLISH: "AoT"})

        self.assertEqual(one, two)
        self.assertNotEqual(two, three)
        self.assertNotEqual(two, four)
        self.assertNotEqual(three, four)

        three.change_default_title_type(TitleType.ROMAJI)

        self.assertEqual(two, three)
        self.assertNotEqual(three, four)

        self.assertNotEqual(one, "Test")

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        title = Title({TitleType.ROMAJI: "SnK", TitleType.ENGLISH: "AoT"})
        representation = str(title)
        serialised = json.loads(representation)
        self.assertEqual(title, title.deserialize(serialised))
