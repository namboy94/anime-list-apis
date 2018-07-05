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

from unittest import TestCase
from anime_list_apis.models.attributes.Title import Title, TitleType


class TestTitle(TestCase):
    """
    Test the Title Attribute class
    """

    def test_title_construction(self):
        """
        Tests constructing the title
        :return: None
        """
        title = Title({
            TitleType.ROMAJI: "Shingeki no Kyojin",
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.NATIVE: "進撃の巨人"
        })  # Default = ROMAJI

        self.assertEqual(title.get(), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.ENGLISH), "Attack on Titan")
        self.assertEqual(title.get(TitleType.ROMAJI), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.NATIVE), "進撃の巨人")

    def test_missing_entries(self):
        """
        Tests that missing title entries are replaced with None.
        :return: None
        """
        title = Title({TitleType.ROMAJI: "Shingeki no Kyojin"})
        self.assertEqual(title.get(TitleType.ROMAJI), "Shingeki no Kyojin")
        self.assertEqual(title.get(TitleType.ENGLISH), None)
        self.assertEqual(title.get(TitleType.NATIVE), None)

    def test_changing_default_title_type(self):
        """
        Tests changing the default title type
        :return: None
        """
        title = Title({
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.ROMAJI: "Shingeki no Kyojin"
        }, default=TitleType.ENGLISH)
        self.assertEqual(title.get(), "Attack on Titan")

    def test_automatically_changing_default_title_type(self):
        """
        Tests changing the default title type by ot supplying the default
        title type.
        :return: None
        """
        title = Title({
            TitleType.ENGLISH: "Attack on Titan",
            TitleType.NATIVE: "進撃の巨人"
        })
        self.assertEqual(title.default, TitleType.ENGLISH)
        title = Title({
            TitleType.NATIVE: "進撃の巨人"
        })
        self.assertEqual(title.default, TitleType.NATIVE)
