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

import os
import time
import json
from enum import Enum
from copy import deepcopy
from typing import Dict, Optional
from anime_list_apis.models.Serializable import Serializable
from anime_list_apis.models.attributes.Id import IdType, Id
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.MediaData import MediaData
from anime_list_apis.models.MediaUserData import MediaUserData
from anime_list_apis.models.MediaListEntry import MediaListEntry


class CacheType(Enum):
    """
    An enumeration that defines what sorts of data can be stored in the cache
    """
    MEDIA_DATA = MediaData
    USER_DATA = MediaUserData


class Cache:
    """
    Handles various caching functionality
    """

    def __init__(
            self,
            cache_location: str = None,
            expiration: int = 6000,
            write_after: int = 20
    ):
        """
        Initializes the Cache. If the Cache directory and file do not exist,
        they will be created here.
        :param cache_location: The location of the cache. Will default to a
                               hidden directory in the user's home directory
        :param expiration: Defines how long objects should be valid.
                           If set to a negative number, will be infinite
        :param write_after: Defines after how many cache changes the changes
                            are automatically written to the cache file
        """
        self.expiration = expiration
        self.write_after = write_after
        self.change_count = 0

        if cache_location is None:  # pragma: no cover
            self.cache_location = os.path.join(
                os.path.expanduser("~"), ".anime_list_apis"
            )
        else:
            self.cache_location = cache_location
        self.cache_file = os.path.join(self.cache_location, "cache.json")

        self.__cache = self.__generate_empty_cache()

        if not os.path.isdir(self.cache_location):
            os.makedirs(self.cache_location)

        if not os.path.isfile(self.cache_file):
            self.write()

        self.load()

    def write(self):
        """
        Writes the content of the cache to the cache file
        :return: None
        """
        serialized = {}

        for cache_type in self.__cache:
            serialized[cache_type.name] = {}

            for site_type in self.__cache[cache_type]:
                serialized[cache_type.name][site_type.name] = {}

                for tag in self.__cache[cache_type][site_type]:
                    serialized[cache_type.name][site_type.name][tag] = {
                        "timestamp":
                            self.__cache[cache_type][site_type][tag]
                            ["timestamp"],
                        "data":
                            self.__cache[cache_type][site_type][tag]
                            ["data"].serialize()
                    }

        with open(self.cache_file, "w") as f:
            json.dump(
                serialized,
                f,
                sort_keys=True,
                indent=4,
                separators=(",", ": ")
            )

    def load(self):
        """
        Loads the content of the cache file into memory
        :return: None
        """
        with open(self.cache_file, "r") as f:
            serialized = json.load(f)

        self.__cache = self.__generate_empty_cache()

        for _cache_type, cache_data in serialized.items():
            cache_type = CacheType[_cache_type]
            data_class = cache_type.value  # type: Serializable

            for _site_type, site_data in cache_data.items():
                site_type = IdType[_site_type]

                for tag, entry in site_data.items():
                    self.__cache[cache_type][site_type][tag] = {
                        "timestamp": entry["timestamp"],
                        "data": data_class.deserialize(entry["data"])
                    }

    def __add_cached(
            self,
            cache_type:
            CacheType,
            site_type: IdType,
            _id: int or Id,
            data: MediaData or MediaUserData,
            ignore_for_write_count: bool = False
    ):
        """
        Adds a copy of an object to the cache.
        If the amount of changes exceeds the amount defined in write_after,
        write to file afterwards
        :param cache_type: The type of data to cache
        :param site_type: The site for which to cache it
        :param _id: The ID of the object in the cache
        :param data: The data to cache
        :param ignore_for_write_count: If set to True, will not increment the
                                       change_count variable.
        :return: None
        """
        _id = self.__resolve_id(site_type, _id)
        if hasattr(data, "username"):
            username = data.username
        else:
            username = None
        tag = self.generate_id_tag(data.media_type, _id, username)

        self.__cache[cache_type][site_type][tag] = {
            "timestamp": time.time(),
            "data": deepcopy(data)
        }
        if not ignore_for_write_count:
            self.change_count += 1

        if self.change_count >= self.write_after:
            self.write()

    def add_media_data(
            self,
            site_type: IdType,
            data: MediaData,
            ignore_for_write_count: bool = False
    ):
        """
        Adds a media data object to the cache
        :param site_type: The site for which to add the entry
        :param data: The data object to add
        :param ignore_for_write_count: If set to True, will not increment the
                                       change_count variable.
        :return: None
        """
        _id = data.id.get(site_type)
        self.__add_cached(
            CacheType.MEDIA_DATA,
            site_type,
            _id,
            data,
            ignore_for_write_count
        )

    def add_media_user_data(
            self,
            site_type: IdType,
            _id: int or Id,
            data: MediaUserData,
            ignore_for_write_count: bool = False
    ):
        """
        Adds a user data object to the cache
        :param site_type: The type of the site
        :param _id: The ID of the corresponding media data
        :param data: The data to cache
        :param ignore_for_write_count: If set to True, will not increment the
                                       change_count variable.
        :return: None
        """
        self.__add_cached(
            CacheType.USER_DATA,
            site_type,
            _id,
            data,
            ignore_for_write_count
        )

    def add_media_list_entry(
            self,
            site_type: IdType,
            data: MediaListEntry,
            ignore_for_write_count: bool = False
    ):
        """
        Stores a media list entry in the cache
        :param site_type: The site type to store it for
        :param data: The data to store
        :param ignore_for_write_count: If set to True, will not increment the
                                       change_count variable.
        :return: None
        """
        self.add_media_data(
            site_type, data.get_media_data(), ignore_for_write_count
        )
        self.add_media_user_data(
            site_type, data.id, data.get_user_data(), ignore_for_write_count
        )

    def __get_cached(
            self,
            cache_type: CacheType,
            site_type: IdType,
            media_type: MediaType,
            _id: int or Id,
            username: Optional[str] = None
    ) -> Optional[MediaData or MediaUserData]:
        """
        Retrieves a cached object.
        If the object has expired, remove it from the cache
        :param cache_type: The cached data type
        :param site_type: The site type for which the object was cached
        :param media_type: The media type of the object to get
        :param _id: The ID to search for
        :param username: Optional-The username associated with the data object
        :return: A copy of the cached object, or None if it wasn't found
        """
        _id = self.__resolve_id(site_type, _id)
        tag = self.generate_id_tag(media_type, _id, username)

        if tag in self.__cache[cache_type][site_type]:
            entry = self.__cache[cache_type][site_type][tag]
            timestamp = entry["timestamp"]

            if time.time() - timestamp > self.expiration >= 0:
                self.__cache[cache_type][site_type].pop(tag)
                return None
            else:
                return deepcopy(entry["data"])
        else:
            return None

    def get_media_data(
            self,
            site_type: IdType,
            media_type: MediaType,
            _id: int or Id
    ) -> Optional[MediaData]:
        """
        Retrieves a media data entry from the cache
        :param site_type: The site for which to fetch an entry
        :param media_type: The type of the media
        :param _id: The ID to fetch
        :return: The entry data or None if no corresponding entry exists
        """
        return self.__get_cached(
            CacheType.MEDIA_DATA,
            site_type,
            media_type,
            _id
        )

    def get_media_user_data(
            self,
            site_type: IdType,
            media_type: MediaType,
            _id: int or Id,
            username: str
    ) -> Optional[MediaUserData]:
        """
        Retrieves a media user entry from the cache
        :param site_type: The site type for which the object was cached
        :param media_type: The media type of the cached object
        :param _id: The ID of the corresponding media data
        :param username: The username of the entry
        :return: The entry or None if not found
        """
        return self.__get_cached(
            CacheType.USER_DATA,
            site_type,
            media_type,
            _id,
            username
        )

    def get_media_list_entry(
            self,
            site_type: IdType,
            media_type: MediaType,
            _id: int or Id,
            username: str
    ) -> Optional[MediaListEntry]:
        """
        Retrieves a media list entry from the cache
        :param site_type: The site for which to fetch the cached object
        :param media_type: The media type of the entry
        :param _id: The ID of the entry
        :param username: The username of the entry
        :return: The entry or None if not found
        """
        media_data = self.get_media_data(site_type, media_type, _id)
        user_data = \
            self.get_media_user_data(site_type, media_type, _id, username)

        if media_data is not None and user_data is not None \
                and media_data.media_type == user_data.media_type \
                and media_type == media_data.media_type:

            media_class = MediaListEntry.get_class_for_media_type(media_type)
            return media_class(media_data, user_data)

        else:
            return None

    @staticmethod
    def __generate_empty_cache() \
            -> Dict[
                CacheType, Dict[
                    IdType, Dict[
                        str, Dict[
                            str, int or Serializable
                        ]
                    ]
                ]
            ]:
        """
        Generates a fresh cache.
        The cache has the following structure:

        {
            CacheType: {
                SiteType: {
                    MediaType + Id: {
                        "timestamp": float,
                        "data": data
                    }
                }
            }
        }

        :return: The generated cache dictionary
        """
        cache = {}
        for cache_type in CacheType:
            cache[cache_type] = {}
            for site_type in IdType:
                cache[cache_type][site_type] = {}
        return cache

    @staticmethod
    def __resolve_id(site_type: IdType, _id: int or Id) -> int:
        """
        Turns an ID into an int if it is not already
        :param site_type: The type of site for which to store the ID
        :param _id: The ID to convert
        :return: The int ID
        """
        if not isinstance(_id, int):
            return _id.get(site_type)
        else:
            return _id

    @staticmethod
    def generate_id_tag(
            media_type: MediaType,
            _id: int,
            username: Optional[str] = None
    ) -> str:
        """
        Generates an ID tag for the cache
        :param media_type: The media type of the tag
        :param _id: The ID of the entry
        :param username: Optionally create a tag for a specific username
        :return: The generated ID tag
        """
        tag = media_type.name + "-" + str(_id)
        if username is not None:
            tag += "-" + username
        return tag
