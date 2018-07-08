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
from typing import Dict, Tuple, Set, List, Optional
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus
from anime_list_apis.models.MediaUserData import MediaUserData, AnimeUserData,\
    MangaUserData


class TestMediaUserData(TestCase):
    """
    Tests the MediaUserData Model class
    """

    @staticmethod
    def generate_sample_anime_user_data() -> AnimeUserData:
        """
        Generates a sample AnimeUserData object
        :return: The generated AnimeUserData object
        """
        return AnimeUserData(
            "namboy94",
            Score(55, ScoreType.PERCENTAGE),
            ConsumingStatus.COMPLETED,
            Date(2018, 1, 1),
            Date(2018, 4, 4),
            12
        )

    @staticmethod
    def generate_sample_manga_user_data() -> MangaUserData:
        """
        Generates a sample MangaUserData object
        :return: The generated MangaUserData object
        """
        return MangaUserData(
            "namboy94",
            Score(55, ScoreType.PERCENTAGE),
            ConsumingStatus.COMPLETED,
            Date(2018, 1, 1),
            Date(2018, 4, 4),
            100,
            10
        )

    @staticmethod
    def generate_sample_serialized_anime_user_data() \
            -> Dict[str, Optional[str or int or float or bool
                    or Dict or List or Tuple or Set]]:
        """
        Generates a sample serialized AnimeUserData object
        :return: The serialized data
        """
        return {
            "media_type": "ANIME",
            "username": "namboy94",
            "score": Score(55, ScoreType.PERCENTAGE).serialize(),
            "consuming_status": "COMPLETED",
            "episode_progress": 12,
            "consuming_start": Date(2018, 1, 1).serialize(),
            "consuming_end": Date(2018, 4, 4).serialize()
        }

    @staticmethod
    def generate_sample_serialized_manga_user_data() \
            -> Dict[str, Optional[str or int or float or bool
                                  or Dict or List or Tuple or Set]]:
        """
        Generates a sample serialized MangaUserData object
        :return: The serialized data
        """
        return {
            "media_type": "MANGA",
            "username": "namboy94",
            "score": Score(55, ScoreType.PERCENTAGE).serialize(),
            "consuming_status": "COMPLETED",
            "chapter_progress": 100,
            "volume_progress": 10,
            "consuming_start": Date(2018, 1, 1).serialize(),
            "consuming_end": Date(2018, 4, 4).serialize()
        }

    def test_generating_anime_user_entry_data(self):
        """
        Tests generating an anime user entry data object
        :return: None
        """
        data = self.generate_sample_anime_user_data()
        self.assertEqual(data.username, "namboy94")
        self.assertEqual(data.score, Score(55, ScoreType.PERCENTAGE))
        self.assertEqual(data.consuming_status, ConsumingStatus.COMPLETED)
        self.assertEqual(data.episode_progress, 12)
        self.assertEqual(data.consuming_start, Date(2018, 1, 1))
        self.assertEqual(data.consuming_end, Date(2018, 4, 4))
        self.assertEqual(data.media_type, MediaType.ANIME)

    def test_generating_manga_user_entry_data(self):
        """
        Tests generating an manga user entry data object
        :return: None
        """
        data = self.generate_sample_manga_user_data()
        self.assertEqual(data.username, "namboy94")
        self.assertEqual(data.score, Score(55, ScoreType.PERCENTAGE))
        self.assertEqual(data.consuming_status, ConsumingStatus.COMPLETED)
        self.assertEqual(data.chapter_progress, 100)
        self.assertEqual(data.volume_progress, 10)
        self.assertEqual(data.consuming_start, Date(2018, 1, 1))
        self.assertEqual(data.consuming_end, Date(2018, 4, 4))
        self.assertEqual(data.media_type, MediaType.MANGA)

    def test_valid(self):
        """
        Makes sure that it's possible to check if an entry is valid
        :return: None
        """
        entry = self.generate_sample_anime_user_data()
        self.assertTrue(entry.is_valid_entry())

        entry.consuming_end = None
        self.assertFalse(entry.is_valid_entry())

        entry.consuming_status = ConsumingStatus.CURRENT
        self.assertTrue(entry.is_valid_entry())

        entry.consuming_start = None
        self.assertFalse(entry.is_valid_entry())

        entry.consuming_status = ConsumingStatus.PLANNING
        self.assertFalse(entry.is_valid_entry())

        entry.score = Score(0, ScoreType.PERCENTAGE)
        self.assertTrue(entry.is_valid_entry())

        entry = self.generate_sample_anime_user_data()
        entry.score = Score(0, ScoreType.PERCENTAGE)
        self.assertFalse(entry.is_valid_entry())

        entry.consuming_status = ConsumingStatus.CURRENT
        self.assertFalse(entry.is_valid_entry())

        entry.consuming_end = None
        self.assertTrue(entry.is_valid_entry())

    def test_none_parameters(self):
        """
        Tests using None as parameters
        :return: None
        """

        for media_cls, data in [
            (AnimeUserData, self.generate_sample_serialized_anime_user_data()),
            (MangaUserData, self.generate_sample_serialized_manga_user_data())
        ]:
            allowed = ["consuming_start", "consuming_end"]

            for parameter in allowed:
                copy = deepcopy(data)
                copy[parameter] = None
                entry = media_cls.deserialize(copy)
                self.assertEqual(entry.serialize()[parameter], None)

            for parameter in list(filter(
                    lambda x: x not in allowed, data.keys()
            )):
                copy = deepcopy(data)
                copy[parameter] = None
                try:
                    media_cls.deserialize(copy)
                    self.fail()
                except (ValueError, TypeError):
                    pass

    def test_serialization(self):
        """
        Tests serializing a MediaUserData object
        :return: None
        """
        self.assertEqual(
            self.generate_sample_anime_user_data().serialize(),
            self.generate_sample_serialized_anime_user_data()
        )
        self.assertEqual(
            self.generate_sample_manga_user_data().serialize(),
            self.generate_sample_serialized_manga_user_data()
        )

    def test_deserialization(self):
        """
        Tests deserializing a MediaUserData object
        :return: None
        """
        serialized = self.generate_sample_serialized_anime_user_data()
        self.assertEqual(
            AnimeUserData.deserialize(serialized),
            self.generate_sample_anime_user_data()
        )
        self.assertEqual(
            serialized,
            self.generate_sample_serialized_anime_user_data()
        )

        serialized = self.generate_sample_serialized_manga_user_data()
        self.assertEqual(
            MangaUserData.deserialize(serialized),
            self.generate_sample_manga_user_data()
        )
        self.assertEqual(
            serialized,
            self.generate_sample_serialized_manga_user_data()
        )

    def test_generic_deserialization(self):
        """
        Tests using the MediaUserData class to deserialize
        :return: None
        """
        anime_obj = self.generate_sample_anime_user_data()
        anime = MediaUserData.deserialize(anime_obj.serialize())
        self.assertEqual(anime_obj, anime)
        self.assertEqual(anime.media_type, MediaType.ANIME)
        self.assertTrue(isinstance(anime, AnimeUserData))

        manga_obj = self.generate_sample_manga_user_data()
        manga = MediaUserData.deserialize(manga_obj.serialize())
        self.assertEqual(manga_obj, manga)
        self.assertEqual(manga.media_type, MediaType.MANGA)
        self.assertTrue(isinstance(manga, MangaUserData))

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        def attempt_deserialize(media_cls: type(MediaUserData), data: dict):
            try:
                media_cls.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

        for media_class, sample in [
            (AnimeUserData, self.generate_sample_serialized_anime_user_data()),
            (MangaUserData, self.generate_sample_serialized_manga_user_data())
        ]:
            for key, value in sample.items():

                for faux_value in [2000, "Hello"]:
                    if type(faux_value) != type(value):
                        copy = deepcopy(sample)
                        copy[key] = faux_value
                        attempt_deserialize(media_class, copy)

                copy = deepcopy(sample)
                copy.pop(key)
                attempt_deserialize(media_class, copy)

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = self.generate_sample_anime_user_data()
        two = self.generate_sample_anime_user_data()

        self.assertEqual(one, two)

        two.username = "hermann"
        self.assertNotEqual(one, two)
        two = self.generate_sample_anime_user_data()

        two.consuming_start = None
        self.assertNotEqual(one, two)

        self.assertNotEqual(one, self.generate_sample_manga_user_data())

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        data = self.generate_sample_anime_user_data()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, AnimeUserData.deserialize(serialised))

        data = self.generate_sample_manga_user_data()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, MangaUserData.deserialize(serialised))
