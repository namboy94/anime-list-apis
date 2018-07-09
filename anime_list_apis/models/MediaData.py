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
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.Id import Id
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Title import Title
from anime_list_apis.models.attributes.Relation import Relation
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus


# noinspection PyAbstractClass
class MediaData(MediaSerializable, CacheAble):
    """
    Class that models user-independent media data
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
        return None

    def get_model_type(self) -> CacheModelType:
        """
        Retrieves the cache model type
        :return: The model type
        """
        return CacheModelType.MEDIA_DATA

    def __init__(
            self,
            media_type: MediaType,
            _id: Id,
            title: Title,
            relations: List[Relation],
            releasing_status: ReleasingStatus,
            releasing_start: Optional[Date],
            releasing_end: Optional[Date],
            cover_url: Optional[str]
    ):
        """
        Initializes the Media Data object and checks for type issues
        Some values may be None, for example if a media has not completed
        releasing yet.
        This constructor initializes all common values of all media types.
        :param media_type: The type of media
        :param _id: The ID of the media
        :param title: The title of the media
        :param relations: The relations of the media to other media
        :param releasing_status: The releasing status of the media
        :param releasing_start: The day the media started releasing
        :param releasing_end: The day the last content was released
        :param cover_url: An URL pointing to a cover image for the anime
        :raises TypeError: If any of the parameters has a wrong type
        """
        self.ensure_type(media_type, MediaType)
        self.ensure_type(_id, Id)
        self.ensure_type(title, Title)
        self.ensure_type(relations, list)
        list(map(lambda x: self.ensure_type(x, Relation), relations))
        self.ensure_type(releasing_status, ReleasingStatus)
        self.ensure_type(releasing_start, Date, True)
        self.ensure_type(releasing_end, Date, True)
        self.ensure_type(cover_url, str, True)

        self.media_type = media_type
        self.id = _id
        self.title = title
        self.relations = relations
        self.releasing_status = releasing_status
        self.releasing_start = releasing_start
        self.releasing_end = releasing_end
        self.cover_url = cover_url

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        releasing_start = None if self.releasing_start is None \
            else self.releasing_start.serialize()
        releasing_end = None if self.releasing_end is None \
            else self.releasing_end.serialize()

        return {
            "media_type": self.media_type.name,
            "id": self.id.serialize(),
            "title": self.title.serialize(),
            "relations": list(map(lambda x: x.serialize(), self.relations)),
            "releasing_status": self.releasing_status.name,
            "releasing_start": releasing_start,
            "releasing_end": releasing_end,
            "cover_url": self.cover_url
        }

    @classmethod
    def get_class_for_media_type(cls, media_type: MediaType):
        """
        Maps a class to a media type
        :param media_type: The media type
        :return: The class mapped to that media type
        """
        return AnimeData if media_type == MediaType.ANIME else MangaData

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
            "id": Id.deserialize(data["id"]),
            "title": Title.deserialize(data["title"]),
            "relations": list(map(
                lambda x: Relation.deserialize(x),
                data["relations"]
            )),
            "releasing_status": ReleasingStatus[data["releasing_status"]],
            "cover_url": data["cover_url"]
        }

        for date in ["releasing_start", "releasing_end"]:
            date_data = data[date]
            if date_data is not None:
                deserialized[date] = Date.deserialize(date_data)
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
            "id", "title", "relations", "releasing_status", "releasing_start",
            "releasing_end", "cover_url"
        ]


class AnimeData(MediaData):
    """
    Class that models anime data
    """

    def __init__(
            self,
            _id: Id,
            title: Title,
            relations: List[Relation],
            releasing_status: ReleasingStatus,
            releasing_start: Optional[Date],
            releasing_end: Optional[Date],
            cover_url: Optional[str],
            episode_count: Optional[int],
            episode_duration: Optional[int],
    ):
        """
        Initializes the Anime Data object and checks for type issues
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
        super().__init__(
            MediaType.ANIME,
            _id,
            title,
            relations,
            releasing_status,
            releasing_start,
            releasing_end,
            cover_url
        )
        self.ensure_type(episode_count, int, True)
        self.ensure_type(episode_duration, int, True)
        self.episode_count = episode_count
        self.episode_duration = episode_duration

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        data = super()._serialize()
        data["episode_count"] = self.episode_count
        data["episode_duration"] = self.episode_duration
        return data

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
            "episode_count": data["episode_count"],
            "episode_duration": data["episode_duration"]
        }

    @classmethod
    def _get_additional_parameter_order(cls) -> List[str]:
        """
        Generates the order of class-specific additional constructor parameters
        :return: The order of the additional parameters
        """
        return ["episode_count", "episode_duration"]


class MangaData(MediaData):
    """
    Class that models manga data
    """

    def __init__(
            self,
            _id: Id,
            title: Title,
            relations: List[Relation],
            releasing_status: ReleasingStatus,
            releasing_start: Optional[Date],
            releasing_end: Optional[Date],
            cover_url: Optional[str],
            chapter_count: Optional[int],
            volume_count: Optional[int],
    ):
        """
        Initializes the Manga Data object and checks for type issues
        :param _id: The ID of the manga
        :param title: The title of the manga
        :param relations: The relations of the manga
        :param releasing_status: The releasing status of the manga
        :param releasing_start: The day the manga started releasing
        :param releasing_end: The day the last chapter/volume released
        :param chapter_count: The total amount of chapters of this manga
        :param volume_count: The total amount of volumes of this manga
        :param cover_url: An URL pointing to a cover image for the manga
        :raises TypeError: If any of the parameters has a wrong type
        """
        super().__init__(
            MediaType.MANGA,
            _id,
            title,
            relations,
            releasing_status,
            releasing_start,
            releasing_end,
            cover_url
        )
        self.ensure_type(chapter_count, int, True)
        self.ensure_type(volume_count, int, True)
        self.chapter_count = chapter_count
        self.volume_count = volume_count

    def _serialize(self) -> Dict[str, Optional[str or int or float or bool
                                 or Dict or List or Tuple or Set]]:
        """
        Serializes the object into a dictionary
        :return: The serialized form of this object
        """
        data = super()._serialize()
        data["chapter_count"] = self.chapter_count
        data["volume_count"] = self.volume_count
        return data

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
            "chapter_count": data["chapter_count"],
            "volume_count": data["volume_count"]
        }

    @classmethod
    def _get_additional_parameter_order(cls) -> List[str]:
        """
        Generates the order of class-specific additional constructor parameters
        :return: The order of the additional parameters
        """
        return ["chapter_count", "volume_count"]
