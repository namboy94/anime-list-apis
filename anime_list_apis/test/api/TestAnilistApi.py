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
from anime_list_apis.cache.Cache import Cache
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Title import TitleType


class TestAnilistApi(TestCase):
    """
    Tests the Anilist Api.
    May be subclassed to test other APIs as well
    """

    api_class = AnilistApi
    """
    The API class to test
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
        self.cache = Cache("testdir/.cache", expiration=0)  # Discard cached
        self.api = self.api_class(cache=self.cache, rate_limit_pause=0.0)
        self.username = "namboy94"

    def tearDown(self):
        """
        Removes all generated files and directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_retrieving_data(self):
        """
        Tests retrieving a single data entry using different methods for
        both anime and manga.
        :return: None
        """
        for media_type, english, _id, get_func in [
            (MediaType.ANIME, "Cowboy Bebop",
             Id({
                 IdType.MYANIMELIST: 1,
                 IdType.KITSU: 1,
                 IdType.ANILIST: 1
             }),
             lambda x: self.api.get_anime_data(x)),
            (MediaType.MANGA, "Monster",
             Id({
                 IdType.MYANIMELIST: 1,
                 IdType.KITSU: 4,
                 IdType.ANILIST: 30001
             }),
             lambda x: self.api.get_manga_data(x))
        ]:

            entries = []
            counter = 0

            for inner_id in [_id, _id.get(self.api.id_type)]:
                entries.append(self.api.get_data(media_type, inner_id))
                entries.append(get_func(inner_id))
                counter += 2

            for id_type in self.valid_id_types:
                inner_id = Id({id_type: _id.get(id_type)})

                entries.append(self.api.get_data(media_type, inner_id))
                entries.append(get_func(inner_id))
                counter += 2

            self.assertEqual(len(entries), counter)
            for entry in entries:
                self.assertIsNotNone(entry)
                self.assertEqual(
                    entry.id.get(self.api.id_type),
                    _id.get(self.api.id_type)
                )
                self.assertEqual(
                    entry.title.get(TitleType.ENGLISH),
                    english
                )
                for compared in entries:
                    self.assertEqual(entry, compared)

    def test_retrieving_invalid_entry(self):
        """
        Tests retrieving invalid entries
        Assumptions: No ids < 0 or > 1000000000
        :return: None
        """
        for _id in [-1, 1000000000]:
            self.assertIsNone(self.api.get_anime_data(_id))
            self.assertIsNone(self.api.get_manga_data(_id))

    def test_retrieving_single_list_entry(self):
        """
        Tests retrieving a single list entry
        :return: None
        """
        for media_type, english, _id, get_func in [
            (MediaType.ANIME, "Steins;Gate",
             Id({
                IdType.KITSU: 5646,
                IdType.MYANIMELIST: 9253,
                IdType.ANILIST: 9253
             }),
             lambda x: self.api.get_anime_list_entry(x, self.username)),
            (MediaType.MANGA, "Spice & Wolf",
             Id({
                 IdType.MYANIMELIST: 9115,
                 IdType.KITSU: 18471,
                 IdType.ANILIST: 39115
             }),
             lambda x: self.api.get_manga_list_entry(x, self.username))
        ]:

            entries = []
            counter = 0

            for inner_id in [_id, _id.get(self.api.id_type)]:
                entries.append(self.api.get_list_entry(
                    media_type, inner_id, self.username
                ))
                entries.append(get_func(inner_id))
                counter += 2

            for id_type in self.valid_id_types:
                inner_id = Id({id_type: _id.get(id_type)})

                entries.append(self.api.get_list_entry(
                    media_type, inner_id, self.username
                ))
                entries.append(get_func(inner_id))
                counter += 2

            self.assertEqual(len(entries), counter)
            for entry in entries:
                self.assertIsNotNone(entry)
                self.assertEqual(self.username, entry.username)
                self.assertEqual(
                    entry.id.get(self.api.id_type),
                    _id.get(self.api.id_type)
                )
                self.assertEqual(
                    entry.title.get(TitleType.ENGLISH),
                    english
                )
                for compared in entries:
                    self.assertEqual(entry, compared)

    def test_retrieving_non_existant_list_entry(self):
        """
        Tests retrieving entries that are not in a user's list
        Uses very badly rated entries to make sure that they never get added
        to the list, breaking the test
        :return: None
        """
        for media_type, _id in {
            MediaType.ANIME: Id({
                IdType.KITSU: 378,  # Mars of Destruction
                IdType.MYANIMELIST: 413,
                IdType.ANILIST: 413
            }),
            MediaType.MANGA: Id({
                IdType.KITSU: 45257,  # Treasure Hunter Kukai
                IdType.MYANIMELIST: 539,
                IdType.ANILIST: 75257
            }),
        }.items():
            self.assertIsNone(self.api.get_list_entry(
                media_type, _id, self.username
            ))

    def test_retrieving_entry_for_non_existant_user(self):
        """
        Tests retrieving an entry for a non-existant user
        :return: None
        """
        self.assertIsNone(self.api.get_anime_list_entry(1, ""))
        self.assertIsNone(self.api.get_manga_list_entry(1, ""))

    def test_retrieving_lists(self):
        """
        Tests retrieving a user's lists using various methods
        :return: None
        """
        for media_type, get_func in {
            MediaType.ANIME: lambda: self.api.get_anime_list(self.username),
            MediaType.MANGA: lambda: self.api.get_manga_list(self.username)
        }.items():
            normal = self.api.get_list(media_type, self.username)
            short = get_func()
            self.assertEqual(normal, short)
            self.assertLess(1, len(normal))  # At least 2 entries

            for entry in normal + short:
                self.assertEqual(entry.media_type, media_type)
                self.assertEqual(entry.username, self.username)

    def test_retrieving_list_for_nonexistant_user(self):
        """
        Tests retrieving an anime list for an invalid user
        :return: None
        """
        self.assertEqual([], self.api.get_anime_list(""))
        self.assertEqual([], self.api.get_manga_list(""))

    def test_fetching_with_invalid_id_type(self):
        """
        Makes sure that trying to use an unsupported ID type results in
        a None object
        :return: None
        """
        for media_type in MediaType:
            for id_type in IdType:
                if id_type in self.valid_id_types:
                    continue
                else:
                    _id = Id({id_type: 1})
                    self.assertIsNone(
                        self.api.get_list_entry(media_type, _id, self.username)
                    )
                    self.assertIsNone(
                        self.api.get_data(media_type, _id)
                    )

    def test_caching_anime(self):
        """
        Tests that the caching works correctly for media data
        :return: None
        """
        self.api.cache = Cache(self.cache.cache_location)
        for media_type, english, _id in [
            (MediaType.ANIME, "Steins;Gate",
             Id({
                 IdType.KITSU: 5646,
                 IdType.MYANIMELIST: 9253,
                 IdType.ANILIST: 9253
             })),
            (MediaType.MANGA, "Spice & Wolf",
             Id({
                 IdType.MYANIMELIST: 9115,
                 IdType.KITSU: 18471,
                 IdType.ANILIST: 39115
             }))
        ]:
            fetched_entry = self.api.get_list_entry(
                media_type, _id, self.username
            )
            fetched_data = self.api.get_data(media_type, _id)
            cached_entry = self.api.cache.get_media_list_entry(
                self.api.id_type, media_type, _id, self.username
            )
            cached_data = self.api.cache.get_media_data(
                self.api.id_type, media_type, _id
            )
            self.assertEqual(
                fetched_data.title.get(TitleType.ENGLISH), english
            )
            self.assertEqual(
                fetched_entry.title.get(TitleType.ENGLISH), english
            )
            self.assertEqual(fetched_data, cached_data)
            self.assertEqual(fetched_entry, cached_entry)

            def raise_value_error():
                raise ValueError()

            # Makes sure that cached value is used from now on
            with mock.patch("requests.post", new=raise_value_error):
                with mock.patch("requests.get", new=raise_value_error):
                    new_fetched_data = self.api.get_data(media_type, _id)
                    new_fetched_entry = self.api.get_list_entry(
                        media_type, _id, self.username
                    )
                    self.assertEqual(new_fetched_data, cached_data)
                    self.assertEqual(new_fetched_entry, cached_entry)


