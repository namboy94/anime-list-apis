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

import json
from copy import deepcopy
from typing import Dict, List, Tuple, Set, Optional

from anime_list_apis.models.attributes.MediaType import MediaType


class Serializable:
    """
    Abstract class that defines methods for subclasses to implement to make
    sure that they can be serialized
    """

    def serialize(self) -> Dict[str, Optional[str or int or float or bool
                                or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return self._serialize()

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Implements the serialization of the object
        :return: The serialized form of this object
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def deserialize(cls, data: Dict[str, Optional[str or int or float or bool
                                    or Dict or List or Tuple or Set]]):
        """
        Deserializes a dictionary into an object of this type
        :param data: The data to deserialize
        :return: The deserialized object
        :raises TypeError: If a type error occurred
        :raises ValueError: If the data could not be deserialized
        """
        cls.ensure_type(data, dict)
        try:
            return cls._deserialize(data)  # type: cls
        except KeyError as e:
            raise ValueError("Missing key: " + str(e))

    @classmethod
    def _deserialize(cls, data: Dict[str, Optional[str or int or float or bool
                                     or Dict or List or Tuple or Set]]):
        """
        Implements the deserialisation of this object
        :param data: The data to deserialize
        :return: The deserialized object
        :raises TypeError: If a type error occurred
        :raises ValueError: If the data could not be deserialized
        """
        raise NotImplementedError()  # pragma: no cover

    def _equals(self, other: object) -> bool:
        """
        Checks if this object is equal to another object.
        The object is guaranteed to be an instance of this class or a subclass
        :param other: The other object to compare this object to
        :return: True if the objects are equal, False otherwise
        """
        # noinspection PyUnresolvedReferences
        return self.serialize() == other.serialize()

    def __eq__(self, other: object) -> bool:
        """
        Compares another object with this one.
        :param other: The other object with which to compare this object with
        :return: True if the objects are equal, False otherwise
        """
        if not isinstance(other, type(self)):
            return False
        else:
            return self._equals(other)

    def __str__(self) -> str:
        """
        Generates a string representation of this object.
        By default, this returns valid JSON.
        :return: The string representation of this object
        """
        return json.dumps(self.serialize())

    @staticmethod
    def type_check(obj: object, typ: type, none_allowed: bool = False) -> bool:
        """
        Checks if an object is an instance of a type
        :param obj: The object to check
        :param typ: The type it should be
        :param none_allowed: If True, allows None values
        :return: True if the object is of that type, else False
        """
        if none_allowed and obj is None:
            return True

        elif not isinstance(obj, typ):
            return False

        # Since bools are ints, make sure that an int object
        # isn't actually a bool
        elif typ == int:
            return not isinstance(obj, bool)

        else:
            return True

    @classmethod
    def ensure_type(cls, obj: object, typ: type, none_allowed: bool = False):
        """
        Raises a TypeError if the object does not match the type
        :param obj: The object to check
        :param typ: The type the object should be
        :param none_allowed: If True, allows None values
        :return: None
        :raises TypeError: If the types do not match
        """
        if not cls.type_check(obj, typ, none_allowed):
            raise TypeError(str(obj) + " is not of type " + str(typ))


# noinspection PyAbstractClass
class MediaSerializable(Serializable):
    """
    Class that allows for easier subclassing of Media classes
    """

    @classmethod
    def get_class_for_media_type(cls, media_type: MediaType):
        """
        Maps a class to a media type
        :param media_type: The media type
        :return: The class mapped to that media type
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def _get_common_deserialized_components(
            cls,
            data: Dict[str, Optional[str or int or float or bool or
                                     Dict or List or Tuple or Set]]) \
            -> Dict[str, Optional[str or int or float or bool or
                                  Dict or List or Tuple or Set]]:
        """
        Deserializes the common child components of the data dictionary
        :param data: The data to deserialize
        :return: The deserialized dictionary
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def _get_specific_deserialized_components(
            cls,
            data: Dict[str, Optional[str or int or float or bool or
                                     Dict or List or Tuple or Set]]) \
            -> Dict[str, Optional[str or int or float or bool or
                                  Dict or List or Tuple or Set]]:
        """
        Deserializes class-specific child components of the data dictionary
        :param data: The data to deserialize
        :return: The deserialized dictionary
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def _get_common_parameter_order(cls) -> List[str]:
        """
        Generates an order of constructor parameters for the common attributes
        used for media classes
        :return: The order of common parameters
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def _get_additional_parameter_order(cls) -> List[str]:
        """
        Generates the order of class-specific additional constructor parameters
        :return: The order of the additional parameters
        """
        raise NotImplementedError()  # pragma: no cover

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
        data = deepcopy(data)  # To make sure not to change the original data

        # Auto-resolve the subclass to use
        _cls = cls.get_class_for_media_type(
            MediaType[data["media_type"]]
        )  # type: MediaSerializable

        deserialized_data = \
            _cls._get_common_deserialized_components(data)
        # noinspection PyProtectedMember
        specific_deserialized_data = \
            _cls._get_specific_deserialized_components(data)

        for key, value in specific_deserialized_data.items():
            deserialized_data[key] = value

        # noinspection PyProtectedMember
        parameter_order = \
            _cls._get_common_parameter_order() + \
            _cls._get_additional_parameter_order()

        params = tuple(map(lambda x: deserialized_data[x], parameter_order))

        # noinspection PyCallingNonCallable
        return _cls(*params)  # type: type(_cls)
