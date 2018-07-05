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
from anime_list_apis.models.attributes.Date import Relation, RelationType
from anime_list_apis.models.attributes.Id import Id, IdType


class TestRelation(TestCase):
    """
    Tests the Relation Attribute class
    """

    def test_serialization(self):
        """
        Tests serializing a Relation object
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        ob = Relation(source, dest, RelationType.SEQUEL)
        data = ob.serialize()

        self.assertEqual(
            data,
            {
                "source": source.serialize(),
                "dest": dest.serialize(),
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
            "dest": dest.serialize(),
            "type": "SEQUEL"
        }
        self.assertEqual(
            Relation.deserialize(data),
            Relation(source, dest, RelationType.SEQUEL)
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1}).serialize()
        dest = Id({IdType.MYANIMELIST: 2}).serialize()
        for data in [
            {"source": source, "dest": dest, "type": "Sequel"},
            {"source": source, "dest": None, "type": "SEQUEL"},
            {"source": None, "dest": dest, "type": "SEQUEL"},
            {"source": source, "dest": dest},
            {"source": source, "type": "SEQUEL"},
            {"dest": dest, "type": "SEQUEL"},
        ]:
            try:
                Relation.deserialize(data)
                self.fail()
            except ValueError:
                pass

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        id_one = Id({IdType.MYANIMELIST: 1}).serialize()
        id_two = Id({IdType.MYANIMELIST: 2}).serialize()
        id_three = Id({IdType.MYANIMELIST: 3}).serialize()

        one = Relation(id_one, id_two, RelationType.SEQUEL)
        two = Relation(id_one, id_two, RelationType.SEQUEL)
        three = Relation(id_one, id_three, RelationType.SEQUEL)
        four = Relation(id_one, id_two, RelationType.ADAPTATION)

        self.assertNotEqual(one, "Test")
        self.assertEqual(one, two)
        self.assertNotEqual(two, three)
        self.assertNotEqual(two, four)
        self.assertNotEqual(three, four)

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        source = Id({IdType.MYANIMELIST: 1})
        dest = Id({IdType.MYANIMELIST: 2})
        relation = Relation(source, dest, RelationType.SEQUEL)
        representation = str(relation)
        serialised = json.loads(representation)
        self.assertEqual(relation, Relation.deserialize(serialised))
