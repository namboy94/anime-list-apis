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

from typing import List, Optional
from anime_list_apis.cache.Cacher import Cacher
from anime_list_apis.models.MediaData import AnimeData
from anime_list_apis.models.MediaListEntry import AnimeListEntry
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType


class ApiInterface:
    """
    Defines methods that every API connector should implement
    """

    id_type = None  # type: IdType
    """
    The ID type of the API interface
    """

    def __init__(self, cache: Cacher = None):
        """
        Initializes the Api interface.
        Intializes cache or uses the one provided.
        :param cache: The cache to use. If left as None, will use default cache
        """
        self.cache = cache if cache is not None else Cacher()

    def get_data(
            self,
            media_type: MediaType,
            _id: int or Id
    ) -> Optional[AnimeData]:  # TODO Manga
        """
        Retrieves a single data object using the API
        Tries to get the cached value first, then checks Anilist
        :param media_type: The media type to retrieve
        :param _id: The ID to retrieve. May be either an int or an Id object
        :return: The Anime Data or None if no valid data was found
        """
        cached = self.cache.get(media_type, IdType.ANILIST, _id)

        if cached is None:
            cached = self._get_data(media_type, _id)

            if cached is not None:
                self.cache.add(media_type, self.id_type, cached)

        return cached

    def _get_data(
            self,
            media_type: MediaType,
            _id: int or Id
    ) -> Optional[AnimeData]:  # TODO Manga
        """
        Retrieves a single data object using the API
        Actual implementation should be done by subclasses
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
    ) -> Optional[AnimeListEntry]:  # TODO Manga
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

    def get_anime_data(self, _id: int or Id) \
            -> Optional[AnimeData]:
        """
        Shortcut for get_data that retrieves only Anime media
        :param _id: The ID to fetch. May be int or Id object
        :return: The retrieved AnimeData object or None if not a valid ID
        """
        return self.get_data(MediaType.ANIME, _id)

    def get_anime_list_entry(self, _id: int or Id, username: str) \
            -> Optional[AnimeListEntry]:
        """
        Retrieves a user's list entry for a single entry
        :param _id: The ID to fetch. May be int or an Id object
        :param username: The user for which to fetch the entry
        :return: The Anime List Entry or None if there is not such entry
        """
        return self.get_list_entry(MediaType.ANIME, _id, username)

    def get_anime_list(self, username: str) -> List[AnimeListEntry]:
        """
        Retrieves a user's complete anime list
        :param username: The user's username
        :return: The user's list of AnimeListEntry objects
        """
        return self.get_list(MediaType.ANIME, username)

    # TODO Manga shortcuts
