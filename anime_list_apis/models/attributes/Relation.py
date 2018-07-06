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
from anime_list_apis.models.attributes.Id import Id


class RelationType(Enum):
    """
    An enumeration modelling the different kinds of relations between
    entries.
    """
    PREQUEL = 100
    SEQUEL = 101
    PARENT = 102
    SIDE_STORY = 103
    SUMMARY = 104
    CHARACTER = 200
    SPIN_OFF = 201
    OTHER = 202
    ADAPTATION = 203


class Relation(Serializable):
    """
    Class that models a relation edge between two anime entries
    """

    def __init__(self, source: Id, dest: Id, relation_type: RelationType):
        """
        Initializes the Relation object.
        :param source: The source node in the relation edge
        :param dest: The destination node in the relation edge
        :param relation_type: The type of the relation
        :raises TypeError: If invalid ID types are provided
                           or other types mismatch
        :raises ValueError: If both IDs are the same, i.e. an invalid relation
        """
        list(map(lambda x: self.ensure_type(x, Id), [source, dest]))
        self.ensure_type(relation_type, RelationType)

        if source == dest:
            raise ValueError("Same ID")

        self.source, self.dest, self.type = source, dest, relation_type
        self.id = self.dest  # For easier access

    def is_important(self) -> bool:
        """
        Checks if this relation is "important", meaning if it's a direct
        connection (Sequel, Prequel, Parent, Side Story or a summary) or not
        :return: True if the relation is important, False otherwise
        """
        # noinspection PyTypeChecker
        return 200 > self.type.value

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {
            "source": self.source.serialize(),
            "dest": self.dest.serialize(),
            "type": self.type.name
        }

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
        source = Id.deserialize(data["source"])
        dest = Id.deserialize(data["dest"])
        relation_type = RelationType[data["type"]]
        generated = cls(source, dest, relation_type)  # type: Relation
        return generated
