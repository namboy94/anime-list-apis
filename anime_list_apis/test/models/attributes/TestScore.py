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
from anime_list_apis.models.attributes.Score import Score, ScoreType


class TestScore(TestCase):
    """
    Tests the Score Attribute class
    """

    def test_invalid_constructor_parameters(self):
        """
        Tests using invalid parameter types with the constructor
        :return: None
        """
        for parameters in [
            (1, 1),
            (ScoreType.TEN_POINT, ScoreType.TEN_POINT),
            (True, ScoreType.TEN_POINT),
            (None, ScoreType.TEN_POINT)
        ]:
            try:
                Score(*parameters)
                self.fail()
            except TypeError:
                pass

    def test_initializing_different_score_types(self):
        """
        Tests initializing all types of scores with equivalent
        :return:
        """

        three = Score(3, ScoreType.THREE_POINT)
        five = Score(4, ScoreType.FIVE_POINT)
        ten = Score(8, ScoreType.TEN_POINT)
        ten_deci = Score(16, ScoreType.TEN_POINT_DECIMAL)
        hundred = Score(80, ScoreType.PERCENTAGE)

        self.assertEqual(three.get(), 3)
        self.assertEqual(three.mode, ScoreType.THREE_POINT)
        self.assertEqual(five.get(), 4)
        self.assertEqual(five.mode, ScoreType.FIVE_POINT)
        self.assertEqual(ten.get(), 8)
        self.assertEqual(ten.mode, ScoreType.TEN_POINT)
        self.assertEqual(ten_deci.get(), 16)
        self.assertEqual(ten_deci.mode, ScoreType.TEN_POINT_DECIMAL)
        self.assertEqual(hundred.get(), 80)
        self.assertEqual(hundred.mode, ScoreType.PERCENTAGE)

        for score in [five, ten, ten_deci, hundred]:
            for comparison in [five, ten, ten_deci, hundred]:
                for score_type in ScoreType:
                    self.assertEqual(
                        score.get(score_type),
                        comparison.get(score_type)
                    )

    def test_invalid_score(self):
        """
        Tests using an invalid score
        :return: None
        """
        for score_type, score in {
            ScoreType.THREE_POINT: 4,
            ScoreType.FIVE_POINT: -1,
            ScoreType.TEN_POINT: 100,
            ScoreType.TEN_POINT_DECIMAL: -100,
            ScoreType.PERCENTAGE: 101
        }.items():
            try:
                Score(score, score_type)
                self.fail()
            except ValueError:
                pass

    def test_score_calculation(self):
        """
        Tests calculating different score types-
        :return: None
        """
        score = Score(77, ScoreType.PERCENTAGE)
        self.assertEqual(score.get(ScoreType.TEN_POINT_DECIMAL), 15)
        self.assertEqual(score.get(ScoreType.TEN_POINT), 8)
        self.assertEqual(score.get(ScoreType.FIVE_POINT), 4)
        self.assertEqual(score.get(ScoreType.THREE_POINT), 2)

    def test_permanent_conversion(self):
        """
        Tests converting the internal score to another score type
        :return: None
        """
        score = Score(75, ScoreType.PERCENTAGE)
        score.convert(ScoreType.TEN_POINT)
        self.assertEqual(score.get(), 8)

    def test_serialization(self):
        """
        Tests serializing and deserializing an ID object
        :return: None
        """
        ob = Score(50, ScoreType.PERCENTAGE)
        self.assertEqual(
            ob.serialize(),
            {"PERCENTAGE": 50}
        )
        ob.convert(ScoreType.TEN_POINT)
        self.assertEqual(
            ob.serialize(),
            {"TEN_POINT": 5}
        )

    def test_deserialization(self):
        """
        Tests deserializing an ID object
        :return: None
        """
        self.assertEqual(
            Score.deserialize({"TEN_POINT_DECIMAL": 7}),
            Score(7, ScoreType.TEN_POINT_DECIMAL)
        )

    def test_invalid_deserialization(self):
        """
        Tests that invalid serialized data raises ValueErrors when deserialized
        :return: None
        """
        for data in [
            {"A": 1},
            {},
            {"TEN_POINT": "1"},
            {"Ten_Point": 1},
            {"TEN_POINT": -1},
            {"PERCENTAGE": 101},
            []
        ]:
            try:
                Score.deserialize(data)
                self.fail()
            except (TypeError, ValueError):
                pass

    def test_equality(self):
        """
        Tests that the equality of the objects is handled correctly
        :return: None
        """
        one = Score(59, ScoreType.PERCENTAGE)
        two = Score(59, ScoreType.PERCENTAGE)
        three = Score(6, ScoreType.TEN_POINT)
        four = Score(6, ScoreType.TEN_POINT_DECIMAL)

        self.assertEqual(one, two)
        self.assertNotEqual(two, three)
        self.assertNotEqual(two, four)
        self.assertNotEqual(three, four)

        two.convert(ScoreType.TEN_POINT)

        self.assertEqual(two, three)
        self.assertNotEqual(two, four)

        self.assertNotEqual(one, "Test")

    def test_string_representation(self):
        """
        Tests that the string representation is correct
        :return: None
        """
        score = Score(59, ScoreType.PERCENTAGE)
        representation = str(score)
        serialised = json.loads(representation)
        self.assertEqual(score, Score.deserialize(serialised))
