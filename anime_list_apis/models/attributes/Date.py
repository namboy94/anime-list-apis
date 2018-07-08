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

from datetime import datetime
from typing import Dict, List, Tuple, Set, Optional
from anime_list_apis.models.Serializable import Serializable


class Date(Serializable):
    """
    Class that models a date consisting of a year, a month and a day
    """

    def __init__(self, year: int, month: int, day: int):
        """
        Initializes the date object. Each parameter must be filled out.
        :param year: The year
        :param month: The month
        :param day: The day
        :raises TypeError: If any of the parameters is not an integer
        :raises ValueError: If any of the parameters takes on an invalid value
        """
        self.__ensure_date_correct(year, month, day)
        self.year, self.month, self.day = year, month, day

    @classmethod
    def __ensure_date_correct(cls, year: int, month: int, day: int):
        """
        Makes sure that a date is valid. If not, exceptions are raised
        :param year: The year
        :param month: The month
        :param day: The day
        :return: None
        :raises TypeError: If any of the parameters is not an integer
        :raises ValueError: If any of the parameters takes on an invalid value
        """
        list(map(lambda x: cls.ensure_type(x, int), [year, month, day]))
        datetime(year, month, day)  # ValueError if invalid

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day
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
        year = data["year"]
        month = data["month"]
        day = data["day"]
        cls.__ensure_date_correct(year, month, day)
        generated = cls(year, month, day)  # type: Date
        return generated
