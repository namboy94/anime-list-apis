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

import time
import json
import requests
import logging
from typing import List, Dict, Tuple, Optional, Any
from anime_list_apis.cache.Cache import Cache
from anime_list_apis.api.ApiInterface import ApiInterface
from anime_list_apis.models.MediaData import MediaData
from anime_list_apis.models.MediaListEntry import MediaListEntry
from anime_list_apis.models.MediaUserData import MediaUserData
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Title import Title, TitleType


class AnilistApi(ApiInterface):
    """
    Implements a wrapper around the anilist.co API
    """

    def __init__(self, cache: Cache = None, rate_limit_pause: float = 0.5):
        """
        Initializes the Anilist Api interface.
        Intializes cache or uses the one provided.
        :param cache: The cache to use. If left as None, will use default cache
        :param rate_limit_pause: A duration in seconds that the API Interface
                                 will pause after a network operation to
                                 prevent being rate limited
        """
        super().__init__(IdType.ANILIST, cache, rate_limit_pause)

    # Implemented Abstract Methods --------------------------------------------

    def _get_data(
            self,
            media_type: MediaType,
            _id: Id
    ) -> Optional[MediaData]:
        """
        Retrieves a single data object using the API
        :param media_type: The media type to retrieve
        :param _id: The ID to retrieve. May be either an int or an Id object
        :return: The Anime Data or None if no valid data was found
        """
        id_tuple = self.__resolve_query_id(media_type, _id, True)
        if id_tuple is None:
            return None
        query_id, id_type = id_tuple
        query_id_type = "id" if id_type == IdType.ANILIST else "idMal"

        query = """
            query ($id: Int, $type: MediaType) {
                Media(""" + query_id_type + """: $id, type: $type) {
                    """ + self.__media_query + """
                }
            }
        """

        variables = {"id": query_id, "type": media_type.name}
        data = self.__graphql_query(query, variables)

        if data is None:
            return None
        else:
            data = self.__generate_media_data(media_type, data["Media"])
            self.__cache_mal_to_anilist_map(
                media_type,
                data.id.get(IdType.MYANIMELIST),
                data.id.get(IdType.ANILIST)
            )
            return data

    def _get_user_data(
            self,
            media_type: MediaType,
            _id: Id,
            username: str
    ) -> Optional[MediaUserData]:
        """
        Actual implementation of the get_user_data for each subclass
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve
        :param username: The user for which to fetch the data
        :return: The user data for the entry or
                 None if the user doesn't have such an entry
        """
        entry = self._get_list_entry(media_type, _id, username)
        if entry is not None:
            return entry.get_user_data()
        else:
            return None

    def _get_user_data_list(self, media_type: MediaType, username: str) \
            -> List[MediaUserData]:
        """
        Retrieves a user's entire list of user data
        Actual implementation method to be implemented by subclasses
        :param media_type: The media type to fetch
        :param username: The username for which to fetch the list
        :return: The list of user data
        """
        return list(map(
            lambda x: x.get_user_data(),
            self._get_list(media_type, username)
        ))

    def _get_list_entry(
            self,
            media_type: MediaType,
            _id: int or Id,
            username: str
    ) -> Optional[MediaListEntry]:
        """
        Retrieves a user list entry
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve. May be and int or an Id object
        :param username: The user for which to fetch the entry
        :return: The entry for the user or
                 None if the user doesn't have such an entry
        """
        id_tuple = self.__resolve_query_id(media_type, _id, False)
        if id_tuple is None:
            return None
        query_id = id_tuple[0]

        # Currently we can't get all the information in one go due to some
        # 500 internal server errors.
        # Once this is fixed, the following should stand here:
        # inject = self.media_list_entry_query
        inject = self.__media_list_entry_query.replace(
            self.__media_query,
            """
            id
            idMal
            """
        )

        query = """
            query ($id: Int, $username: String, $type: MediaType) {
                MediaList(mediaId: $id, userName: $username, type: $type) {
                    """ + inject + """
                }
            }
        """
        variables = {
            "id": query_id,
            "type": media_type.name,
            "username": username
        }
        result = self.__graphql_query(query, variables)

        if result is None:
            return None
        else:

            # Again, due to 500 Server errors we have to hack around a bit
            # media_data = self.__generate_media_data(
            #     media_type, result["MediaList"]["media"]
            # )
            media_data = self._get_data(media_type, _id)

            user_data = self.__generate_media_user_data(
                media_type, result["MediaList"]
            )
            entry_cls = MediaListEntry.get_class_for_media_type(media_type)
            return entry_cls(media_data, user_data)

    def _get_list(self, media_type: MediaType, username: str) \
            -> List[MediaListEntry]:
        """
        Retrieves a user's entire list
        :param media_type: The media type to fetch
        :param username: The username for which to fetch the list
        :return: The list of List entries
        """
        query = """
            query($username: String, $type: MediaType) {
                MediaListCollection (userName: $username, type: $type) {
                    lists {
                        entries {
                            """ + self.__media_list_entry_query + """
                        }
                    }
                }
            }
        """
        variables = {"username": username, "type": media_type.name}
        result = self.__graphql_query(query, variables)

        if result is None:
            return []
        else:

            entries = []
            entry_cls = MediaListEntry.get_class_for_media_type(media_type)

            for collection in result["MediaListCollection"]["lists"]:
                for entry in collection["entries"]:
                    media_data = self.__generate_media_data(
                        media_type,
                        entry["media"]
                    )
                    user_data = self.__generate_media_user_data(
                        media_type,
                        entry
                    )

                    self.__cache_mal_to_anilist_map(
                        media_type,
                        media_data.id.get(IdType.MYANIMELIST),
                        media_data.id.get(IdType.ANILIST)
                    )

                    entries.append(entry_cls(media_data, user_data))
            return entries

    # Useful public methods ---------------------------------------------------

    def get_anilist_id_from_mal_id(
            self,
            media_type: MediaType,
            mal_id: int
    ) -> Optional[int]:
        """
        Retrieves an anilist ID from a myanimelist ID
        :param media_type: The media type of the myanimelist ID
        :param mal_id: The myanimelist ID
        :return: The anilist ID. May be None if myanimelist ID has no
                 equivalent on anilist
        """
        cached = self.cache.get_primitive(
            self.id_type, "mal-" + media_type.name + "-" + str(mal_id)
        )
        if cached is not None:
            return cached

        query = """
            query ($mal_id: Int, $type: MediaType) {
                Media(idMal: $mal_id, type: $type) {
                    id
                }
            }
        """
        if mal_id is None:
            return None
        variables = {"mal_id": mal_id, "type": media_type.name}
        result = self.__graphql_query(query, variables)
        if result is None:
            return None
        else:
            anilist_id = result["Media"]["id"]
            self.__cache_mal_to_anilist_map(media_type, mal_id, anilist_id)
            return anilist_id

    # Helper Methods ----------------------------------------------------------

    @staticmethod
    def __generate_media_user_data(media_type: MediaType,
                                   data: Dict[str, Any]) -> MediaUserData:
        """
        Generates an Media User Data object from JSON data
        :param media_type: The media type to generate
        :param data: The data to parse as User Data
        :return: The generated MediaUserData object
        """
        _id = Id({
            IdType.ANILIST: data["media"]["id"],
            IdType.MYANIMELIST: data["media"]["idMal"]
        })

        serialized = {
            "media_id": _id.serialize(),
            "media_type": media_type.name,
            "username": data["user"]["name"],
            "score": Score(data["score"], ScoreType.PERCENTAGE).serialize(),
            "consuming_status": data["status"],
            "episode_progress": data["progress"],
            "chapter_progress": data["progress"],
            "volume_progress": data["progressVolumes"]
        }

        for api_key, dict_key in {
            "startedAt": "consuming_start",
            "completedAt": "consuming_end"
        }.items():
            try:
                serialized[dict_key] = Date(
                    data[api_key]["year"],
                    data[api_key]["month"],
                    data[api_key]["day"]
                ).serialize()
            except (TypeError, ValueError):
                serialized[dict_key] = None

        return MediaUserData.deserialize(serialized)

    # noinspection PyTypeChecker
    @staticmethod
    def __generate_media_data(media_type: MediaType,
                              data: Dict[str, Any]) -> MediaData:
        """
        Generates an MediaData object from a GraphQL result
        :param media_type: The media type to generate
        :param data: The data to convert into an AnimeData object
        :return: The generated AnimeData object
        """
        _id = Id({
            IdType.ANILIST: data["id"],
            IdType.MYANIMELIST: data["idMal"]
        })

        title = Title({
            TitleType.ROMAJI: data["title"]["romaji"],
            TitleType.ENGLISH: data["title"]["english"],
            TitleType.JAPANESE: data["title"]["native"],
        })
        if title.get(TitleType.ENGLISH) is None:
            title.set(title.get(TitleType.ROMAJI), TitleType.ENGLISH)

        relations = []
        for relation in data["relations"]["edges"]:
            dest_id = Id({
                IdType.ANILIST: relation["node"]["id"],
                IdType.MYANIMELIST: relation["node"]["idMal"]
            })
            dest_media_type = media_type
            rel_type = RelationType[relation["relationType"]]

            if rel_type == RelationType.ADAPTATION:
                if media_type == MediaType.ANIME:
                    dest_media_type = MediaType.MANGA
                else:
                    dest_media_type = MediaType.ANIME

            relations.append(Relation(
                _id, media_type, dest_id, dest_media_type, rel_type
            ).serialize())

        releasing_status = \
            data["status"].replace("NOT_YET_RELEASED", "NOT_RELEASED")

        serialized = {
            "media_type": media_type.name,
            "id": _id.serialize(),
            "title": title.serialize(),
            "relations": relations,
            "releasing_status": releasing_status,
            "cover_url": data["coverImage"]["large"],
            "episode_count": data["episodes"],
            "episode_duration": data["duration"],
            "chapter_count": data["episodes"],
            "volume_count": data["episodes"]
        }

        for api_key, dict_key in {
            "startDate": "releasing_start",
            "endDate": "releasing_end"
        }.items():
            try:
                serialized[dict_key] = Date(
                    data[api_key]["year"],
                    data[api_key]["month"],
                    data[api_key]["day"]
                ).serialize()
            except (TypeError, ValueError):
                serialized[dict_key] = None

        return MediaData.deserialize(serialized)

    def __graphql_query(self, query: str, variables: Dict[str, Any]) \
            -> Optional[Dict[str, Any]]:
        """
        Executes a GraphQL query on the anilist API
        :param query: The query string
        :param variables: The variables to post
        :return: The result of the query or None if an error occured
        """
        url = 'https://graphql.anilist.co'
        response = requests.post(
            url, json={'query': query, 'variables': variables}
        )
        time.sleep(self.rate_limit_pause)  # For rate limiting
        result = json.loads(response.text)

        if "errors" in result:
            if result["errors"][0]["message"] == \
                    "Too Many Requests.":  # pragma: no cover
                logging.getLogger(__name__).warning(
                    "Rate limited on anilist. "
                    "Waiting for 70 seconds before retrying"
                )
                time.sleep(70)
                return self.__graphql_query(query, variables)
            else:
                return None
        else:
            return result["data"]

    def __resolve_query_id(self, media_type: MediaType, _id: Id,
                           allow_mal: bool) -> Optional[Tuple[int, IdType]]:
        """
        Calculates the ID value to use in a query
        :param media_type: The media type of the ID
        :param _id: The ID
        :param allow_mal: If True, may return a Myanimelist ID.
                          This will be signified by the second return value
                          being IdType.MYANIMELIST
        :return: A tuple consisting of the ID and the IDs type
        """
        mal_id = _id.get(IdType.MYANIMELIST)
        anilist_id = _id.get(IdType.ANILIST)

        id_type = IdType.ANILIST
        if anilist_id is None:
            query_id = mal_id

            if allow_mal:
                id_type = IdType.MYANIMELIST
            else:
                query_id = self.get_anilist_id_from_mal_id(
                    media_type, query_id
                )

        else:
            query_id = anilist_id

        if query_id is None:
            return None
        else:
            return query_id, id_type

    def __cache_mal_to_anilist_map(
            self,
            media_type: MediaType,
            mal_id: int,
            anilist_id: int
    ):
        """
        Caches an anilist ID mapped to a myanimelist ID
        :param media_type: The media type to map
        :param mal_id: The myanimelist ID to map
        :param anilist_id: The anilist ID to map
        :return: None
        """
        self.cache.add_primitive(
            self.id_type,
            "mal-" + media_type.name + "-" + str(mal_id),
            anilist_id
        )

    # Query definitions -------------------------------------------------------

    __media_query = """
            id
            idMal
            title {
                romaji
                english
                native
            }
            status
            episodes
            duration
            coverImage {
                large
            }
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            relations {
                edges {
                    node {
                        id
                        idMal
                    }
                    relationType
                }
            }
        """
    """
    The GraphQL query for a Media object
    """

    __media_list_entry_query = """
            user {
                name
            }
            score(format: POINT_100)
            status
            progress
            progressVolumes
            startedAt {
                year
                month
                day
            }
            completedAt {
                year
                month
                day
            }
            media {
            """ + __media_query + """
            }
        """
    """
    The query for a media list entry
    """
