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
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus


class AnimeUserData(Serializable):
    """
    Models a user's entry data for an anime series
    """

    def __init__(
            self,
            username: str,
            score: Score,
            consuming_status: ConsumingStatus,
            episode_progress: int,
            consuming_start:  Optional[Date],
            consuming_end: Optional[Date]
    ):
        """
        Initializes the AnimeUserData object
        :param username: The user's username
        :param score: The user's score for this anime
        :param consuming_status: The user's current watching status
        :param episode_progress: The user's progress
        :param consuming_start: The date on which the user started watching
        :param consuming_end: The date on which the user completed the show
        :raises TypeError: If any of the parameters has a wrong type
        """
        self.ensure_type(username, str)
        self.ensure_type(score, Score)
        self.ensure_type(consuming_status, ConsumingStatus)
        self.ensure_type(episode_progress, int)
        self.ensure_type(consuming_start, Date, True)
        self.ensure_type(consuming_end, Date, True)

        self.media_type = MediaType.ANIME

        self.username = username
        self.score = score
        self.consuming_status = consuming_status
        self.episode_progress = episode_progress
        self.consuming_start = consuming_start  # type: Date
        self.consuming_end = consuming_end  # type: Date

    def is_valid_entry(self) -> bool:
        """
        Checks if the data has a valid combination of entry data
        :return: True, if all required attributes are valid and present
        """
        score_zero = self.score.get(ScoreType.PERCENTAGE) == 0
        begin_none = self.consuming_start is None
        complete_none = self.consuming_end is None

        if self.consuming_status in [
            ConsumingStatus.COMPLETED, ConsumingStatus.REPEATING
        ]:
            return not score_zero and not begin_none and not complete_none

        elif self.consuming_status in [
            ConsumingStatus.DROPPED,
            ConsumingStatus.CURRENT,
            ConsumingStatus.PAUSED
        ]:
            return not begin_none and complete_none

        else:  # self.consuming_status == WatchingStatus.PLANNING:
            return begin_none and complete_none and score_zero

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        serialized = {
            "username": self.username,
            "score": self.score.serialize(),
            "consuming_status": self.consuming_status.name,
            "episode_progress": self.episode_progress,
            "consuming_start": self.consuming_start,
            "consuming_end": self.consuming_end
        }

        for date in ["consuming_start", "consuming_end"]:
            if serialized[date] is not None:
                serialized[date] = serialized[date].serialize()

        return serialized

    @classmethod
    def _deserialize(cls, data: Dict[str, Optional[str or int or float or bool
                                     or Dict or List or Tuple or Set]]
                     ):
        """
        Deserializes a dictionary into an object of this type
        :param data: The data to deserialize
        :return: The deserialized object
        :raises TypeError: If a type error occurred
        :raises ValueError: If the data could not be deserialized
        """
        data = deepcopy(data)
        for date in ["consuming_start", "consuming_end"]:
            if data[date] is not None:
                data[date] = Date.deserialize(data[date])

        generated = cls(
            data["username"],
            Score.deserialize(data["score"]),
            ConsumingStatus[data["consuming_status"]],
            data["episode_progress"],
            data["consuming_start"],
            data["consuming_end"]
        )  # type: AnimeUserData
        return generated
