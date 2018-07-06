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
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.Id import IdType
from anime_list_apis.test.api.TestApiInterface import TestApiInterface


class TestAnilistApi(TestApiInterface):
    """
    Tests the Anilist API Wrapper
    """

    api_class = AnilistApi
    """
    The API class to test
    """

    primary_id_type = IdType.ANILIST
    """
    The primary ID type
    """

    valid_id_types = [IdType.MYANIMELIST, IdType.ANILIST]
    """
    A list of valid ID types
    """
