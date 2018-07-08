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


class TitleType(Enum):
    """
    An enumeration modelling the different type of titles
    """
    ROMAJI = 1
    ENGLISH = 2
    JAPANESE = 3


class Title(Serializable):
    """
    Models a title of an entry
    """

    def __init__(
            self,
            titles: Dict[TitleType, str],
            default: TitleType = TitleType.ROMAJI
    ):
        """
        Initializes the Title object.
        In case no valid titles are supplied, a ValueError is raised
        :param titles: The titles to include
        :param default: The default title to show. Defaults to ROMAJI
        :raises TypeError: If an invalid parameter type was provided
        :raises ValueError: In case no valid titles were provided
        """
        self.ensure_type(titles, dict)
        self.ensure_type(default, TitleType)
        titles = {
            key: value for key, value in titles.items()
            if self.type_check(value, str)
        }
        if len(titles) == 0:
            raise ValueError("At least one title required")

        if default not in titles:
            # noinspection PyTypeChecker
            sorted_types = list(TitleType)
            sorted_types.sort(key=lambda x: x.value, reverse=True)
            for _type in sorted_types:
                if _type in titles:
                    default = _type

        self.__titles = titles
        self.default = default

        for title_type in TitleType:
            if title_type not in self.__titles:
                # noinspection PyTypeChecker
                self.__titles[title_type] = None

    def get(self, title_type: TitleType = None) -> Optional[str]:
        """
        Retrieves the title in the provided title format
        :param title_type: The title type in which to retrieve the title.
                           Defaults to the current default title type
        :return: The requested title string or None if no title string for
                 the provided title exists
        """
        if title_type is None:
            return self.__titles[self.default]
        else:
            return self.__titles[title_type]

    def set(self, title: str, title_type: TitleType):
        """
        Sets the title of a title type
        :param title: The title string to set
        :param title_type: The type of that title
        :return: None
        :raises TypeError: If the type of the title string is wrong
        """
        self.ensure_type(title, str)
        self.__titles[title_type] = title

    def change_default_title_type(self, title_type: TitleType):
        """
        Sets the default title type
        :param title_type: The new default title type
        :return: None
        :raises ValueError: If there exists no title entry for the provided
                            title type
        """
        if self.__titles[title_type] is not None:
            self.default = title_type
        else:
            raise ValueError("Title Type has no title")

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        data = {}
        for title_type, title in self.__titles.items():
            data[title_type.name] = title
        data["default"] = self.default.name
        return data

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
        default = TitleType[data.pop("default")]
        des = {}
        for title_type, title in data.items():
            des[TitleType[title_type]] = title
        generated = cls(des, default=default)  # type: Title
        return generated
