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
from anime_list_apis.models.attributes.Id import Id, IdType


class TestId(TestCase):
    """
    Test the Id Attribute class
    """

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
        _id.set(IdType.MYANIMELIST, 100)
        _id.set(IdType.ANILIST, 200)
        _id.set(IdType.KITSU, 300)
        self.assertEqual(100, _id.get(IdType.MYANIMELIST))
        self.assertEqual(200, _id.get(IdType.ANILIST))
        self.assertEqual(300, _id.get(IdType.KITSU))

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
