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


class ScoreType(Enum):
    """
    Enumeration modelling the different score types
    The value of the enum specifies the maximum value a score of that
    type may be.
    For example, TEN_POINT scores may range from 0 to 10
    """
    THREE_POINT = 3
    FIVE_POINT = 5
    TEN_POINT = 10
    TEN_POINT_DECIMAL = 20
    PERCENTAGE = 100


class Score(Serializable):
    """
    Class that models a score. Allows for different score types.
    """

    def __init__(self, score: int, score_type: ScoreType):
        """
        Initializes the Score object.
        The score must be a positive number that less or equal than the
        maximum score of the score type.
        :param score: The points of the score
        :param score_type: The Type of score
        :raises TypeError: In case any of the parameter values
                           is of the wrong type
        :raises ValueError: If the score is outside the valid range
        """
        self.ensure_type(score, int)
        self.ensure_type(score_type, ScoreType)

        if score < 0 or score > score_type.value:
            raise ValueError("Invalid score")

        self.__score = score
        self.mode = score_type

    def get(self, score_type: ScoreType = None) -> int:
        """
        Retrieves the score converted to the selected score type.
        If no score type was supplied, returns the default score type's score
        :param score_type: The score type in which to retrieve the score.
                           If left as None, will result in the default score
                           type to be used
        :return: The score in the provided score type
        """
        if score_type is None:
            return self.__score
        else:
            return self.__convert(self.__score, self.mode, score_type)

    def convert(self, score_type: ScoreType):
        """
        Converts the internal score representation to another score type
        :param score_type: The score type to which to convert to
        :return: None
        """
        self.__score = self.__convert(self.__score, self.mode, score_type)
        self.mode = score_type

    # noinspection PyMethodMayBeStatic
    def __convert(self, score: int, source: ScoreType, dest: ScoreType) -> int:
        """
        Converts a score from one score type to another.
        If converting to a score type of a higher accuracy, inaccuracies
        may occur and when converting to a less accurate one,
        loss of information may occur
        :param score: The score to convert
        :param source: The source score type
        :param dest: The destination score type
        :return: The converted score value
        """
        percentage = score / source.value
        converted = percentage * dest.value
        return round(converted)

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {self.mode.name: self.__score}

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
        if len(data) != 1:
            raise ValueError("Too many score values")

        score_type, score = list(data.items())[0]

        cls.ensure_type(score, int)

        generated = cls(score, ScoreType[score_type])  # type: Score
        return generated
