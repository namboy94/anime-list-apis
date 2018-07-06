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
import json
from typing import Dict

from anime_list_apis.models.AnimeData import AnimeData
from anime_list_apis.models.attributes.Id import IdType, Id
from anime_list_apis.models.attributes.MediaType import MediaType


class Cacher:
    """
    Handles various caching functionality
    """

    def __init__(self, cache_location: str = None):
        """
        Initializes the Cache. If the Cache directory and file do not exist,
        they will be created here.
        :param cache_location: The location of the cache. Will default to a
                               hidden directory in the user's home directory
        """
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

        for media_type in self.__cache:
            serialized[media_type.name] = {}

            for site_type in self.__cache[media_type]:
                serialized[media_type.name][site_type.name] = {}

                for _id in self.__cache[media_type][site_type]:
                    entry = self.__cache[media_type][site_type][_id]
                    data = entry.serialize()
                    serialized[media_type.name][site_type.name][_id] = data

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

        for _media_type, media_data in serialized.items():
            media_type = MediaType[_media_type]

            for _site_type, site_data in media_data.items():
                site_type = IdType[_site_type]

                for _id, data in site_data.items():

                    if media_type == MediaType.ANIME:
                        entry = AnimeData.deserialize(data)
                    else:
                        continue  # TODO Implement Manga

                    self.__cache[media_type][site_type][int(_id)] = entry

    def add(
            self,
            media_type: MediaType,
            site_type: IdType,
            entry: AnimeData  # TODO Add Manga
    ):
        """
        Adds an entry to the cache
        :param media_type: The media type to add
        :param site_type: The site for which to add the entry
        :param entry: The entry to add
        :return: None
        """
        _id = entry.id.get(site_type)
        self.__cache[media_type][site_type][_id] = entry

    def get(self, media_type: MediaType, site_type: IdType, _id: int or Id) \
            -> AnimeData or None:  # TODO Manga
        """
        Retrieves an entry from the cache
        :param media_type: The type of the media
        :param site_type: The site for which to fetch an entry
        :param _id: The ID to fetch
        :return: The entry data or None if no corresponding entry exists
        """
        if not isinstance(_id, int):
            _id = _id.get(site_type)

        if _id in self.__cache[media_type][site_type]:
            return self.__cache[media_type][site_type][_id]
        else:
            return None

    @staticmethod
    def __generate_empty_cache() \
            -> Dict[MediaType,
                    Dict[IdType,
                         Dict[int, AnimeData]]]:  # TODO Manga
        """
        Generates a fresh cache
        :return: The generated cache dictionary
        """
        cache = {}
        for media_type in MediaType:
            cache[media_type] = {}
            for site_type in IdType:
                cache[media_type][site_type] = {}
        return cache
