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

from enum import Enum
from typing import Optional
from anime_list_apis.models.attributes.Id import IdType, Id
from anime_list_apis.models.Serializable import Serializable
from anime_list_apis.models.attributes.MediaType import MediaType


class CacheModelType(Enum):
    """
    An enumeration that keeps track of different cache-able model types
    """
    MEDIA_DATA = 1
    MEDIA_USER_DATA = 2
    MEDIA_LIST_ENTRY = 3


# noinspection PyAbstractClass
class CacheAble(Serializable):
    """
    Class that defines methods needed to be implemented by a cache-able object
    """

    def generate_tag(self, site_type: IdType) -> str:
        """
        Generates a tag/identifier for storing in the cache
        :param site_type: The site type for which to generate the tag
        :return: The generated tag
        """
        _id = str(self.get_id().get(site_type))
        tag = self.get_media_type().name + "-" + _id
        username = self.get_username()

        if username is not None:
            tag += "-" + username
        return tag

    def get_id(self) -> Id:
        """
        Retrieves the cache entry's ID
        :return: The ID
        """
        raise NotImplementedError()  # pragma: no cover

    def get_media_type(self) -> MediaType:
        """
        Retrieves the media type
        :return: The media type
        """
        raise NotImplementedError()  # pragma: no cover

    def get_username(self) -> Optional[str]:
        """
        Retrieves the username, if applicable. Else None
        :return: The username or None if not applicable
        """
        raise NotImplementedError()  # pragma: no cover

    def get_model_type(self) -> CacheModelType:
        """
        Retrieves the cache model type
        :return: The model type
        """
        raise NotImplementedError()  # pragma: no cover
