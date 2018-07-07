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
from unittest import TestCase
from anime_list_apis.cache.Cache import Cache
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Id import IdType
from anime_list_apis.test.models.TestMediaData import TestMediaData


class TestCacher(TestCase):
    """
    Tests the Cacher
    """

    def setUp(self):
        """
        Creates a cache
        :return: None
        """
        self.tearDown()
        os.makedirs("testdir")
        self.cache = Cache("testdir/.cache")

    def tearDown(self):
        """
        Removes all generated files and directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_generating_new_cache(self):
        """
        Tests creating a new cache in a custom location
        :return: None
        """
        Cache("testdir/testcache")
        self.assertTrue(os.path.isdir("testdir/testcache"))
        self.assertTrue(os.path.isfile("testdir/testcache/cache.json"))

    def test_loading_and_retrieving_cache(self):
        """
        Tests writing some data into the cache and then reloading it
        in a different Cache object
        :return: None
        """
        entry = TestMediaData.generate_sample_anime_data()
        _id = entry.id
        self.cache.add_media_data(IdType.MYANIMELIST, entry)
        self.cache.write()
        new_cache = Cache("testdir/.cache")
        self.assertEqual(
            entry, self.cache.get_media_data(MediaType.ANIME, IdType.MYANIMELIST, _id)
        )
        self.assertEqual(
            entry, new_cache.get_media_data(MediaType.ANIME, IdType.MYANIMELIST, _id)
        )

    def test_retrieving_non_existant_entry(self):
        """
        Tests retrieving an entry from the cache that doesn't exist
        :return: None
        """
        self.assertEqual(
            self.cache.get_media_data(MediaType.ANIME, IdType.ANILIST, 1),
            None
        )

    def test_using_int_instead_of_id_object(self):
        """
        Tests retrieving entries by using ints instead of Id objects
        :return: None
        """
        entry = TestMediaData.generate_sample_anime_data()
        id_obj = entry.id
        id_int = id_obj.get_media_data(IdType.MYANIMELIST)

        self.cache.add_media_data(IdType.MYANIMELIST, entry)

        self.assertEqual(
            self.cache.get_media_data(MediaType.ANIME, IdType.MYANIMELIST, id_int),
            self.cache.get_media_data(MediaType.ANIME, IdType.MYANIMELIST, id_obj)
        )
