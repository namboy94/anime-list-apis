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

from unittest import TestCase
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

    def test_generating_anime_data(self):
        """
        Tests generating an anime data object
        :return: None
        """
        id_one = Id({IdType.MYANIMELIST: 1})
        id_two = Id({IdType.MYANIMELIST: 2})
        title = Title({TitleType.ROMAJI: "Test"})
        relations = [Relation(id_one, id_two, RelationType.SEQUEL)]
        data = AnimeData(
            id_one,
            title,
            relations,
            AiringStatus.FINISHED,
            Date(2018, 1, 1),
            Date(2018, 4, 4),
            12,
            25,
            "https://example.com/image.png"
        )
        self.assertEqual(data.id, id_one)
        self.assertEqual(data.title, title)
        self.assertEqual(data.relations, relations)
        self.assertEqual(data.airing_state, AiringStatus.FINISHED)
        self.assertEqual(data.start_date, Date(2018, 1, 1))
        self.assertEqual(data.end_date, Date(2018, 4, 4))
        self.assertEqual(data.episodes, 12)
        self.assertEqual(data.runtime, 25)
        self.assertEqual(data.cover_url, "https://example.com/image.png")
