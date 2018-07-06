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
from typing import Dict, List, Set, Tuple, Optional
from anime_list_apis.models.AnimeListEntry import AnimeListEntry
from anime_list_apis.models.attributes.AiringStatus import AiringStatus
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Title import Title, TitleType
from anime_list_apis.models.attributes.WatchingStatus import WatchingStatus
from anime_list_apis.test.models.TestAnimeData import TestAnimeData
from anime_list_apis.test.models.TestAnimeUserData import TestAnimeUserData


class TestAnimeListEntry(TestCase):
    """
    Tests the AnimeListEntry Model class
    """

    @staticmethod
    def generate_sample_entry() -> AnimeListEntry:
        """
        Generates a sample AnimeListEntry object
        :return: The generated AnimeListEntry object
        """
        return AnimeListEntry(
            TestAnimeData.generate_sample_anime_data(),
            TestAnimeUserData.generate_sample_user_data()
        )

    @staticmethod
    def generate_sample_serialized_entry() \
            -> Dict[str, Optional[str or int or float or bool
                    or Dict or List or Tuple or Set]]:
        """
        Generates a sample deserialized version of the sample entry
        :return: The deserialized sample entry
        """
        return {
            "anime_data":
                TestAnimeData.generate_sample_serialized_anime_data(),
            "user_data":
                TestAnimeUserData.generate_sample_serialized_user_data()
        }

    def test_generating_anime_list_entry(self):
        """
        Tests generating an anime list entry object
        :return: None
        """
        data = self.generate_sample_entry()
        self.assertEqual(data.id, Id({IdType.MYANIMELIST: 1}))
        self.assertEqual(data.title, Title({TitleType.ROMAJI: "Test"}))
        self.assertEqual(
            data.relations,
            [Relation(
                Id({IdType.MYANIMELIST: 1}),
                Id({IdType.MYANIMELIST: 2}),
                RelationType.SEQUEL
            )]
        )
        self.assertEqual(data.airing_status, AiringStatus.FINISHED)
        self.assertEqual(data.airing_start, Date(2018, 1, 1))
        self.assertEqual(data.airing_end, Date(2018, 4, 4))
        self.assertEqual(data.episode_count, 12)
        self.assertEqual(data.episode_duration, 25)
        self.assertEqual(data.cover_url, "https://example.com/image.png")
        self.assertEqual(data.username, "namboy94")
        self.assertEqual(data.score, Score(55, ScoreType.PERCENTAGE))
        self.assertEqual(data.watching_status, WatchingStatus.COMPLETED)
        self.assertEqual(data.episode_progress, 12)
        self.assertEqual(data.watching_start, Date(2018, 1, 1))
        self.assertEqual(data.watching_end, Date(2018, 4, 4))
        self.assertEqual(data.media_type, MediaType.ANIME)

    def test_internal_getters(self):
        """
        Tests the two generating getter methods that generate
        AnimeData and AnimeUserData objects
        :return: None
        """
        entry = self.generate_sample_entry()
        self.assertEqual(
            entry.get_anime_data(),
            TestAnimeData.generate_sample_anime_data()
        )
        self.assertEqual(
            entry.get_user_data(),
            TestAnimeUserData.generate_sample_user_data()
        )

    def test_if_valid(self):
        """
        Tests the functionality of the is_valid_entry method
        :return: None
        """
        entry = self.generate_sample_entry()
        self.assertTrue(entry.is_valid_entry())

        for config in [
            [
                ("anime", "airing_status", AiringStatus.RELEASING.name),
                ("user", "watching_status", WatchingStatus.WATCHING.name),
                ("user", "score", Score(0, ScoreType.PERCENTAGE).serialize()),
                ("user", "watching_end", None)
            ],
            [
                ("user", "watching_status", WatchingStatus.PLANNING.name),
                ("user", "score", Score(0, ScoreType.PERCENTAGE).serialize()),
                ("user", "watching_start", None),
                ("user", "watching_end", None)
            ],
            [
                ("user", "score", Score(0, ScoreType.PERCENTAGE).serialize()),
                ("user", "score", Score(70, ScoreType.PERCENTAGE).serialize()),
            ],
            [
                ("anime", "airing_status", AiringStatus.NOT_RELEASED.name),
                ("user", "score", Score(0, ScoreType.PERCENTAGE).serialize()),
                ("user", "watching_start", None),
                ("user", "watching_end", None),
                ("user", "watching_status", WatchingStatus.WATCHING.name),
                ("user", "watching_status", WatchingStatus.PAUSED.name),
                ("user", "watching_status", WatchingStatus.DROPPED.name),
                ("user", "watching_status", WatchingStatus.PLANNING.name)
            ]
        ]:
            serialized = self.generate_sample_serialized_entry()
            for i, conf in enumerate(config):
                master, key, value = conf

                serialized[master + "_data"][key] = value
                entry = AnimeListEntry.deserialize(serialized)

                if i == len(config) - 1:
                    self.assertTrue(entry.is_valid_entry())
                else:
                    self.assertFalse(entry.is_valid_entry())

    def test_serialization(self):
        """
        Tests serializing a AnimeUserData object
        :return: None
        """
        self.assertEqual(
            self.generate_sample_entry().serialize(),
            self.generate_sample_serialized_entry()
        )

    def test_deserialization(self):
        """
        Tests deserializing a AnimeUserData object
        :return: None
        """
        self.assertEqual(
            AnimeListEntry.deserialize(
                self.generate_sample_serialized_entry()
            ),
            self.generate_sample_entry()
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        def attempt_deserialize(data: dict):
            try:
                AnimeListEntry.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

        for key in ["anime_data", "user_data"]:
            serialized = self.generate_sample_serialized_entry()

            serialized[key] = None
            attempt_deserialize(serialized)

            serialized.pop(key)
            attempt_deserialize(serialized)

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = self.generate_sample_entry()
        two = self.generate_sample_entry()

        self.assertEqual(one, two)

        two.id = Id({IdType.KITSU: 1})
        self.assertNotEqual(one, two)
        two = self.generate_sample_entry()

        two.airing_start = None
        self.assertNotEqual(one, two)
        two = self.generate_sample_entry()

        two.username = "hermann"
        self.assertNotEqual(one, two)
        two = self.generate_sample_entry()

        two.watching_end = None
        self.assertNotEqual(one, two)

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        data = self.generate_sample_entry()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, AnimeListEntry.deserialize(serialised))
