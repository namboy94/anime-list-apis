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

import os
import shutil
from unittest import TestCase, mock

from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.cache.Cacher import Cacher
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType


class TestAnilistApi(TestCase):
    """
    Tests the Anilist Api.
    May be subclassed to test other APIs as well
    """

    api_class = AnilistApi
    """
    The API class to test
    """

    primary_id_type = IdType.ANILIST
    """
    The primary ID type
    """

    valid_id_types = [IdType.ANILIST, IdType.MYANIMELIST]
    """
    A list of valid ID types
    """

    def setUp(self):
        """
        Creates a cache
        :return: None
        """
        self.tearDown()
        os.makedirs("testdir")
        self.cache = Cacher("testdir/.cache")
        self.api = self.api_class(cache=self.cache)

    def tearDown(self):
        """
        Removes all generated files and directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_retrieving_anime_data(self):
        """
        Tests retrieving a single anime data entry using different methods
        ID 1, Cowboy Bebop will be used here, since its ID is the same
        across Myanimelist, Anilist and Kitsu
        :return: None
        """
        entries = []
        for id_type in self.valid_id_types:
            _id = Id({id_type: 1})

            entries.append(self.api.get_data(MediaType.ANIME, _id))
            entries.append(self.api.get_anime_data(_id))

        entries.append(self.api.get_data(MediaType.ANIME, 1))
        entries.append(self.api.get_anime_data(1))

        for entry in entries:
            for compared in entries:
                self.assertEqual(entry, compared)

    def test_retrieving_invalid_anime_entry(self):
        """
        Tests retrieving invalid anime entries
        Assumptions: No ids < 0 or > 1000000000
        :return: None
        """
        for _id in [-1, 1000000000]:
            self.assertIsNone(self.api.get_anime_data(_id))

    def test_retrieving_single_anime_list_entry(self):
        """
        Tests retrieving a single anime list entry
        :return: None
        """
        steins_gate_id = Id({
            IdType.KITSU: 5646,
            IdType.MYANIMELIST: 9253,
            IdType.ANILIST: 9253
        })

        entries = []

        for id_type in self.valid_id_types:
            _id = steins_gate_id.get(id_type)
            entries.append(
                self.api.get_list_entry(MediaType.ANIME, _id, "namboy94")
            )
            entries.append(self.api.get_anime_list_entry(_id, "namboy94"))

        entries.append(self.api.get_list_entry(
            MediaType.ANIME, steins_gate_id, "namboy94"
        ))
        entries.append(self.api.get_anime_list_entry(
            steins_gate_id, "namboy94"
        ))

        for entry in entries:
            for compared in entries:
                self.assertEqual(entry, compared)

    def test_retrieving_non_existant_anime_list_entry(self):
        """
        Tests retrieving entries that are not in a user's list
        :return: None
        """
        mars_of_destruction_id = Id({
            IdType.KITSU: 378,
            IdType.MYANIMELIST: 413,
            IdType.ANILIST: 413
        })
        self.assertIsNone(self.api.get_anime_list_entry(
            mars_of_destruction_id, "namboy94"
        ))

    def test_retrieving_anime_entry_for_non_existant_user(self):
        """
        Tests retrieving an entry for a non-existant user
        :return: None
        """
        self.assertIsNone(self.api.get_anime_list_entry(1, ""))

    def test_retrieving_anime_list(self):
        """
        Tests retrieving a user's anime list using various methods
        :return: None
        """
        normal = self.api.get_list(MediaType.ANIME, "namboy94")
        short = self.api.get_anime_list("namboy94")
        self.assertEqual(normal, short)
        self.assertLess(10, len(normal))

    def test_retrieving_anime_list_for_nonexistant_user(self):
        """
        Tests retrieving an anime list for an invalid user
        :return: None
        """
        self.assertEqual([], self.api.get_anime_list(""))

    def test_caching_anime(self):
        """
        Tests that the caching works correctly for anime data
        :return: None
        """
        fetched = self.api.get_anime_data(1)
        cached = self.cache.get(MediaType.ANIME, self.primary_id_type, 1)
        self.assertEqual(fetched, cached)

        def raise_value_error():
            raise ValueError()

        # Makes sure that cached value is used from now on
        with mock.patch("requests.post", new=raise_value_error):
            with mock.patch("requests.get", new=raise_value_error):
                new_fetched = self.api.get_anime_data(1)
                self.assertEqual(new_fetched, cached)
