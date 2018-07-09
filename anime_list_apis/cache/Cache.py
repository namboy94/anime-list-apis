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
from copy import deepcopy
from typing import Dict, Optional
from anime_list_apis.models.Serializable import Serializable
from anime_list_apis.models.attributes.Id import IdType, Id
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.MediaData import MediaData
from anime_list_apis.models.MediaUserData import MediaUserData
from anime_list_apis.models.MediaListEntry import MediaListEntry
from anime_list_apis.models.CacheAble import CacheModelType, CacheAble


class Cache:
    """
    Handles various caching functionality
    """

    model_map = {
        CacheModelType.MEDIA_DATA: MediaData,
        CacheModelType.MEDIA_USER_DATA: MediaUserData,
        CacheModelType.MEDIA_LIST_ENTRY: MediaListEntry
    }
    """
    Maps model types to their respective classes
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

        for model_type in self.__cache:
            serialized[model_type.name] = {}

            for site_type in self.__cache[model_type]:
                serialized[model_type.name][site_type.name] = {}

                for tag in self.__cache[model_type][site_type]:
                    serialized[model_type.name][site_type.name][tag] = {
                        "timestamp":
                            self.__cache[model_type][site_type][tag]
                            ["timestamp"],
                        "data":
                            self.__cache[model_type][site_type][tag]
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

        for _model_type, cache_data in serialized.items():
            model_type = CacheModelType[_model_type]
            data_class = self.model_map[model_type]  # type: Serializable

            for _site_type, site_data in cache_data.items():
                site_type = IdType[_site_type]

                for tag, entry in site_data.items():
                    self.__cache[model_type][site_type][tag] = {
                        "timestamp": entry["timestamp"],
                        "data": data_class.deserialize(entry["data"])
                    }

    def add(
            self,
            site_type: IdType,
            data: CacheAble,
            ignore_for_write_count: bool = False
    ):
        """
        Adds a copy of an object to the cache.
        If the amount of changes exceeds the amount defined in write_after,
        write to file afterwards
        :param site_type: The site for which to cache it
        :param data: The data to cache
        :param ignore_for_write_count: If set to True, will not increment the
                                       change_count variable.
        :return: None
        """
        if data.get_model_type() == CacheModelType.MEDIA_LIST_ENTRY:
            data = data  # type: MediaListEntry
            self.add(site_type, data.get_media_data(), ignore_for_write_count)
            self.add(site_type, data.get_user_data(), ignore_for_write_count)

        else:
            if data.get_model_type() == CacheModelType.MEDIA_USER_DATA:
                username = data.get_username()
            else:
                username = None

            _id = data.get_id().get(site_type)
            tag = self.generate_id_tag(data.get_media_type(), _id, username)

            self.__cache[data.get_model_type()][site_type][tag] = {
                "timestamp": time.time(),
                "data": deepcopy(data)
            }
            if not ignore_for_write_count:
                self.change_count += 1

            if self.change_count >= self.write_after:
                self.write()

    def get(
            self,
            model_type: CacheModelType,
            site_type: IdType,
            media_type: MediaType,
            _id: int or Id,
            username: Optional[str] = None
    ) -> Optional[CacheAble]:
        """
        Retrieves a cached object.
        If the object has expired, remove it from the cache
        :param model_type: The cached data type
        :param site_type: The site type for which the object was cached
        :param media_type: The media type of the object to get
        :param _id: The ID to search for
        :param username: Optional-The username associated with the data object
        :return: A copy of the cached object, or None if it wasn't found
        """
        if model_type == CacheModelType.MEDIA_LIST_ENTRY:
            media = self.get(
                CacheModelType.MEDIA_DATA,
                site_type,
                media_type,
                _id
            )
            user = self.get(
                CacheModelType.MEDIA_USER_DATA,
                site_type,
                media_type,
                _id,
                username
            )
            try:
                media_cls = MediaListEntry.get_class_for_media_type(media_type)
                return media_cls(media, user)
            except (ValueError, TypeError):
                return None

        else:
            _id = self.__resolve_id(site_type, _id)
            tag = self.generate_id_tag(media_type, _id, username)

            if tag in self.__cache[model_type][site_type]:
                entry = self.__cache[model_type][site_type][tag]
                timestamp = entry["timestamp"]

                if time.time() - timestamp > self.expiration >= 0:
                    self.__cache[model_type][site_type].pop(tag)
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
        return self.get(
            CacheModelType.MEDIA_DATA,
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
        return self.get(
            CacheModelType.MEDIA_USER_DATA,
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
        return self.get(
            CacheModelType.MEDIA_LIST_ENTRY,
            site_type,
            media_type,
            _id,
            username
        )

    @staticmethod
    def __generate_empty_cache() \
            -> Dict[
                CacheModelType, Dict[
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
            CacheModelType: {
                SiteType: {
                    MediaType + Id: {
                        "timestamp": float,
                        "data": data
                    }
                }
            }
        }

        The CacheModelType 'MediaListEntry' will be split into their
        'MediaData' and 'MediaUserData' components, so there will be no
        separate entry for them
        :return: The generated cache dictionary
        """
        cache = {}
        for model_type in CacheModelType:

            if model_type == CacheModelType.MEDIA_LIST_ENTRY:
                continue
            cache[model_type] = {}

            for site_type in IdType:
                cache[model_type][site_type] = {}
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
