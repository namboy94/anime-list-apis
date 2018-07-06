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

from typing import List
from anime_list_apis.api.ApiInterface import ApiInterface
from anime_list_apis.models.AnimeData import AnimeData
from anime_list_apis.models.AnimeListEntry import AnimeListEntry
from anime_list_apis.models.attributes.Id import Id
from anime_list_apis.models.attributes.MediaType import MediaType


class KitsuApi(ApiInterface):
    """
    Implements a wrapper around the kitsu.io API
    """

    def get_data(
            self,
            media_type: MediaType,
            _id: int or Id
    ) -> AnimeData or None:  # TODO Manga
        """
        Retrieves a single data object using the API
        :param media_type: The media type to retrieve
        :param _id: The ID to retrieve. May be either an int or an Id object
        :return: The Anime Data or None if no valid data was found
        """
        raise NotImplementedError()

    def get_list_entry(
            self,
            media_type: MediaType,
            _id: int or Id,
            username: str
    ) -> AnimeListEntry:  # TODO Manga
        """
        Retrieves a user list entry
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve. May be and int or an Id object
        :param username: The user for which to fetch the entry
        :return: The entry for the user or
                 None if the user doesn't have such an entry
        """
        raise NotImplementedError()

    def get_list(self, media_type: MediaType, username: str) \
            -> List[AnimeListEntry]:  # TODO Manga
        """
        Retrieves a user's entire list
        :param media_type: The media type to fetch
        :param username: The username for which to fetch the list
        :return: The list of List entries
        """
        raise NotImplementedError()
