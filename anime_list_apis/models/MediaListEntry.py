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

from anime_list_apis.models.CacheAble import CacheAble, CacheModelType
from anime_list_apis.models.Serializable import MediaSerializable
from anime_list_apis.models.attributes.Id import Id
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Score import ScoreType
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus
from anime_list_apis.models.MediaData import \
    AnimeData, MangaData, MediaData
from anime_list_apis.models.MediaUserData import \
    AnimeUserData, MangaUserData, MediaUserData


class MediaListEntry(MediaSerializable, CacheAble):
    """
    Class that models a user's media list entry
    """

    def get_id(self) -> Id:
        """
        Retrieves the cache entry's ID
        :return: The ID
        """
        return self.id

    def get_media_type(self) -> MediaType:
        """
        Retrieves the media type
        :return: The media type
        """
        return self.media_type

    def get_username(self) -> Optional[str]:
        """
        Retrieves the username, if applicable. Else None
        :return: The username or None if not applicable
        """
        return self.username

    def get_model_type(self) -> CacheModelType:
        """
        Retrieves the cache model type
        :return: The model type
        """
        return CacheModelType.MEDIA_LIST_ENTRY

    def __init__(self, media_type: MediaType,
                 media_data: MediaData, user_data: MediaUserData):
        """
        Initializes the media list entry.
        :param media_data: The media data
        :param user_data: The user data
        :raises TypeError: If any of the parameters has a wrong type
        :raises ValueError: If the media and user data do not match
        """
        self.ensure_type(media_data,
                         MediaData.get_class_for_media_type(media_type))
        self.ensure_type(user_data,
                         MediaUserData.get_class_for_media_type(media_type))

        if media_data.id != user_data.id \
                or media_data.media_type != user_data.media_type \
                or media_type != media_data.media_type:
            raise ValueError("Mismatching User and Media Data")

        self.media_type = media_type
        self.id = media_data.id
        self.title = media_data.title
        self.relations = media_data.relations
        self.releasing_status = media_data.releasing_status
        self.releasing_start = media_data.releasing_start
        self.releasing_end = media_data.releasing_end
        self.cover_url = media_data.cover_url

        self.username = user_data.username
        self.score = user_data.score
        self.consuming_status = user_data.consuming_status
        self.consuming_start = user_data.consuming_start
        self.consuming_end = user_data.consuming_end

        self.__media_data_cls = type(media_data)
        self.__user_data_cls = type(user_data)

    def get_media_data(self) -> MediaData:
        """
        Generates a new MediaData object from the internal representation
        :return: The generated MediaData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        raise NotImplementedError()  # pragma: no cover

    def get_user_data(self) -> MediaUserData:
        """
        Generates a new MediaUserData object from the internal representation
        :return: The generated MediaUserData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        raise NotImplementedError()  # pragma: no cover

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

    @classmethod
    def get_class_for_media_type(cls, media_type: MediaType):
        """
        Maps a class to a media type
        :param media_type: The media type
        :return: The class mapped to that media type
        """
        return AnimeListEntry \
            if media_type == MediaType.ANIME \
            else MangaListEntry

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        return {
            "media_type": self.media_type.name,
            "media_data": self.get_media_data().serialize(),
            "user_data": self.get_user_data().serialize()
        }

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
            "media_data": MediaData.deserialize(data["media_data"]),
            "user_data": MediaUserData.deserialize(data["user_data"])
        }
        return deserialized

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
        return {}

    @classmethod
    def _get_common_parameter_order(cls) -> List[str]:
        """
        Generates an order of constructor parameters for the common attributes
        used for media classes
        :return: The order of common parameters
        """
        return ["media_data", "user_data"]

    @classmethod
    def _get_additional_parameter_order(cls) -> List[str]:
        """
        Generates the order of class-specific additional constructor parameters
        :return: The order of the additional parameters
        """
        return []


class AnimeListEntry(MediaListEntry):
    """
    Class that models a user's anime list entry
    """

    def __init__(self, anime_data: AnimeData, user_data: AnimeUserData):
        """
        Initializes the anime list entry.
        :param anime_data: The anime data
        :param user_data: The user data
        :raises TypeError: If any of the parameters has a wrong type
        """
        super().__init__(MediaType.ANIME, anime_data, user_data)
        self.episode_count = anime_data.episode_count
        self.episode_duration = anime_data.episode_duration
        self.episode_progress = user_data.episode_progress

    def get_media_data(self) -> AnimeData:
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
            self.cover_url,
            self.episode_count,
            self.episode_duration
        )

    def get_user_data(self) -> AnimeUserData:
        """
        Generates a new AnimeUserData object from the internal representation
        :return: The generated AnimeUserData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        return AnimeUserData(
            self.id,
            self.username,
            self.score,
            self.consuming_status,
            self.consuming_start,
            self.consuming_end,
            self.episode_progress
        )


class MangaListEntry(MediaListEntry):
    """
    Class that models a user's manga list entry
    """

    def __init__(self, manga_data: MangaData, user_data: MangaUserData):
        """
        Initializes the manga list entry.
        :param manga_data: The manga data
        :param user_data: The user data
        :raises TypeError: If any of the parameters has a wrong type
        """
        super().__init__(MediaType.MANGA, manga_data, user_data)
        self.chapter_count = manga_data.chapter_count
        self.volume_count = manga_data.volume_count
        self.chapter_progress = user_data.chapter_progress
        self.volume_progress = user_data.volume_progress

    def get_media_data(self) -> MangaData:
        """
        Generates a new MangaData object from the internal representation
        :return: The generated MangaData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        return MangaData(
            self.id,
            self.title,
            self.relations,
            self.releasing_status,
            self.releasing_start,
            self.releasing_end,
            self.cover_url,
            self.chapter_count,
            self.volume_count
        )

    def get_user_data(self) -> MangaUserData:
        """
        Generates a new MangaUserData object from the internal representation
        :return: The generated MangaUserData object
        :raises TypeError: If any of the internal parameters has a wrong type
        """
        return MangaUserData(
            self.id,
            self.username,
            self.score,
            self.consuming_status,
            self.consuming_start,
            self.consuming_end,
            self.chapter_progress,
            self.volume_progress
        )
