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

from unittest import TestCase
from anime_list_apis.models.attributes.Score import Score, ScoreType


class TestScore(TestCase):
    """
    Test the Score Attribute class
    """

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

        self.assertEqual(three.score, 3)
        self.assertEqual(three.mode, ScoreType.THREE_POINT)
        self.assertEqual(three.score, 4)
        self.assertEqual(three.mode, ScoreType.FIVE_POINT)
        self.assertEqual(three.score, 8)
        self.assertEqual(three.mode, ScoreType.TEN_POINT)
        self.assertEqual(three.score, 16)
        self.assertEqual(three.mode, ScoreType.TEN_POINT_DECIMAL)
        self.assertEqual(three.score, 80)
        self.assertEqual(three.mode, ScoreType.PERCENTAGE)

        for score in [five, ten, ten_deci, hundred]:
            for comparison in [five, ten, ten_deci, hundred]:
                for score_type in ScoreType:
                    self.assertEqual(
                        score.get(score_type),
                        comparison.get(score_type)
                    )

    def test_score_calculation(self):
        """
        Tests calculating different score types
        :return: None
        """
        score = Score(77, ScoreType.PERCENTAGE)
        self.assertEqual(score.get(ScoreType.TEN_POINT_DECIMAL), 15)
        self.assertEqual(score.get(ScoreType.TEN_POINT), 8)
        self.assertEqual(score.get(ScoreType.FIVE_POINT), 4)
        self.assertEqual(score.get(ScoreType.THREE_POINT), 2)
