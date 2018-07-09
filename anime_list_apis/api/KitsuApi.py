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
from anime_list_apis.api.ApiInterface import ApiInterface
from anime_list_apis.cache.Cache import Cache
from anime_list_apis.models.MediaData import MediaData
from anime_list_apis.models.MediaListEntry import MediaListEntry
from anime_list_apis.models.MediaUserData import MediaUserData
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType


class KitsuApi(ApiInterface):
    """
    Implements a wrapper around the kitsu.io API
    """

    def __init__(self, cache: Cache = None, rate_limit_pause: float = 0.0):
        """
        Initializes the Kitsu Api interface.
        Intializes cache or uses the one provided.
        :param cache: The cache to use. If left as None, will use default cache
        :param rate_limit_pause: A duration in seconds that the API Interface
                                 will pause after a network operation to
                                 prevent being rate limited
        """
        super().__init__(IdType.KITSU, cache, rate_limit_pause)

    def _get_data(
            self,
            media_type: MediaType,
            _id: Id
    ) -> Optional[MediaData]:
        """
        Retrieves a single data object using the API
        Actual implementation should be done by subclasses
        :param media_type: The media type to retrieve
        :param _id: The ID to retrieve.
        :return: The Anime Data or None if no valid data was found
        """
        raise NotImplementedError()  # pragma: no cover

    def _get_user_data(
            self,
            media_type: MediaType,
            _id: Id,
            username: str
    ) -> Optional[MediaUserData]:
        """
        Actual implementation of the get_user_data for each subclass
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve
        :param username: The user for which to fetch the data
        :return: The user data for the entry or
                 None if the user doesn't have such an entry
        """
        raise NotImplementedError()  # pragma: no cover

    def _get_user_data_list(self, media_type: MediaType, username: str) \
            -> List[MediaUserData]:
        """
        Retrieves a user's entire list of user data
        Actual implementation method to be implemented by subclasses
        :param media_type: The media type to fetch
        :param username: The username for which to fetch the list
        :return: The list of user data
        """
        raise NotImplementedError()  # pragma: no cover

    def _get_list_entry(
            self,
            media_type: MediaType,
            _id: Id,
            username: str
    ) -> Optional[MediaListEntry]:
        """
        Actual implementation of the get_list_entry for each subclass
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve
        :param username: The user for which to fetch the entry
        :return: The entry for the user or
                 None if the user doesn't have such an entry
        """
        raise NotImplementedError()  # pragma: no cover

    def _get_list(self, media_type: MediaType, username: str) \
            -> List[MediaListEntry]:
        """
        Retrieves a user's entire list
        Actual implementation method to be implemented by subclasses
        :param media_type: The media type to fetch
        :param username: The username for which to fetch the list
        :return: The list of List entries
        """
        raise NotImplementedError()  # pragma: no cover
