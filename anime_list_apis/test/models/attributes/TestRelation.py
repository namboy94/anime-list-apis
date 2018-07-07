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
from unittest import TestCase

from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.Id import Id, IdType


class TestRelation(TestCase):
    """
    Tests the Relation Attribute class
    """

    def test_invalid_constructor_parameters(self):
        """
        Tests using invalid parameter types with the constructor
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        for parameters in [
            (None, MediaType.ANIME, dest, MediaType.ANIME,
             RelationType.SEQUEL),
            (source, MediaType.ANIME, None, MediaType.ANIME,
             RelationType.SEQUEL),
            (source, MediaType.ANIME, dest, MediaType.ANIME, None),
            (1, MediaType.ANIME, 2, MediaType.ANIME, RelationType.SEQUEL),
            (True, MediaType.ANIME, False, MediaType.ANIME,
             RelationType.SEQUEL),
            (source, MediaType.ANIME, dest, MediaType.ANIME, "SEQUEL"),
            (source, "ANIME", dest, MediaType.ANIME, RelationType.SEQUEL),
            (source, MediaType.ANIME, dest, "MANGA", RelationType.SEQUEL)
        ]:
            try:
                Relation(*parameters)
                self.fail()
            except TypeError:
                pass

    def test_important_relations(self):
        """
        Tests if relations are correctly identified as "important"
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        for relation_type, important in {
            RelationType.SEQUEL: True,
            RelationType.PREQUEL: True,
            RelationType.PARENT: True,
            RelationType.SIDE_STORY: True,
            RelationType.SUMMARY: True,
            RelationType.SPIN_OFF: False,
            RelationType.CHARACTER: False,
            RelationType.ADAPTATION: False,
            RelationType.OTHER: False
        }.items():
            same_type_relation = Relation(
                source, MediaType.ANIME, dest, MediaType.ANIME, relation_type
            )
            self.assertEqual(same_type_relation.is_important(), important)
            other_type_relation = Relation(
                source, MediaType.ANIME, dest, MediaType.MANGA, relation_type
            )
            self.assertFalse(other_type_relation.is_important())

    def test_using_same_ids(self):
        """
        Makes sure that using the same ID for both the source and the
        destination results in an error
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        try:
            Relation(
                source, MediaType.ANIME,
                source, MediaType.ANIME,
                RelationType.OTHER
            )
            self.fail()
        except ValueError:
            pass

        Relation(
            source, MediaType.ANIME,
            source, MediaType.MANGA,
            RelationType.OTHER
        )

    def test_serialization(self):
        """
        Tests serializing a Relation object
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        ob = Relation(
            source, MediaType.ANIME, dest, MediaType.MANGA, RelationType.SEQUEL
        )
        data = ob.serialize()

        self.assertEqual(
            data,
            {
                "source": source.serialize(),
                "source_type": "ANIME",
                "dest": dest.serialize(),
                "dest_type": "MANGA",
                "type": "SEQUEL"
            }
        )

    def test_deserialization(self):
        """
        Tests deserializing an ID object
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        data = {
            "source": source.serialize(),
            "source_type": "ANIME",
            "dest": dest.serialize(),
            "dest_type": "MANGA",
            "type": "SEQUEL"
        }
        self.assertEqual(
            Relation.deserialize(data),
            Relation(
                source, MediaType.ANIME,
                dest, MediaType.MANGA,
                RelationType.SEQUEL
            )
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1}).serialize()
        dest = Id({IdType.MYANIMELIST: 2}).serialize()
        for data in [
            {"source": source, "dest": dest, "type": "Sequel",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": source, "dest": None, "type": "SEQUEL",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": None, "dest": dest, "type": "SEQUEL",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": source, "dest": dest,
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": source, "type": "SEQUEL",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"dest": dest, "type": "SEQUEL",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": 1, "dest": dest, "type": "Sequel",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": source, "dest": 2, "type": "Sequel",
             "source_type": "ANIME", "dest_type": "MANGA"},
            {"source": source, "dest": dest, "type": "Sequel"},
            []
        ]:
            try:
                Relation.deserialize(data)
                self.fail()
            except (ValueError, TypeError):
                pass

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        id_one = Id({IdType.MYANIMELIST: 1})
        id_two = Id({IdType.MYANIMELIST: 2})
        id_three = Id({IdType.MYANIMELIST: 3})

        one = Relation(id_one, MediaType.ANIME,
                       id_two, MediaType.ANIME, RelationType.SEQUEL)
        two = Relation(id_one, MediaType.ANIME,
                       id_two, MediaType.ANIME, RelationType.SEQUEL)
        three = Relation(id_one, MediaType.ANIME,
                         id_three, MediaType.ANIME, RelationType.SEQUEL)
        four = Relation(id_one, MediaType.ANIME,
                        id_two, MediaType.ANIME, RelationType.ADAPTATION)
        five = Relation(id_one, MediaType.ANIME,
                        id_two, MediaType.MANGA, RelationType.SEQUEL)

        self.assertNotEqual(one, "Test")
        self.assertEqual(one, two)
        self.assertNotEqual(two, three)
        self.assertNotEqual(two, four)
        self.assertNotEqual(three, four)
        self.assertNotEqual(one, five)

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        relation = Relation(source, MediaType.ANIME,
                            dest, MediaType.ANIME, RelationType.SEQUEL)
        representation = str(relation)
        serialised = json.loads(representation)
        self.assertEqual(relation, Relation.deserialize(serialised))
