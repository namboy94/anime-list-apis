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
from anime_list_apis.models.Serializable import MediaSerializable
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus


# noinspection PyAbstractClass
class MediaUserData(MediaSerializable):
    """
    Models a user's entry data for an anime series
    """

    def __init__(
            self,
            media_type: MediaType,
            username: str,
            score: Score,
            consuming_status: ConsumingStatus,
            consuming_start:  Optional[Date],
            consuming_end: Optional[Date]
    ):
        """
        Initializes the MediaUserData object
        :param media_type: The type of media represented
        :param username: The user's username
        :param score: The user's score for this entry
        :param consuming_status: The user's current consuming status
        :param consuming_start: The date on which the user started consuming
        :param consuming_end: The date on which the user completed the entry
        :raises TypeError: If any of the parameters has a wrong type
        """
        self.ensure_type(media_type, MediaType)
        self.ensure_type(username, str)
        self.ensure_type(score, Score)
        self.ensure_type(consuming_status, ConsumingStatus)
        self.ensure_type(consuming_start, Date, True)
        self.ensure_type(consuming_end, Date, True)

        self.media_type = media_type
        self.username = username
        self.score = score
        self.consuming_status = consuming_status
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
            "media_type": self.media_type.name,
            "username": self.username,
            "score": self.score.serialize(),
            "consuming_status": self.consuming_status.name,
            "consuming_start": self.consuming_start,
            "consuming_end": self.consuming_end
        }

        for date in ["consuming_start", "consuming_end"]:
            if serialized[date] is not None:
                serialized[date] = serialized[date].serialize()

        return serialized

    @classmethod
    def get_class_for_media_type(cls, media_type: MediaType):
        """
        Maps a class to a media type
        :param media_type: The media type
        :return: The class mapped to that media type
        """
        return AnimeUserData \
            if media_type == MediaType.ANIME \
            else MangaUserData

    @classmethod
    def _get_common_deserialized_components(
            cls,
            data: Dict[str, Optional[str or int or float or bool or
                                     Dict or List or Tuple or Set]]) \
            -> Dict[str, Optional[str or int or float or bool or
                                  Dict or List or Tuple or Set]]:
        """
        Deserializes the common child components of the data dictionary
        :param data: The data to deserialize
        :return: The deserialized dictionary
        """
        deserialized = {
            "media_type": MediaType[data["media_type"]],
            "username": data["username"],
            "score": Score.deserialize(data["score"]),
            "consuming_status": ConsumingStatus[data["consuming_status"]]
        }

        for date in ["consuming_start", "consuming_end"]:
            if data[date] is not None:
                deserialized[date] = Date.deserialize(data[date])
            else:
                deserialized[date] = None

        return deserialized

    @classmethod
    def _get_common_parameter_order(cls) -> List[str]:
        """
        Generates an order of constructor parameters for the common attributes
        used for media classes
        :return: The order of common parameters
        """
        return [
            "username", "score",
            "consuming_status", "consuming_start", "consuming_end"
        ]


class AnimeUserData(MediaUserData):
    """
    Models a user's entry data for an anime series
    """

    def __init__(
            self,
            username: str,
            score: Score,
            consuming_status: ConsumingStatus,
            consuming_start:  Optional[Date],
            consuming_end: Optional[Date],
            episode_progress: int
    ):
        """
        Initializes the AnimeUserData object
        :param username: The user's username
        :param score: The user's score for this anime
        :param consuming_status: The user's current watching status
        :param consuming_start: The date on which the user started watching
        :param consuming_end: The date on which the user completed the show
        :param episode_progress: The user's progress
        :raises TypeError: If any of the parameters has a wrong type
        """
        super().__init__(
            MediaType.ANIME,
            username,
            score,
            consuming_status,
            consuming_start,
            consuming_end
        )
        self.ensure_type(episode_progress, int)
        self.episode_progress = episode_progress

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        serialized = super()._serialize()
        serialized["episode_progress"] = self.episode_progress
        return serialized

    @classmethod
    def _get_specific_deserialized_components(
            cls,
            data: Dict[str, Optional[str or int or float or bool or
                                     Dict or List or Tuple or Set]]) \
            -> Dict[str, Optional[str or int or float or bool or
                                  Dict or List or Tuple or Set]]:
        """
        Deserializes class-specific child components of the data dictionary
        :param data: The data to deserialize
        :return: The deserialized dictionary
        """
        return {
            "episode_progress": data["episode_progress"]
        }

    @classmethod
    def _get_additional_parameter_order(cls) -> List[str]:
        """
        Generates the order of class-specific additional constructor parameters
        :return: The order of the additional parameters
        """
        return ["episode_progress"]


class MangaUserData(MediaUserData):
    """
    Models a user's entry data for a manga series
    """

    def __init__(
            self,
            username: str,
            score: Score,
            consuming_status: ConsumingStatus,
            consuming_start: Optional[Date],
            consuming_end: Optional[Date],
            chapter_progress: int,
            volume_progress: int
    ):
        """
        Initializes the MangaUserData object
        :param username: The user's username
        :param score: The user's score for this manga
        :param consuming_status: The user's current reading status
        :param consuming_start: The date on which the user started reading
        :param consuming_end: The date on which the user completed the series
        :param chapter_progress: The user's chapter progress
        :param volume_progress: The user's volume progress
        :raises TypeError: If any of the parameters has a wrong type
        """
        super().__init__(
            MediaType.MANGA,
            username,
            score,
            consuming_status,
            consuming_start,
            consuming_end
        )
        self.ensure_type(chapter_progress, int)
        self.ensure_type(volume_progress, int)
        self.chapter_progress = chapter_progress
        self.volume_progress = volume_progress

    def _serialize(self) -> Dict[str,
                                 Optional[str or int or float or bool
                                          or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        serialized = super()._serialize()
        serialized["chapter_progress"] = self.chapter_progress
        serialized["volume_progress"] = self.volume_progress
        return serialized

    @classmethod
    def _get_specific_deserialized_components(
            cls,
            data: Dict[str, Optional[str or int or float or bool or
                                     Dict or List or Tuple or Set]]) \
            -> Dict[str, Optional[str or int or float or bool or
                                  Dict or List or Tuple or Set]]:
        """
        Deserializes class-specific child components of the data dictionary
        :param data: The data to deserialize
        :return: The deserialized dictionary
        """
        return {
            "chapter_progress": data["chapter_progress"],
            "volume_progress": data["volume_progress"]
        }

    @classmethod
    def _get_additional_parameter_order(cls) -> List[str]:
        """
        Generates the order of class-specific additional constructor parameters
        :return: The order of the additional parameters
        """
        return ["chapter_progress", "volume_progress"]