class TestAnilistApiSpecific(TestCase):
    """
    Tests specifically for the Anilist API
    """

    def setUp(self):
        """
        Creates a cache
        :return: None
        """
        self.tearDown()
        os.makedirs("testdir")
        self.cache = Cache("testdir/.cache")
        self.api = AnilistApi(cache=self.cache, rate_limit_pause=0.0)
        self.username = "namboy94"

    def tearDown(self):
        """
        Removes all generated files and directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_filling_in_english_title_with_romaji(self):
        """
        Some titles don't have an english title entry on anilist.
        In such cases, the romaji will automatically be filled in into the
        english title.
        :return: None
        """
        steins_gate = self.api.get_anime_data(9253)
        self.assertEqual(
            steins_gate.title.get(TitleType.ROMAJI),
            steins_gate.title.get(TitleType.ENGLISH),
        )
        self.assertEqual(
            steins_gate.title.get(TitleType.ROMAJI),
            "Steins;Gate",
        )

    def test_getting_anilist_id_from_mal_id(self):
        """
        Tests retrieving an anilist ID for a myanimelist ID
        :return: None
        """
        mal = 30484
        anilist = 21127
        self.assertEqual(
            self.api.get_anilist_id_from_mal_id(MediaType.ANIME, mal),
            anilist
        )

    def test_getting_anilist_info_with_invalid_mal_id(self):
        """
        Tests retrieving anilist data with an invalid myanimelist ID
        :return: None
        """
        for _id in [-1, 2, 1000000000]:
            self.assertIsNone(
                self.api.get_anilist_id_from_mal_id(MediaType.ANIME, _id)
            )
            self.assertIsNone(
                self.api.get_anime_list_entry(_id, self.username)
            )
            self.assertIsNone(
                self.api.get_anime_data(_id)
            )
        # noinspection PyTypeChecker
        self.assertIsNone(
            self.api.get_anilist_id_from_mal_id(MediaType.ANIME, None)
        )
