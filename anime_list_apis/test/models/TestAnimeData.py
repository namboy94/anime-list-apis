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
# from anime_list_apis.models.AnimeData import AnimeData
# from anime_list_apis.models.attributes.Id import Id, IdType
# from anime_list_apis.models.attributes.Title import Title, TitleType


class TestAnimeData(TestCase):
    """
    Tests the AnimeData Model class
    """

    def test_generating_anime_data(self):
        """
        Tests generating an anime data object
        :return: None
        """
        """
        data = AnimeData(
            Id({IdType.MYANIMELIST: 1}),
            Title({TitleType.ROMAJI: "Test"}),
            "Airing Status",
            "Episodes",
            "Relations",
            "Start Date",
            "End Date",
            "Episode Duration",
            "CoverUrl"
        )
        """
