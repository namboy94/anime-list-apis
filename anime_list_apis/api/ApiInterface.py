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
from anime_list_apis.cache.Cache import Cache
from anime_list_apis.models.CacheAble import CacheAble
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.MediaData import AnimeData, MangaData, MediaData
from anime_list_apis.models.MediaUserData import \
    MediaUserData, AnimeUserData, MangaUserData
from anime_list_apis.models.MediaListEntry import \
    AnimeListEntry, MangaListEntry, MediaListEntry


class ApiInterface:
    """
    Defines methods that every API connector should implement
    """

    def __init__(
            self,
            id_type: IdType,
            cache: Cache = None,
            rate_limit_pause: float = 0.0
    ):
        """
        Initializes the Api interface.
        Intializes cache or uses the one provided.
        :param id_type: TheID type of the API Interface
        :param cache: The cache to use. If left as None, will use default cache
        :param rate_limit_pause: A duration in seconds that the API Interface
                                 will pause after a network operation to
                                 prevent being rate limited
        """
        self.cache = cache if cache is not None else Cache()
        self.id_type = id_type
        self.rate_limit_pause = rate_limit_pause

    # Public Methods ----------------------------------------------------------

    def get_data(
            self,
            media_type: MediaType,
            _id: int or Id,
            fresh: bool = False
    ) -> Optional[MediaData]:
        """
        Retrieves a single data object using the API
        Tries to get the cached value first, then checks Anilist
        :param media_type: The media type to retrieve
        :param _id: The ID to retrieve. May be either an int or an Id object
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The Media Data or None if no valid data was found
        """
        cached = self.cache.get_media_data(IdType.ANILIST, media_type, _id)

        if fresh or cached is None:
            cached = self._get_data(media_type, self.__generate_id_obj(_id))
            self.__cache(cached)

        return cached

    def get_user_data(
            self,
            media_type: MediaType,
            _id: int or Id,
            username: str,
            fresh: bool = True
    ) -> Optional[MediaUserData]:
        """
        Retrieves the user data of a single entry for a user
        :param media_type: The type of media to fetch
        :param _id: The ID to fetch
        :param username: The username for which to fetch
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The MediaUserData object or None if not found
        """
        cached = self.cache.get_media_user_data(
            IdType.ANILIST, media_type, _id, username
        )

        if fresh or cached is None:
            cached = self._get_user_data(
                media_type, self.__generate_id_obj(_id), username
            )
            self.__cache(cached)

        return cached

    def get_user_data_list(
            self,
            media_type: MediaType,
            username: str
    ) -> List[MediaUserData]:
        """
        Retrieves a user's entire list with only the user data
        :param media_type: The media type to fetch the entries for
        :param username: The user for whom to fetch the entries for
        :return: The retrieves user data in a list
        """
        data = self._get_user_data_list(media_type, username)
        for obj in data:
            self.__cache(obj, dont_write=True)
        return data

    def get_list_entry(
            self,
            media_type: MediaType,
            _id: int or Id,
            username: str,
            fresh: bool = False
    ) -> Optional[MediaListEntry]:
        """
        Retrieves a user list entry.
        First checks for cached entries, otherwise fetches from anilist
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve. May be and int or an Id object
        :param username: The user for which to fetch the entry
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The entry for the user or
                 None if the user doesn't have such an entry
        """
        cached = self.cache.get_media_list_entry(
            IdType.ANILIST, media_type, _id, username
        )

        if fresh or cached is None:
            cached = self._get_list_entry(
                media_type,
                self.__generate_id_obj(_id),
                username
            )
            self.__cache(cached)

        return cached

    def get_list(
            self,
            media_type: MediaType,
            username: str
    ) -> List[MediaListEntry]:
        """
        Retrieves a user's entire list
        Stores all entries in the cache upon completion
        :param media_type: The media type to fetch
        :param username: The username for which to fetch the list
        :return: The list of List entries
        """
        entries = self._get_list(media_type, username)
        for entry in entries:
            self.__cache(entry, dont_write=True)
        return entries

    # Abstract Methods --------------------------------------------------------

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

    # Shortcut Methods --------------------------------------------------------

    def get_anime_data(self, _id: int or Id, fresh: bool = False) \
            -> Optional[AnimeData]:
        """
        Shortcut for get_data that retrieves only Anime media
        :param _id: The ID to fetch. May be int or Id object
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The retrieved AnimeData object or None if not a valid ID
        """
        return self.get_data(MediaType.ANIME, _id, fresh)

    def get_anime_user_data(
            self,
            _id: int or Id,
            username: str,
            fresh: bool = False
    ) -> Optional[AnimeUserData]:
        """
        Retrieves a user's user data for a single entry
        :param _id: The ID to fetch. May be int or an Id object
        :param username: The user for which to fetch the user data
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The AnimeUserData or None if there is not such entry
        """
        return self.get_user_data(MediaType.ANIME, _id, username, fresh)

    def get_anime_user_data_list(self, username: str) -> List[AnimeUserData]:
        """
        Retrieves a user's complete anime list of user data objects
        :param username: The user's username
        :return: The user's list of AnimeUserData objects
        """
        # noinspection PyTypeChecker
        return self.get_user_data_list(MediaType.ANIME, username)

    def get_anime_list_entry(
            self,
            _id: int or Id,
            username: str,
            fresh: bool = False
    ) -> Optional[AnimeListEntry]:
        """
        Retrieves a user's list entry for a single entry
        :param _id: The ID to fetch. May be int or an Id object
        :param username: The user for which to fetch the entry
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The Anime List Entry or None if there is not such entry
        """
        return self.get_list_entry(MediaType.ANIME, _id, username, fresh)

    def get_anime_list(self, username: str) -> List[AnimeListEntry]:
        """
        Retrieves a user's complete anime list
        :param username: The user's username
        :return: The user's list of AnimeListEntry objects
        """
        # noinspection PyTypeChecker
        return self.get_list(MediaType.ANIME, username)

    def get_manga_data(self, _id: int or Id, fresh: bool = False) \
            -> Optional[MangaData]:
        """
        Shortcut for get_data that retrieves only Manga media
        :param _id: The ID to fetch. May be int or Id object
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The retrieved MangaData object or None if not a valid ID
        """
        return self.get_data(MediaType.MANGA, _id, fresh)

    def get_manga_user_data(
            self,
            _id: int or Id,
            username: str,
            fresh: bool = False
    ) -> Optional[MangaUserData]:
        """
        Retrieves a user's user data for a single entry
        :param _id: The ID to fetch. May be int or an Id object
        :param username: The user for which to fetch the user data
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The MangaUserData or None if there is not such entry
        """
        return self.get_user_data(MediaType.MANGA, _id, username, fresh)

    def get_manga_user_data_list(self, username: str) -> List[AnimeUserData]:
        """
        Retrieves a user's complete manga list of user data objects
        :param username: The user's username
        :return: The user's list of MangaUserData objects
        """
        # noinspection PyTypeChecker
        return self.get_user_data_list(MediaType.MANGA, username)

    def get_manga_list_entry(
            self,
            _id: int or Id,
            username: str,
            fresh: bool = False
    ) -> Optional[MangaListEntry]:
        """
        Retrieves a user's list entry for a single entry
        :param _id: The ID to fetch. May be int or an Id object
        :param username: The user for which to fetch the entry
        :param fresh: Fetches a fresh, i.e. non-cached version
        :return: The Manga List Entry or None if there is not such entry
        """
        return self.get_list_entry(MediaType.MANGA, _id, username, fresh)

    def get_manga_list(self, username: str) -> List[MangaListEntry]:
        """
        Retrieves a user's complete manga list
        :param username: The user's username
        :return: The user's list of MangaListEntry objects
        """
        # noinspection PyTypeChecker
        return self.get_list(MediaType.MANGA, username)

    # Helper Methods ----------------------------------------------------------

    def __cache(self, data: Optional[CacheAble], dont_write: bool = True):
        """
        Caches a cache-able data object
        :param data: The data object to cache
        :param dont_write: Will make sure that the cache won't be written to
                           file.
        :return: None
        """
        if data is not None:
            self.cache.add(
                self.id_type, data, ignore_for_write_count=dont_write
            )

    def __generate_id_obj(self, _id: int or Id) -> Id:
        """
        Generates an Id object if the given ID is an integer
        :param _id: The ID to make sure is an Id object
        :return: The generated Id object
        """
        if isinstance(_id, int):
            _id = Id({self.id_type: _id})
        return _id
