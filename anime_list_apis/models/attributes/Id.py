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
from typing import Dict, List, Tuple, Set, Optional
from anime_list_apis.models.Serializable import Serializable


class IdType(Enum):
    """
    Enumeration of different ID types
    """
    MYANIMELIST = 1
    ANILIST = 2
    KITSU = 3


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
        :raises TypeError: If an invalid parameter type was provided
        :raises ValueError: In case no valid ID was provided
        """
        self.ensure_type(ids, dict)
        ids = {
            key: value for key, value in ids.items()
            if self.type_check(value, int)
        }
        if len(ids) == 0:
            raise ValueError("At least one ID required")

        self.__ids = ids
        for id_type in IdType:
            if id_type not in self.__ids:
                # noinspection PyTypeChecker
                self.__ids[id_type] = None

    def get(self, id_type: IdType) -> Optional[int]:
        """
        Retrieves an ID for a given ID type
        :param id_type: The ID type to get
        :return: The ID. If it does not exist, return None
        """
        self.ensure_type(id_type, IdType)
        return self.__ids[id_type]

    def set(self, _id: int, id_type: IdType):
        """
        Sets an ID for a given ID type
        :param _id: The ID to set
        :param id_type: The type of ID for which to set the ID
        :return: None
        :raises TypeError: If the provided ID is not an integer
        """
        self.ensure_type(_id, int)
        self.__ids[id_type] = _id

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        data = {}
        for key, value in self.__ids.items():
            data[key.name] = value
        return data

    @classmethod
    def _deserialize(cls, data: Dict[str, Optional[str or int or float or bool
                                     or Dict or List or Tuple or Set]]):
        """
        Deserializes a dictionary into an object of this type
        :param data: The data to deserialize
        :return: The deserialized object
        :raises TypeError: If a type error occurred
        :raises ValueError: If the data could not be deserialized
        """
        des = {}
        for key, value in data.items():
            des[IdType[key]] = value
        generated = cls(des)  # type: Id
        return generated
