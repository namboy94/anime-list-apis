from typing import Dict, List, Tuple, Set


class Serializable:

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
