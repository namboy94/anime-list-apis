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

from typing import Dict, List, Tuple, Set, Optional
from anime_list_apis.models.MediaData import AnimeData
from anime_list_apis.models.MediaUserData import AnimeUserData
from anime_list_apis.models.Serializable import Serializable
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Score import ScoreType
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus


class AnimeListEntry(Serializable):

    def __init__(self, anime_data: AnimeData, user_data: AnimeUserData):
        """
        Initializes the anime list entry.
        By subclassing both AnimeData and AnimeUserData, it's possible to
        access all of their attributes
        :param anime_data: The anime data
        :param user_data: The user data
        :raises TypeError: If any of the parameters has a wrong type
        """
        self.ensure_type(anime_data, AnimeData)
        self.ensure_type(user_data, AnimeUserData)

        self.media_type = MediaType.ANIME

        self.id = anime_data.id
        self.title = anime_data.title
        self.relations = anime_data.relations
        self.releasing_status = anime_data.releasing_status
        self.releasing_start = anime_data.releasing_start
        self.releasing_end = anime_data.releasing_end
        self.episode_count = anime_data.episode_count
        self.episode_duration = anime_data.episode_duration
        self.cover_url = anime_data.cover_url

        self.username = user_data.username
        self.score = user_data.score
        self.consuming_status = user_data.consuming_status
        self.episode_progress = user_data.episode_progress
        self.consuming_start = user_data.consuming_start
        self.consuming_end = user_data.consuming_end

    def get_anime_data(self) -> AnimeData:
        """
        Generates a new AnimeData object from the internal representation
        :return: The generated AnimeData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        return AnimeData(
            self.id,
            self.title,
            self.relations,
            self.releasing_status,
            self.releasing_start,
            self.releasing_end,
            self.episode_count,
            self.episode_duration,
            self.cover_url
        )

    def get_user_data(self) -> AnimeUserData:
        """
        Generates a new AnimeUserData object from the internal representation
        :return: The generated AnimeUserData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        return AnimeUserData(
            self.username,
            self.score,
            self.consuming_status,
            self.episode_progress,
            self.consuming_start,
            self.consuming_end
        )

    def is_valid_entry(self) -> bool:
        """
        Checks if the data has a valid combination of entry data
        :return: True, if all required attributes are valid and present
        """
        score_zero = self.score.get(ScoreType.PERCENTAGE) == 0
        begin_none = self.consuming_start is None
        complete_none = self.consuming_end is None
        consuming_complete = self.consuming_status == ConsumingStatus.COMPLETED
        started_watching = self.consuming_status in [
            ConsumingStatus.CURRENT,
            ConsumingStatus.PAUSED,
            ConsumingStatus.DROPPED
        ]

        if not self.get_user_data().is_valid_entry():
            return False

        if self.releasing_status in [
            ReleasingStatus.FINISHED
        ]:
            return True

        elif self.releasing_status in [
            ReleasingStatus.RELEASING, ReleasingStatus.CANCELLED,
        ]:
            return complete_none and score_zero and not consuming_complete

        else:  # AiringStatus.NOT_RELEASESD
            return begin_none and complete_none and score_zero \
                   and not consuming_complete and not started_watching

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {
            "anime_data": self.get_anime_data().serialize(),
            "user_data": self.get_user_data().serialize()
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
        generated = cls(
            AnimeData.deserialize(data["anime_data"]),
            AnimeUserData.deserialize(data["user_data"])
        )  # type: AnimeListEntry
        return generated
