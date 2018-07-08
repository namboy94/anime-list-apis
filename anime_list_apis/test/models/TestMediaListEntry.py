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
from copy import deepcopy
from unittest import TestCase
from typing import Dict, List, Set, Tuple, Optional
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Title import Title, TitleType
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus
from anime_list_apis.test.models.TestMediaData import TestMediaData
from anime_list_apis.test.models.TestMediaUserData import TestMediaUserData
from anime_list_apis.models.MediaListEntry import MediaListEntry, \
    AnimeListEntry, MangaListEntry


class TestMediaListEntry(TestCase):
    """
    Tests the MediaListEntry Model class
    """

    @staticmethod
    def generate_sample_anime_entry() -> AnimeListEntry:
        """
        Generates a sample AnimeListEntry object
        :return: The generated AnimeListEntry object
        """
        return AnimeListEntry(
            TestMediaData.generate_sample_anime_data(),
            TestMediaUserData.generate_sample_anime_user_data()
        )

    @staticmethod
    def generate_sample_manga_entry() -> MangaListEntry:
        """
        Generates a sample MangaListEntry object
        :return: The generated MangaListEntry object
        """
        return MangaListEntry(
            TestMediaData.generate_sample_manga_data(),
            TestMediaUserData.generate_sample_manga_user_data()
        )

    @staticmethod
    def generate_sample_serialized_anime_entry() \
            -> Dict[str, Optional[str or int or float or bool
                    or Dict or List or Tuple or Set]]:
        """
        Generates a sample deserialized version of the sample anime entry
        :return: The deserialized sample entry
        """
        return {
            "media_type": "ANIME",
            "media_data":
                TestMediaData.generate_sample_serialized_anime_data(),
            "user_data":
                TestMediaUserData.generate_sample_serialized_anime_user_data()
        }

    @staticmethod
    def generate_sample_serialized_manga_entry() \
            -> Dict[str, Optional[str or int or float or bool
                                  or Dict or List or Tuple or Set]]:
        """
        Generates a sample deserialized version of the sample manga entry
        :return: The deserialized sample entry
        """
        return {
            "media_type": "MANGA",
            "media_data":
                TestMediaData.generate_sample_serialized_manga_data(),
            "user_data":
                TestMediaUserData.generate_sample_serialized_manga_user_data()
        }

    def test_generating_anime_media_list_entry(self):
        """
        Tests generating an anime media list entry object
        :return: None
        """
        data = self.generate_sample_anime_entry()
        self.assertEqual(data.id, Id({IdType.MYANIMELIST: 1}))
        self.assertEqual(data.title, Title({TitleType.ROMAJI: "Test"}))
        self.assertEqual(
            data.relations,
            [Relation(
                Id({IdType.MYANIMELIST: 1}),
                MediaType.ANIME,
                Id({IdType.MYANIMELIST: 2}),
                MediaType.MANGA,
                RelationType.SEQUEL
            )]
        )
        self.assertEqual(data.releasing_status, ReleasingStatus.FINISHED)
        self.assertEqual(data.releasing_start, Date(2018, 1, 1))
        self.assertEqual(data.releasing_end, Date(2018, 4, 4))
        self.assertEqual(data.episode_count, 12)
        self.assertEqual(data.episode_duration, 25)
        self.assertEqual(data.cover_url, "https://example.com/image.png")
        self.assertEqual(data.username, "namboy94")
        self.assertEqual(data.score, Score(55, ScoreType.PERCENTAGE))
        self.assertEqual(data.consuming_status, ConsumingStatus.COMPLETED)
        self.assertEqual(data.episode_progress, 12)
        self.assertEqual(data.consuming_start, Date(2018, 1, 1))
        self.assertEqual(data.consuming_end, Date(2018, 4, 4))
        self.assertEqual(data.media_type, MediaType.ANIME)

    def test_generating_manga_media_list_entry(self):
        """
        Tests generating a manga media list entry object
        :return: None
        """
        data = self.generate_sample_manga_entry()
        self.assertEqual(data.id, Id({IdType.MYANIMELIST: 1}))
        self.assertEqual(data.title, Title({TitleType.ROMAJI: "Test"}))
        self.assertEqual(
            data.relations,
            [Relation(
                Id({IdType.MYANIMELIST: 1}),
                MediaType.MANGA,
                Id({IdType.MYANIMELIST: 2}),
                MediaType.MANGA,
                RelationType.SEQUEL
            )]
        )
        self.assertEqual(data.releasing_status, ReleasingStatus.FINISHED)
        self.assertEqual(data.releasing_start, Date(2018, 1, 1))
        self.assertEqual(data.releasing_end, Date(2018, 4, 4))
        self.assertEqual(data.chapter_count, 100)
        self.assertEqual(data.volume_count, 10)
        self.assertEqual(data.cover_url, "https://example.com/image.png")
        self.assertEqual(data.username, "namboy94")
        self.assertEqual(data.score, Score(55, ScoreType.PERCENTAGE))
        self.assertEqual(data.consuming_status, ConsumingStatus.COMPLETED)
        self.assertEqual(data.chapter_progress, 100)
        self.assertEqual(data.volume_progress, 10)
        self.assertEqual(data.consuming_start, Date(2018, 1, 1))
        self.assertEqual(data.consuming_end, Date(2018, 4, 4))
        self.assertEqual(data.media_type, MediaType.MANGA)

    def test_internal_getters(self):
        """
        Tests the generating getter methods that generate
        MediaData and MediaUserData objects
        :return: None
        """
        entry = self.generate_sample_anime_entry()
        self.assertEqual(
            entry.get_media_data(),
            TestMediaData.generate_sample_anime_data()
        )
        self.assertEqual(
            entry.get_user_data(),
            TestMediaUserData.generate_sample_anime_user_data()
        )

        entry = self.generate_sample_manga_entry()
        self.assertEqual(
            entry.get_media_data(),
            TestMediaData.generate_sample_manga_data()
        )
        self.assertEqual(
            entry.get_user_data(),
            TestMediaUserData.generate_sample_manga_user_data()
        )

    def test_if_valid(self):
        """
        Tests the functionality of the is_valid_entry method
        :return: None
        """

        for cls, entry, serialized in [
            (AnimeListEntry,
             self.generate_sample_anime_entry(),
             self.generate_sample_serialized_anime_entry()),
            (MangaListEntry,
             self.generate_sample_manga_entry(),
             self.generate_sample_serialized_manga_entry())
        ]:
            self.assertTrue(entry.is_valid_entry())

            zero = Score(0, ScoreType.PERCENTAGE).serialize()
            non_zero = Score(70, ScoreType.PERCENTAGE).serialize()
            for config in [
                [
                    ("media", "releasing_status", "RELEASING"),
                    ("user", "consuming_status", "CURRENT"),
                    ("user", "score", zero),
                    ("user", "consuming_end", None)
                ],
                [
                    ("user", "consuming_status", "PLANNING"),
                    ("user", "score", zero),
                    ("user", "consuming_start", None),
                    ("user", "consuming_end", None)
                ],
                [
                    ("user", "score", zero),
                    ("user", "score", non_zero),
                ],
                [
                    ("media", "releasing_status", "NOT_RELEASED"),
                    ("user", "score", zero),
                    ("user", "consuming_start", None),
                    ("user", "consuming_end", None),
                    ("user", "consuming_status", "CURRENT"),
                    ("user", "consuming_status", "PAUSED"),
                    ("user", "consuming_status", "DROPPED"),
                    ("user", "consuming_status", "PLANNING")
                ]
            ]:
                data = deepcopy(serialized)

                for i, conf in enumerate(config):

                    master, key, value = conf

                    data[master + "_data"][key] = value
                    entry = MediaListEntry.deserialize(data)

                    if i == len(config) - 1:
                        self.assertTrue(entry.is_valid_entry())
                    else:
                        self.assertFalse(entry.is_valid_entry())

    def test_mixing_anime_and_manga(self):
        """
        Tests that it's impossible to mix anime and manga data
        :return:
        """

        try:
            # noinspection PyTypeChecker
            AnimeListEntry(
                TestMediaData.generate_sample_manga_data(),
                TestMediaUserData.generate_sample_manga_user_data()
            )
            self.fail()
        except (TypeError, ValueError):
            pass

    def test_serialization(self):
        """
        Tests serializing a MediaUserData object
        :return: None
        """
        self.assertEqual(
            self.generate_sample_anime_entry().serialize(),
            self.generate_sample_serialized_anime_entry()
        )
        self.assertEqual(
            self.generate_sample_manga_entry().serialize(),
            self.generate_sample_serialized_manga_entry()
        )

    def test_deserialization(self):
        """
        Tests deserializing a MediaUserData object
        :return: None
        """
        self.assertEqual(
            AnimeListEntry.deserialize(
                self.generate_sample_serialized_anime_entry()
            ),
            self.generate_sample_anime_entry()
        )
        self.assertEqual(
            MangaListEntry.deserialize(
                self.generate_sample_serialized_manga_entry()
            ),
            self.generate_sample_manga_entry()
        )

    def test_generic_deserialization(self):
        """
        Tests using the MediaListEntry class to deserialize
        :return: None
        """
        anime_obj = self.generate_sample_anime_entry()
        anime = MediaListEntry.deserialize(anime_obj.serialize())
        self.assertEqual(anime_obj, anime)
        self.assertEqual(anime.media_type, MediaType.ANIME)
        self.assertTrue(isinstance(anime, AnimeListEntry))

        manga_obj = self.generate_sample_manga_entry()
        manga = MediaListEntry.deserialize(manga_obj.serialize())
        self.assertEqual(manga_obj, manga)
        self.assertEqual(manga.media_type, MediaType.MANGA)
        self.assertTrue(isinstance(manga, MangaListEntry))

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        def attempt_deserialize(media_cls: type(MediaListEntry), data: dict):
            try:
                media_cls.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

        for media_class, serialized in [
            (AnimeListEntry, self.generate_sample_serialized_anime_entry()),
            (MangaListEntry, self.generate_sample_serialized_manga_entry())
        ]:

            for key in ["media_data", "user_data"]:

                backup = serialized[key]
                serialized[key] = None
                attempt_deserialize(media_class, serialized)

                serialized.pop(key)
                attempt_deserialize(media_class, serialized)
                serialized[key] = backup

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = self.generate_sample_anime_entry()
        two = self.generate_sample_anime_entry()

        self.assertEqual(one, two)

        two.id = Id({IdType.KITSU: 1})
        self.assertNotEqual(one, two)
        two = self.generate_sample_anime_entry()

        two.releasing_start = None
        self.assertNotEqual(one, two)
        two = self.generate_sample_anime_entry()

        two.username = "hermann"
        self.assertNotEqual(one, two)
        two = self.generate_sample_anime_entry()

        two.consuming_end = None
        self.assertNotEqual(one, two)

        self.assertNotEqual(one, self.generate_sample_manga_entry())

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        data = self.generate_sample_anime_entry()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, AnimeListEntry.deserialize(serialised))

        data = self.generate_sample_manga_entry()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, MangaListEntry.deserialize(serialised))
