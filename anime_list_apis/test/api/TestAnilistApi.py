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
from unittest import TestCase, mock, skip
from anime_list_apis.cache.Cacher import Cacher
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.AnimeData import AnimeData
from anime_list_apis.models.AnimeListEntry import AnimeListEntry
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.Title import TitleType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.WatchingStatus import WatchingStatus


@skip
class TestAnilistApi(TestCase):
    """
    Tests the Anilist API Wrapper
    """

    def setUp(self):
        """
        Creates a cache
        :return: None
        """
        self.tearDown()
        os.makedirs("testdir")
        self.cache = Cacher("testdir/.cache")
        self.api = AnilistApi(cache=self.cache)

    def tearDown(self):
        """
        Removes all generated files and directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_retrieving_anime_data(self):
        """
        Tests retrieving a single anime data entry
        :return: None
        """
        entry = self.api.get(MediaType.ANIME, Id({IdType.ANILIST: 1}))
        self.assertEqual(entry.id.get(IdType.ANILIST), 1)
        self.assertEqual(entry.title.get(TitleType.ENGLISH), "Cowboy Bebop")
        self.assertTrue(isinstance(entry, AnimeData))

    def test_retrieving_anime_data_using_mal_id(self):
        """
        Tests retrieving a single anime data entry using a myanimelist ID
        :return: None
        """
        entry = self.api.get(MediaType.ANIME, Id({IdType.MYANIMELIST: 1}))
        self.assertEqual(entry.id.get(IdType.MYANIMELIST), 1)
        self.assertEqual(entry.title.get(TitleType.ENGLISH), "Cowboy Bebop")
        self.assertTrue(isinstance(entry, AnimeData))

    def test_get_anime_shortcut(self):
        """
        Tests that the get_anime shortcut method works as expected
        :return: None
        """
        long = self.api.get(MediaType.ANIME, Id({IdType.ANILIST: 1}))
        short = self.api.get_anime(Id({IdType.ANILIST: 1}))
        self.assertEqual(long, short)

    def test_getting_anime_with_int_id(self):
        """
        Tests retrieving an anime using an integer instead of an Id object
        :return: None
        """
        long = self.api.get(MediaType.ANIME, Id({IdType.ANILIST: 1}))
        short = self.api.get(MediaType.ANIME, 1)
        self.assertEqual(long, short)

    def test_retrieving_user_anime_entries(self):
        """
        Tests retrieving all entries in a user's anime list
        :return: None
        """
        entries = self.api.get_list(MediaType.ANIME, "namboy94")
        self.assertLess(0, len(entries))
        list(map(
            lambda x: self.assertEqual(MediaType.ANIME, x.media_type),
            entries
        ))
        list(map(
            lambda x: self.assertTrue(isinstance(x, AnimeListEntry)),
            entries
        ))

    def test_retrieving_anime_list_shortcut(self):
        """
        Tests the get_anime_list() shortcut method
        :return: None
        """
        long = self.api.get_list(MediaType.ANIME, "namboy94")
        short = self.api.get_anime_list("namboy94")
        self.assertEqual(long, short)

    def test_retrieving_single_user_entry(self):
        """
        Tests retrieving a single user entry
        :return: None
        """
        entry = self.api.get(
            MediaType.ANIME, Id({IdType.ANILIST: 9253}), username="namboy94"
        )
        self.assertEqual(entry.id.get(IdType.ANILIST), 9253)
        self.assertEqual(entry.username, "namboy94")
        self.assertEqual(entry.watching_status, WatchingStatus.COMPLETED)

    def test_retrieving_nonexistant_user_entry(self):
        """
        Tests fetching an entry that is not in a user's list
        :return:
        """
        entry = self.api.get(
            MediaType.ANIME, Id({IdType.ANILIST: 9253}), username="namboy94"
        )
        self.assertEqual(entry, None)

    def test_caching(self):
        """
        Tests that the caching works correctly
        :return: None
        """
        fetched = self.api.get(MediaType.ANIME, Id({IdType.ANILIST: 1}))
        cached = self.cache.get(MediaType.ANIME, IdType.ANILIST, 1)
        self.assertEqual(fetched, cached)

        def raise_value_error():
            raise ValueError()

        # Makes sure that cached value is used from now on
        with mock.patch("requests.post", new=raise_value_error):
            new_fetched = self.api.get(
                MediaType.ANIME, Id({IdType.ANILIST: 1})
            )
            self.assertEqual(new_fetched, cached)
