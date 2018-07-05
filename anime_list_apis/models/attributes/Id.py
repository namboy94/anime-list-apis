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

from enum import Enum, auto
from typing import Dict, List, Tuple, Set
from anime_list_apis.models.Serializable import Serializable


class IdType(Enum):
    """
    Enumeration of different ID types
    """
    MYANIMELIST = auto()
    ANILIST = auto()
    KITSU = auto()


class Id(Serializable):
    """
    Class that models an ID. Has the capability to store different ID types
    """

    def __init__(self, ids: Dict[IdType, int]):
        """
        Initializes the ID. The IDs are set using a dictionary mapping
        IDs to the different ID types. At least one entry is required.
        Missing IDs will be replaced with None
        :param ids: The IDs mapped to an IdType
        :raises ValueError: In case no valid ID was provided
        """
        ids = {
            key: value for key, value in ids.items() if value is not None
        }
        if len(ids) == 0:
            raise ValueError("At least one ID required")

        self.__ids = ids
        for id_type in IdType:
            if id_type not in self.__ids:
                # noinspection PyTypeChecker
                self.__ids[id_type] = None

        print(self.__ids)

    def get(self, id_type: IdType) -> int or None:
        """
        Retrieves an ID for a given ID type
        :param id_type: The ID type to get
        :return: The ID. If it does not exist, return None
        """
        return self.__ids[id_type]

    def set(self, _id: int, id_type: IdType):
        """
        Sets an ID for a given ID type
        :param _id: The ID to set
        :param id_type: The type of ID for which to set the ID
        :return: None
        :raises TypeError: If the provided ID is not an integer
        """
        if not isinstance(_id, int):
            raise TypeError("Not an integer")
        else:
            self.__ids[id_type] = _id

    def serialize(self) -> Dict[str, str or int or float or bool or None
                                or Dict or List or Tuple or Set]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data: Dict[str, str or int or float or bool or None
                                    or Dict or List or Tuple or Set]):
        """
        Deserializes a dictionary into an object of this type
        :param data: The data to deserialize
        :return: The deserialized object
        :raises ValueError: If the data could not be deserialized
        """
        raise NotImplementedError()

    def _equals(self, other: object) -> bool:
        """
        Checks if this object is equal to another object.
        The object is guaranteed to be an instance of this class or a subclass
        :param other: The other object to compare this object to
        :return: True if the objects are equal, False otherwise
        """
        raise NotImplementedError()
