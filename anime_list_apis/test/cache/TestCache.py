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
import time
import shutil
from unittest import TestCase
from anime_list_apis.cache.Cache import Cache
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Id import IdType, Id
from anime_list_apis.test.models.TestMediaData import TestMediaData
from anime_list_apis.test.models.TestMediaListEntry import TestMediaListEntry
from anime_list_apis.test.models.TestMediaUserData import TestMediaUserData


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
        entry = TestMediaListEntry.generate_sample_anime_entry()
        one = entry.id
        two = Id({IdType.MYANIMELIST: 2})
        user = entry.username

        self.cache.add(IdType.MYANIMELIST, entry.get_media_data())
        self.cache.add(IdType.MYANIMELIST, entry.get_user_data())

        entry.id = two
        self.cache.add(IdType.MYANIMELIST, entry)

        self.cache.write()
        new_cache = Cache("testdir/.cache")

        for cache in [self.cache, new_cache]:
            for _id in [one, two]:
                entry.id = _id
                self.assertEqual(
                    cache.get_media_data(
                        IdType.MYANIMELIST, MediaType.ANIME, _id
                    ),
                    entry.get_media_data()
                )
                self.assertEqual(
                    cache.get_media_user_data(
                        IdType.MYANIMELIST, MediaType.ANIME, _id, user
                    ),
                    entry.get_user_data()
                )
                self.assertEqual(
                    cache.get_media_list_entry(
                        IdType.MYANIMELIST, MediaType.ANIME, _id, user
                    ),
                    entry
                )

    def test_reloading(self):
        """
        Tests reloading the cache
        :return: None
        """
        cache = Cache(self.cache.cache_location)
        entry = TestMediaListEntry.generate_sample_anime_entry()
        _id, user, media = entry.id, entry.username, entry.media_type
        site = IdType.MYANIMELIST

        cache.add(site, entry)
        cache.write()
        self.assertIsNone(self.cache.get_media_list_entry(
            site, media, _id, user
        ))
        self.assertIsNotNone(cache.get_media_list_entry(
            site, media, _id, user
        ))

        self.cache.load()

        self.assertIsNotNone(self.cache.get_media_list_entry(
            site, media, _id, user
        ))

    def test_retrieving_non_existant_data(self):
        """
        Tests retrieving an entry from the cache that doesn't exist
        :return: None
        """
        self.assertIsNone(self.cache.get_media_data(
            IdType.MYANIMELIST, MediaType.ANIME, 1
        ))
        self.assertIsNone(self.cache.get_media_user_data(
            IdType.MYANIMELIST, MediaType.ANIME, 1, ""
        ))
        self.assertIsNone(self.cache.get_media_list_entry(
            IdType.MYANIMELIST, MediaType.ANIME, 1, ""
        ))

    def test_getting_from_other_site_type(self):
        """
        Tests that it's not possible to get an entry from another site
        :return: None
        """
        entry = TestMediaListEntry.generate_sample_manga_entry()
        _id, user, media = entry.id, entry.username, entry.media_type
        site = IdType.MYANIMELIST

        self.cache.add(site, entry)
        self.assertIsNotNone(
            self.cache.get_media_list_entry(site, media, _id, user)
        )
        self.assertIsNone(
            self.cache.get_media_list_entry(IdType.KITSU, media, _id, user)
        )

    def test_using_int_or_id_object(self):
        """
        Tests retrieving entries by using ints and Id objects interchangeably
        :return: None
        """
        anime = TestMediaUserData.generate_sample_anime_user_data()
        manga = TestMediaUserData.generate_sample_manga_user_data()
        anime_int = anime.id.get(IdType.MYANIMELIST)
        manga_int = manga.id.get(IdType.MYANIMELIST)
        site = IdType.MYANIMELIST

        self.cache.add(site, anime)
        self.cache.add(site, manga)

        self.assertEqual(
            self.cache.get_media_user_data(
                site, MediaType.ANIME, anime_int, anime.username
            ),
            anime
        )
        self.assertEqual(
            self.cache.get_media_user_data(
                site, MediaType.ANIME, anime.id, anime.username
            ),
            anime
        )
        self.assertEqual(
            self.cache.get_media_user_data(
                site, MediaType.MANGA, manga_int, manga.username
            ),
            manga
        )
        self.assertEqual(
            self.cache.get_media_user_data(
                site, MediaType.MANGA, manga.id, manga.username
            ),
            manga
        )

    def test_lifetime(self):
        """
        Tests the lifetime of cache entries
        :return: None
        """
        cache = Cache(self.cache.cache_location, expiration=0)
        entry = TestMediaListEntry.generate_sample_anime_entry()
        _id, user, media = entry.id, entry.username, entry.media_type
        site = IdType.MYANIMELIST

        # Immediately Deleted
        cache.add(site, entry)
        self.assertIsNone(cache.get_media_list_entry(site, media, _id, user))

        # Deleted after one second
        cache = Cache(self.cache.cache_location, expiration=1)
        cache.add(site, entry)
        self.assertIsNotNone(
            cache.get_media_list_entry(site, media, _id, user)
        )
        time.sleep(1)
        self.assertIsNone(cache.get_media_list_entry(site, media, _id, user))

        # Test that updating works
        cache.add(site, entry)
        self.assertIsNotNone(
            cache.get_media_list_entry(site, media, _id, user)
        )
        time.sleep(0.7)
        self.assertIsNotNone(
            cache.get_media_list_entry(site, media, _id, user)
        )
        cache.add(site, entry)  # Update
        time.sleep(0.7)
        self.assertIsNotNone(
            cache.get_media_list_entry(site, media, _id, user)
        )
        time.sleep(1)
        self.assertIsNone(cache.get_media_list_entry(site, media, _id, user))

    def test_autowrite(self):
        """
        Tests the automatic writing of the cache after
        x amount of added entries
        :return: None
        """
        cache = Cache(self.cache.cache_location, write_after=0)
        entry = TestMediaListEntry.generate_sample_anime_entry()
        _id, user, media = entry.id, entry.username, entry.media_type
        site = IdType.MYANIMELIST

        cache.add(site, entry)
        new_cache = Cache(self.cache.cache_location)
        self.assertIsNotNone(new_cache.get_media_list_entry(
            site, media, _id, user
        ))

    def test_delayed_autowrite(self):
        """
        Tests that cache data is written to file automatically after
        a certain amount of added entries
        :return: None
        """
        entry_count = 10
        cache = Cache(self.cache.cache_location, write_after=entry_count)
        data = TestMediaData.generate_sample_anime_data()
        _id, media, site = data.id, data.media_type, IdType.MYANIMELIST

        def add_and_check(invalid: bool):
            cache.add(site, data)
            new_cache = Cache(self.cache.cache_location)
            self.assertEqual(
                new_cache.get_media_data(site, media, _id) is None,
                invalid
            )

        for i in range(1, entry_count):
            add_and_check(True)

        add_and_check(False)

    def test_not_being_able_to_fetch_incomplete_list_entry(self):
        """
        Makes sure that one can't fetch an incomplete media list entry
        :return: None
        """
        anime_data = TestMediaData.generate_sample_anime_data()
        manga_user_data = TestMediaUserData.generate_sample_manga_user_data()
        site = IdType.MYANIMELIST

        self.cache.add(IdType.MYANIMELIST, anime_data)
        self.cache.add(site, manga_user_data)

        for media_type in MediaType:
            self.assertIsNone(self.cache.get_media_list_entry(
                site, media_type, anime_data.id, manga_user_data.username
            ))

    def test_caching_entry(self):
        """
        Tests caching and retrieving a Media List Entry
        :return: None
        """
        entry = TestMediaListEntry.generate_sample_anime_entry()
        self.cache.add(IdType.MYANIMELIST, entry)
        self.assertEqual(
            entry,
            self.cache.get_media_list_entry(
                IdType.MYANIMELIST,
                entry.get_media_type(),
                entry.get_id(),
                entry.get_username()
            )
        )
