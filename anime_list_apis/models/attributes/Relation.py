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
from anime_list_apis.models.attributes.MediaType import MediaType


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
    ALTERNATIVE = 204


class Relation(Serializable):
    """
    Class that models a relation edge between two anime entries
    """

    def __init__(
            self,
            source: Id,
            source_type: MediaType,
            dest: Id,
            dest_type: MediaType,
            relation_type: RelationType
    ):
        """
        Initializes the Relation object.
        :param source: The source node in the relation edge
        :param source_type: The media type of the source node
        :param dest: The destination node in the relation edge
        :param dest_type: The destination node's media type
        :param relation_type: The type of the relation
        :raises TypeError: If invalid ID types are provided
                           or other types mismatch
        :raises ValueError: If both IDs are the same, i.e. an invalid relation
        """
        list(map(lambda x: self.ensure_type(x, Id), [source, dest]))
        list(map(
            lambda x: self.ensure_type(x, MediaType), [source_type, dest_type]
        ))
        self.ensure_type(relation_type, RelationType)

        if source == dest and source_type == dest_type:
            raise ValueError("Same ID")

        self.source, self.dest, self.type = source, dest, relation_type
        self.source_type, self.dest_type = source_type, dest_type

        # For easier access
        self.id, self.media_type = self.dest, self.dest_type

    def is_important(self) -> bool:
        """
        Checks if this relation is "important", meaning if it's a direct
        connection (Sequel, Prequel, Parent, Side Story or a summary) or not
        :return: True if the relation is important, False otherwise
        """
        # noinspection PyTypeChecker
        return 200 > self.type.value and self.source_type == self.dest_type

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {
            "source": self.source.serialize(),
            "source_type": self.source_type.name,
            "dest": self.dest.serialize(),
            "dest_type": self.dest_type.name,
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
        source_type = MediaType[data["source_type"]]
        dest = Id.deserialize(data["dest"])
        dest_type = MediaType[data["dest_type"]]
        relation_type = RelationType[data["type"]]
        generated = cls(
            source, source_type, dest, dest_type, relation_type
        )  # type: Relation
        return generated
