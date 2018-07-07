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

from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus
from anime_list_apis.models.MediaData import MediaData, AnimeData, MangaData
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.Title import Title, TitleType
from anime_list_apis.models.attributes.Date import Date


class TestMediaData(TestCase):
    """
    Tests the MediaData Model class
    """

    @staticmethod
    def generate_sample_anime_data() -> AnimeData:
        """
        Generates a generic AnimeData object
        :return: The generated anime data object
        """
        return AnimeData(
            Id({IdType.MYANIMELIST: 1}),
            Title({TitleType.ROMAJI: "Test"}),
            [Relation(
                Id({IdType.MYANIMELIST: 1}),
                MediaType.ANIME,
                Id({IdType.MYANIMELIST: 2}),
                MediaType.MANGA,
                RelationType.SEQUEL
            )],
            ReleasingStatus.FINISHED,
            Date(2018, 1, 1),
            Date(2018, 4, 4),
            "https://example.com/image.png",
            12,
            25,
        )

    @staticmethod
    def generate_sample_manga_data() -> MangaData:
        """
        Generates a generic MangaData object
        :return: The generated manga data object
        """
        return MangaData(
            Id({IdType.MYANIMELIST: 1}),
            Title({TitleType.ROMAJI: "Test"}),
            [Relation(
                Id({IdType.MYANIMELIST: 1}),
                MediaType.MANGA,
                Id({IdType.MYANIMELIST: 2}),
                MediaType.MANGA,
                RelationType.SEQUEL
            )],
            ReleasingStatus.FINISHED,
            Date(2018, 1, 1),
            Date(2018, 4, 4),
            "https://example.com/image.png",
            100,
            10
        )

    @staticmethod
    def generate_sample_serialized_anime_data() -> \
            Dict[str, Optional[str or int or float or bool
                 or Dict or List or Tuple or Set]]:
        """
        Generates some sample serialized anime data
        :return: The serialized sample data
        """
        return {
            "media_type": "ANIME",
            "id": Id({IdType.MYANIMELIST: 1}).serialize(),
            "title": Title({TitleType.ROMAJI: "Test"}).serialize(),
            "relations": [
                Relation(
                    Id({IdType.MYANIMELIST: 1}),
                    MediaType.ANIME,
                    Id({IdType.MYANIMELIST: 2}),
                    MediaType.MANGA,
                    RelationType.SEQUEL
                ).serialize()
            ],
            "releasing_status": ReleasingStatus.FINISHED.name,
            "releasing_start": Date(2018, 1, 1).serialize(),
            "releasing_end": Date(2018, 4, 4).serialize(),
            "episode_count": 12,
            "episode_duration": 25,
            "cover_url": "https://example.com/image.png"
        }

    @staticmethod
    def generate_sample_serialized_manga_data() -> \
            Dict[str, Optional[str or int or float or bool
                 or Dict or List or Tuple or Set]]:
        """
        Generates some sample serialized manga data
        :return: The serialized sample data
        """
        return {
            "media_type": "MANGA",
            "id": Id({IdType.MYANIMELIST: 1}).serialize(),
            "title": Title({TitleType.ROMAJI: "Test"}).serialize(),
            "relations": [
                Relation(
                    Id({IdType.MYANIMELIST: 1}),
                    MediaType.MANGA,
                    Id({IdType.MYANIMELIST: 2}),
                    MediaType.MANGA,
                    RelationType.SEQUEL
                ).serialize()
            ],
            "releasing_status": ReleasingStatus.FINISHED.name,
            "releasing_start": Date(2018, 1, 1).serialize(),
            "releasing_end": Date(2018, 4, 4).serialize(),
            "chapter_count": 100,
            "volume_count": 10,
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
        self.assertEqual(data.media_type, MediaType.ANIME)

    def test_generating_manga_data(self):
        """
        Tests generating a manga data object
        :return: None
        """
        data = self.generate_sample_manga_data()
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
        self.assertEqual(data.media_type, MediaType.MANGA)

    def test_generating_with_none_value(self):
        """
        Tests using a valid None value in the constructor
        :return: None
        """
        serialized = self.generate_sample_serialized_anime_data()
        serialized["releasing_end"] = None
        data = AnimeData.deserialize(serialized)
        self.assertEqual(data.releasing_end, None)

    def test_serialization(self):
        """
        Tests serializing an MediaData object
        :return: None
        """
        self.assertEqual(
            self.generate_sample_anime_data().serialize(),
            self.generate_sample_serialized_anime_data()
        )
        self.assertEqual(
            self.generate_sample_manga_data().serialize(),
            self.generate_sample_serialized_manga_data()
        )

    def test_deserialization(self):
        """
        Tests deserializing an MediaData object
        :return: None
        """
        anime_serialized = self.generate_sample_serialized_anime_data()
        self.assertEqual(
            AnimeData.deserialize(anime_serialized),
            self.generate_sample_anime_data()
        )
        self.assertEqual(
            anime_serialized,
            self.generate_sample_serialized_anime_data()
        )

        manga_serialized = self.generate_sample_serialized_manga_data()
        self.assertEqual(
            MangaData.deserialize(manga_serialized),
            self.generate_sample_manga_data()
        )
        self.assertEqual(
            manga_serialized,
            self.generate_sample_serialized_manga_data()
        )

    def test_generic_deserialization(self):
        """
        Tests using the MediaData class to deserialize
        :return: None
        """
        anime_obj = self.generate_sample_anime_data()
        anime = MediaData.deserialize(anime_obj.serialize())
        self.assertEqual(anime_obj, anime)
        self.assertEqual(anime.media_type, MediaType.ANIME)
        self.assertTrue(isinstance(anime, AnimeData))

        manga_obj = self.generate_sample_manga_data()
        manga = MediaData.deserialize(manga_obj.serialize())
        self.assertEqual(manga_obj, manga)
        self.assertEqual(manga.media_type, MediaType.MANGA)
        self.assertTrue(isinstance(manga, MangaData))

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        def attempt_deserialize(media_cls: type(MediaType), data: dict):
            try:
                media_cls.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

        for media_class, sample in [
            (AnimeData, self.generate_sample_serialized_anime_data()),
            (MangaData, self.generate_sample_serialized_manga_data())
        ]:
            for key, value in sample.items():

                for faux_value in [2000, "Hello", Id({IdType.KITSU: 1})]:
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
        one = self.generate_sample_anime_data()
        two = self.generate_sample_anime_data()

        self.assertEqual(one, two)

        two.id = Id({IdType.KITSU: 1})
        self.assertNotEqual(one, two)
        two = self.generate_sample_anime_data()

        two.releasing_start = None
        self.assertNotEqual(one, two)

        self.assertNotEqual(one, self.generate_sample_manga_data())

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        data = self.generate_sample_anime_data()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, AnimeData.deserialize(serialised))

        data = self.generate_sample_manga_data()
        representation = str(data)
        serialised = json.loads(representation)
        self.assertEqual(data, MangaData.deserialize(serialised))
