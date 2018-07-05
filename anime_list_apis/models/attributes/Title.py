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
from typing import Dict


class TitleType(Enum):
    """
    An enumeration modelling the different type of titles
    """
    ROMAJI = 1
    ENGLISH = 2
    JAPANESE = 3


class Title:
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
        :raises ValueError: In case no valid titles were provided
        """
        titles = {
            key: value for key, value in titles.items() if value is not None
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
        self.__default = default

        for title_type in TitleType:
            if title_type not in self.__titles:
                # noinspection PyTypeChecker
                self.__titles[title_type] = None

    def get(self, title_type: TitleType = None) -> str or None:
        """
        Retrieves the title in the provided title format
        :param title_type: The title type in which to retrieve the title.
                           Defaults to the current default title type
        :return: The requested title string or None if no title string for
                 the provided title exists
        """
        if title_type is None:
            return self.__titles[self.__default]
        else:
            return self.__titles[title_type]
