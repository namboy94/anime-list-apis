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

from copy import deepcopy
from typing import Dict, List, Tuple, Set, Optional
from anime_list_apis.models.Serializable import Serializable
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.Id import Id
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Title import Title
from anime_list_apis.models.attributes.Relation import Relation
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus


class AnimeData(Serializable):
    """
    Class that models user-independent anime data
    """

    def __init__(
            self,
            _id: Id,
            title: Title,
            relations: List[Relation],
            releasing_status: ReleasingStatus,
            releasing_start: Optional[Date],
            releasing_end: Optional[Date],
            episode_count: Optional[int],
            episode_duration: Optional[int],
            cover_url: Optional[str]
    ):
        """
        Initializes the Anime Data object and checks for type issues
        Some values may be None, for example if a show has not yet completed
        airing.
        :param _id: The ID of the anime
        :param title: The title of the anime
        :param relations: The relations of the anime
        :param releasing_status: The airing status of the anime
        :param releasing_start: The day the anime started airing
        :param releasing_end: The day the last episode aired
        :param episode_count: The amount of episodes of the anime
        :param episode_duration: The duration of the episodes in minutes
        :param cover_url: An URL pointing to a cover image for the anime
        :raises TypeError: If any of the parameters has a wrong type
        """
        self.ensure_type(_id, Id)
        self.ensure_type(title, Title)
        self.ensure_type(relations, list)
        list(map(lambda x: self.ensure_type(x, Relation), relations))
        self.ensure_type(releasing_status, ReleasingStatus)
        self.ensure_type(releasing_start, Date, True)
        self.ensure_type(releasing_end, Date, True)
        self.ensure_type(episode_count, int, True)
        self.ensure_type(episode_duration, int, True)
        self.ensure_type(cover_url, str, True)

        self.media_type = MediaType.ANIME
        self.id = _id
        self.title = title
        self.relations = relations
        self.releasing_status = releasing_status
        self.releasing_start = releasing_start  # type: Date
        self.releasing_end = releasing_end  # type: Date
        self.episode_count = episode_count  # type: int
        self.episode_duration = episode_duration  # type: int
        self.cover_url = cover_url  # type: str

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {
            "id": self.id.serialize(),
            "title": self.title.serialize(),
            "relations": list(map(lambda x: x.serialize(), self.relations)),
            "releasing_status": self.releasing_status.name,
            "releasing_start": self.__get_serialized(self.releasing_start),
            "releasing_end": self.__get_serialized(self.releasing_end),
            "episode_count": self.episode_count,
            "episode_duration": self.episode_duration,
            "cover_url": self.cover_url
        }

    @staticmethod
    def __get_serialized(to_serialize: Optional[Serializable]) \
            -> None or Dict[str, Optional[str or int or float or bool
                            or Dict or List or Tuple or Set]]:
        """
        Checks if a serializable object is None or not and returns either
        None or the serialized dictionary accordingly
        :param to_serialize: The object to serialize
        :return: The serialized dictionary or None if the object is None
        """
        if to_serialize is None:
            return None
        else:
            return to_serialize.serialize()

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
        data = deepcopy(data)
        # Deserialize sub-parts
        data["id"] = Id.deserialize(data["id"])
        data["title"] = Title.deserialize(data["title"])
        data["relations"] = list(map(
            lambda x: Relation.deserialize(x),
            data["relations"]
        ))
        data["releasing_status"] = ReleasingStatus[data["releasing_status"]]
        for date in ["releasing_start", "releasing_end"]:
            date_data = data[date]
            if date_data is not None:
                data[date] = Date.deserialize(date_data)

        order = [
            "id", "title", "relations", "releasing_status", "releasing_start",
            "releasing_end", "episode_count", "episode_duration", "cover_url"
        ]
        params = tuple(map(lambda x: data[x], order))
        return cls(*params)  # type: AnimeData
