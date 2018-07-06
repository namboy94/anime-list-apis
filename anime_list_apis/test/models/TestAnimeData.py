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
from typing import Dict, List, Set, Tuple

from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.AiringStatus import AiringStatus
from anime_list_apis.models.AnimeData import AnimeData
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.Title import Title, TitleType
from anime_list_apis.models.attributes.Date import Date


class TestAnimeData(TestCase):
    """
    Tests the AnimeData Model class
    """

    @staticmethod
    def generate_sample_anime_data() -> AnimeData:
        """
        Generates a generic Anime Data object
        :return: The generated anime data object
        """
        return AnimeData(
            Id({IdType.MYANIMELIST: 1}),
            Title({TitleType.ROMAJI: "Test"}),
            [Relation(
                Id({IdType.MYANIMELIST: 1}),
                Id({IdType.MYANIMELIST: 2}),
                RelationType.SEQUEL
            )],
            AiringStatus.FINISHED,
            Date(2018, 1, 1),
            Date(2018, 4, 4),
            12,
            25,
            "https://example.com/image.png"
        )

    @staticmethod
    def generate_sample_serialized_anime_data() -> \
            Dict[str, str or int or float or bool or None
                 or Dict or List or Tuple or Set]:
        """
        Generates some sample serialized anime data
        :return: The serialized sample data
        """
        return {
            "id": Id({IdType.MYANIMELIST: 1}).serialize(),
            "title": Title({TitleType.ROMAJI: "Test"}).serialize(),
            "relations": [
                Relation(
                    Id({IdType.MYANIMELIST: 1}),
                    Id({IdType.MYANIMELIST: 2}),
                    RelationType.SEQUEL
                ).serialize()
            ],
            "airing_status": AiringStatus.FINISHED.name,
            "airing_start": Date(2018, 1, 1).serialize(),
            "airing_end": Date(2018, 4, 4).serialize(),
            "episode_count": 12,
            "episode_duration": 25,
            "cover_url": "https://example.com/image.png"
        }

    def test_generating_anime_data(self):
        """
        Tests generating an anime data object
        :return: None
        """
        data = self.generate_sample_anime_data()
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
        self.assertEqual(data.media_type, MediaType.ANIME)

    def test_generating_with_none_value(self):
        """
        Tests using a valid None value in the constructor
        :return: None
        """
        serialized = self.generate_sample_serialized_anime_data()
        serialized["airing_end"] = None
        data = AnimeData.deserialize(serialized)
        self.assertEqual(data.airing_end, None)

    def test_serialization(self):
        """
        Tests serializing an AnimeData object
        :return: None
        """
        self.assertEqual(
            self.generate_sample_anime_data().serialize(),
            self.generate_sample_serialized_anime_data()
        )

    def test_deserialization(self):
        """
        Tests deserializing an AnimeData object
        :return: None
        """
        serialized = self.generate_sample_serialized_anime_data()
        self.assertEqual(
            AnimeData.deserialize(serialized),
            self.generate_sample_anime_data()
        )
        self.assertEqual(
            serialized,
            self.generate_sample_serialized_anime_data()
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        def attempt_deserialize(data: dict):
            try:
                AnimeData.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

        sample = self.generate_sample_serialized_anime_data()
        for key, value in sample.items():

            for faux_value in [2000, "Hello", Id({IdType.KITSU: 1})]:
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
        one = self.generate_sample_anime_data()
        two = self.generate_sample_anime_data()

        self.assertEqual(one, two)

        two.id = Id({IdType.KITSU: 1})
        self.assertNotEqual(one, two)
        two = self.generate_sample_anime_data()

        two.airing_start = None
        self.assertNotEqual(one, two)

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        data = self.generate_sample_anime_data()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, AnimeData.deserialize(serialised))
