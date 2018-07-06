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

from typing import Dict, List, Tuple, Set
from anime_list_apis.models.Serializable import Serializable
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.WatchingStatus import WatchingStatus


class AnimeUserData(Serializable):
    """
    Models a user's entry data for an anime series
    """

    def __init__(
            self,
            username: str,
            score: Score,
            watching_status: WatchingStatus,
            episode_progress: int,
            watching_start: Date or None,
            watching_end: Date or None
    ):
        """
        Initializes the AnimeUserData object
        :param username: The user's username
        :param score: The user's score for this anime
        :param watching_status: The user's current watching status
        :param episode_progress: The user's progress
        :param watching_start: The date on which the user started watching
        :param watching_end: The date on which the user completed the show
        :raises TypeError: If any of the parameters has a wrong type
        """
        self.ensure_type(username, str)
        self.ensure_type(score, Score)
        self.ensure_type(watching_status, WatchingStatus)
        self.ensure_type(episode_progress, int)
        self.ensure_type(watching_start, Date, True)
        self.ensure_type(watching_end, Date, True)

        self.username = username
        self.score = score
        self.watching_status = watching_status
        self.episode_progress = episode_progress
        self.watching_start = watching_start  # type: Date
        self.watching_end = watching_end  # type: Date

    def is_valid_entry(self) -> bool:
        """
        Checks if the data has a valid combination of entry data
        :return: True, if all required attributes are valid and present
        """
        score_zero = self.score.get(ScoreType.PERCENTAGE) == 0
        begin_none = self.watching_start is None
        complete_none = self.watching_end is None

        if self.watching_status in [
            WatchingStatus.COMPLETED, WatchingStatus.REWATCHING
        ]:
            return not score_zero and not begin_none and not complete_none

        elif self.watching_status in [
            WatchingStatus.DROPPED,
            WatchingStatus.WATCHING,
            WatchingStatus.PAUSED
        ]:
            return not begin_none and complete_none

        else:  # self.watching_status == WatchingStatus.PLANNING:
            return begin_none and complete_none and score_zero

    def _serialize(self) -> Dict[str, str or int or float or bool or None
                                 or Dict or List or Tuple or Set]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        serialized = {
            "username": self.username,
            "score": self.score.serialize(),
            "watching_status": self.watching_status.name,
            "episode_progress": self.episode_progress,
            "watching_start": self.watching_start,
            "watching_end": self.watching_end
        }

        for date in ["watching_start", "watching_end"]:
            if serialized[date] is not None:
                serialized[date] = serialized[date].serialize()

        return serialized

    @classmethod
    def _deserialize(cls, data: Dict[str, str or int or float or bool or None
                                     or Dict or List or Tuple or Set]):
        """
        Deserializes a dictionary into an object of this type
        :param data: The data to deserialize
        :return: The deserialized object
        :raises TypeError: If a type error occurred
        :raises ValueError: If the data could not be deserialized
        """
        for date in ["watching_start", "watching_end"]:
            if data[date] is not None:
                data[date] = Date.deserialize(data[date])

        generated = cls(
            data["username"],
            Score.deserialize(data["score"]),
            WatchingStatus[data["watching_status"]],
            data["episode_progress"],
            data["watching_start"],
            data["watching_end"]
        )  # type: AnimeUserData
        return generated
