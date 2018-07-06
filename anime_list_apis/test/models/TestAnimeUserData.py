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
from typing import Dict, Tuple, Set, List
from anime_list_apis.models.AnimeUserData import AnimeUserData
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.WatchingStatus import WatchingStatus


class TestAnimeUserData(TestCase):
    """
    Tests the AnimeUserData Model class
    """

    @staticmethod
    def generate_sample_user_data() -> AnimeUserData:
        """
        Generates a sample AnimeUserData object
        :return: The generated AnimeUserData object
        """
        return AnimeUserData(
            "namboy94",
            Score(55, ScoreType.PERCENTAGE),
            WatchingStatus.COMPLETED,
            12,
            Date(2018, 1, 1),
            Date(2018, 4, 4)
        )

    @staticmethod
    def generate_sample_serialized_user_data() \
            -> Dict[str, str or int or float or bool or None
                    or Dict or List or Tuple or Set]:
        """
        Generates a sample serialized AnimeUserData object
        :return: The serialized data
        """
        return {
            "username": "namboy94",
            "score": Score(55, ScoreType.PERCENTAGE).serialize(),
            "watching_status": "COMPLETED",
            "episode_progress": 12,
            "watching_start": Date(2018, 1, 1).serialize(),
            "watching_end": Date(2018, 4, 4).serialize()
        }

    def test_generating_user_entry_data(self):
        """
        Tests generating a user entry data object
        :return: None
        """
        data = self.generate_sample_user_data()
        self.assertEqual(data.username, "namboy94")
        self.assertEqual(data.score, Score(55, ScoreType.PERCENTAGE))
        self.assertEqual(data.watching_status, WatchingStatus.COMPLETED)
        self.assertEqual(data.episode_progress, 12)
        self.assertEqual(data.watching_start, Date(2018, 1, 1))
        self.assertEqual(data.watching_end, Date(2018, 4, 4))
        self.assertEqual(data.media_type, MediaType.ANIME)

    def test_valid(self):
        """
        Makes sure that it's possible to check if an entry is valid
        :return: None
        """
        entry = self.generate_sample_user_data()
        self.assertTrue(entry.is_valid_entry())

        entry.watching_end = None
        self.assertFalse(entry.is_valid_entry())

        entry.watching_status = WatchingStatus.WATCHING
        self.assertTrue(entry.is_valid_entry())

        entry.watching_start = None
        self.assertFalse(entry.is_valid_entry())

        entry.watching_status = WatchingStatus.PLANNING
        self.assertFalse(entry.is_valid_entry())

        entry.score = Score(0, ScoreType.PERCENTAGE)
        self.assertTrue(entry.is_valid_entry())

        entry = self.generate_sample_user_data()
        entry.score = Score(0, ScoreType.PERCENTAGE)
        self.assertFalse(entry.is_valid_entry())

        entry.watching_status = WatchingStatus.WATCHING
        self.assertFalse(entry.is_valid_entry())

        entry.watching_end = None
        self.assertTrue(entry.is_valid_entry())

    def test_none_parameters(self):
        """
        Tests using None as parameters
        :return: None
        """

        data = self.generate_sample_serialized_user_data()
        allowed = ["watching_start", "watching_end"]

        for parameter in allowed:
            copy = deepcopy(data)
            copy[parameter] = None
            entry = AnimeUserData.deserialize(copy)
            self.assertEqual(entry.serialize()[parameter], None)

        for parameter in list(filter(lambda x: x not in allowed, data.keys())):
            copy = deepcopy(data)
            copy[parameter] = None
            try:
                AnimeUserData.deserialize(copy)
                self.fail()
            except (ValueError, TypeError):
                pass

    def test_serialization(self):
        """
        Tests serializing a AnimeUserData object
        :return: None
        """
        self.assertEqual(
            self.generate_sample_user_data().serialize(),
            self.generate_sample_serialized_user_data()
        )

    def test_deserialization(self):
        """
        Tests deserializing a AnimeUserData object
        :return: None
        """
        serialized = self.generate_sample_serialized_user_data()
        self.assertEqual(
            AnimeUserData.deserialize(serialized),
            self.generate_sample_user_data()
        )
        self.assertEqual(
            serialized,
            self.generate_sample_serialized_user_data()
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        def attempt_deserialize(data: dict):
            try:
                AnimeUserData.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

        sample = self.generate_sample_serialized_user_data()
        for key, value in sample.items():

            for faux_value in [2000, "Hello"]:
                if type(faux_value) != type(value):
                    copy = deepcopy(sample)
                    copy[key] = faux_value
                    attempt_deserialize(copy)

            copy = deepcopy(sample)
            copy.pop(key)
            attempt_deserialize(copy)

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = self.generate_sample_user_data()
        two = self.generate_sample_user_data()

        self.assertEqual(one, two)

        two.username = "hermann"
        self.assertNotEqual(one, two)
        two = self.generate_sample_user_data()

        two.watching_start = None
        self.assertNotEqual(one, two)

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        data = self.generate_sample_user_data()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, AnimeUserData.deserialize(serialised))
