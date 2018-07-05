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
from typing import Dict, List, Tuple, Set


class Serializable:
    """
    Abstract class that defines methods for subclasses to implement to make
    sure that they can be serialized
    """

    def serialize(self) -> Dict[str, str or int or float or bool or None
                                or Dict or List or Tuple or Set]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return self._serialize()

    def _serialize(self) -> Dict[str, str or int or float or bool or None
                                 or Dict or List or Tuple or Set]:
        """
        Implements the serialization of the object
        :return: The serialized form of this object
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def deserialize(cls, data: Dict[str, str or int or float or bool or None
                                    or Dict or List or Tuple or Set]):
        """
        Deserializes a dictionary into an object of this type
        :param data: The data to deserialize
        :return: The deserialized object
        :raises TypeError: If a type error occurred
        :raises ValueError: If the data could not be deserialized
        """
        cls.ensure_type(data, dict)
        return cls._deserialize(data)  # type: cls

    @classmethod
    def _deserialize(cls, data: Dict[str, str or int or float or bool or None
                                     or Dict or List or Tuple or Set]):
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
        By default, this prints valid JSON.
        :return: The string representation of this object
        """
        return json.dumps(self.serialize())

    @staticmethod
    def type_check(obj: object, typ: type) -> bool:
        """
        Checks if an object is an instance of a type
        :param obj: The object to check
        :param typ: The type it should be
        :return: True if the object is of that type, else False
        """
        if not isinstance(obj, typ):
            return False

        # Since bools are ints, make sure that an int object
        # isn't actually a bool
        elif typ == int:
            return not isinstance(obj, bool)

        else:
            return True

    @classmethod
    def ensure_type(cls, obj: object, typ: type):
        """
        Raises a TypeError if the object does not match the type
        :param obj: The object to check
        :param typ: The type the object should be
        :return: None
        :raises TypeError: If the types do not match
        """
        if not cls.type_check(obj, typ):
            raise TypeError(str(obj) + " is not of type " + str(typ))
