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
from typing import List, Dict, Tuple, Optional, Any
from anime_list_apis.api.ApiInterface import ApiInterface
from anime_list_apis.models.MediaData import AnimeData
from anime_list_apis.models.MediaListEntry import AnimeListEntry
from anime_list_apis.models.MediaUserData import AnimeUserData
from anime_list_apis.models.attributes.ReleasingStatus import ReleasingStatus
from anime_list_apis.models.attributes.Date import Date
from anime_list_apis.models.attributes.Id import Id, IdType
from anime_list_apis.models.attributes.MediaType import MediaType
from anime_list_apis.models.attributes.Relation import Relation, RelationType
from anime_list_apis.models.attributes.Score import Score, ScoreType
from anime_list_apis.models.attributes.Title import Title, TitleType
from anime_list_apis.models.attributes.ConsumingStatus import ConsumingStatus


class AnilistApi(ApiInterface):
    """
    Implements a wrapper around the anilist.co API
    """

    id_type = IdType.ANILIST
    """
    The ID type of the API interface
    """

    media_query = """
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

    media_list_entry_query = """
        user {
            name
        }
        score(format: POINT_100)
        status
        progress
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
        """ + media_query + """
        }
    """
    """
    The query for a media list entry
    """

    def _get_data(
            self,
            media_type: MediaType,
            _id: int or Id
    ) -> Optional[AnimeData]:  # TODO Manga
        """
        Retrieves a single data object using the API
        :param media_type: The media type to retrieve
        :param _id: The ID to retrieve. May be either an int or an Id object
        :return: The Anime Data or None if no valid data was found
        """
        id_tuple = self.__resolve_query_id(_id, True)
        if id_tuple is None:
            return None
        query_id, id_type = id_tuple
        query_id_type = "id" if id_type == IdType.ANILIST else "idMal"

        query = """
            query ($id: Int, $type: MediaType) {
                Media(""" + query_id_type + """: $id, type: $type) {
                    """ + self.media_query + """
                }
            }
        """

        variables = {"id": query_id, "type": media_type.name}
        data = self.__graphql_query(query, variables)

        if data is None:
            return None
        else:
            return self.__generate_anime_data(data["Media"])

    def get_list_entry(
            self,
            media_type: MediaType,
            _id: int or Id,
            username: str
    ) -> Optional[AnimeListEntry]:  # TODO Manga
        """
        Retrieves a user list entry
        :param media_type: The media type to fetch
        :param _id: The ID to retrieve. May be and int or an Id object
        :param username: The user for which to fetch the entry
        :return: The entry for the user or
                 None if the user doesn't have such an entry
        """
        id_tuple = self.__resolve_query_id(_id, False)
        if id_tuple is None:
            return None
        query_id = id_tuple[0]

        query = """
            query ($id: Int, $username: String, $type: MediaType) {
                MediaList(mediaId: $id, userName: $username, type: $type) {
                    """ + self.media_list_entry_query + """
                }
            }
        """
        variables = {"id": query_id, "type": media_type.name}
        result = self.__graphql_query(query, variables)

        if result is None:
            return None
        else:
            anime_data = \
                self.__generate_anime_data(result["MediaList"]["media"])
            user_data = self.__generate_anime_user_data(result["MediaList"])
            return AnimeListEntry(anime_data, user_data)

    def get_list(self, media_type: MediaType, username: str) \
            -> List[AnimeListEntry]:  # TODO Manga
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
                            """ + self.media_list_entry_query + """
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
            for collection in result["MediaListCollection"]["lists"]:
                for entry in collection["entries"]:
                    anime_data = self.__generate_anime_data(entry["media"])
                    user_data = self.__generate_anime_user_data(entry)
                    entries.append(AnimeListEntry(anime_data, user_data))
            return entries

    def get_anilist_id_from_mal_id(self, mal_id: int) -> Optional[int]:
        """
        Retrieves an anilist ID from a myanimelist ID
        :param mal_id: The myanimelist ID
        :return: The anilist ID. May be None if myanimelist ID has no
                 equivalent on anilist
        """
        query = """
            query ($mal_id: Int) {
                Media(idMal: $mal_id) {
                    id
                }
            }
        """
        variables = {"mal_id": mal_id}
        result = self.__graphql_query(query, variables)
        if result is None:
            return None
        else:
            return result["Media"]["id"]

    def __generate_anime_user_data(self, data: Dict[str, Any]):
        """
        Generates an Anime User Data object from JSON data
        :param data: The data to parse as User Data
        :return: The generated AnimeUserData object
        """
        watching_status = data["status"]

        return AnimeUserData(
            data["user"]["name"],
            Score(data["score"], ScoreType.PERCENTAGE),
            ConsumingStatus[watching_status],
            data["progress"],
            self.__resolve_date(data["startedAt"]),
            self.__resolve_date(data["completedAt"])
        )

    # noinspection PyTypeChecker
    def __generate_anime_data(self, data: Dict[str, Any]) -> AnimeData:
        """
        Generates an AnimeData object from a GraphQL result
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
        relations = []
        for relation in data["relations"]["edges"]:
            dest_id = Id({
                IdType.ANILIST: relation["node"]["id"],
                IdType.MYANIMELIST: relation["node"]["idMal"]
            })
            rel_type = RelationType[relation["relationType"]]
            relations.append(Relation(_id, dest_id, rel_type))

        airing_status = data["status"]
        if airing_status == "NOT_YET_RELEASED":
            airing_status = "NOT_RELEASED"
        airing_status = ReleasingStatus[airing_status]

        return AnimeData(
            _id,
            title,
            relations,
            airing_status,
            self.__resolve_date(data["startDate"]),
            self.__resolve_date(data["endDate"]),
            data["episodes"],
            data["duration"],
            data["coverImage"]["large"]
        )

    @staticmethod
    def __graphql_query(query: str, variables: Dict[str, Any]) \
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
        time.sleep(0.5)  # For rate limiting
        result = json.loads(response.text)

        if "errors" in result:
            return None
        else:
            return result["data"]

    @staticmethod
    def __resolve_date(date_data: Dict[str, int]) -> Optional[Date]:
        """
        Resolves a date dictionary into either a Date object or None
        :param date_data: The date data to use
        :return: The generated Date object or None if invalid date
        """
        try:
            return Date(
                date_data["year"],
                date_data["month"],
                date_data["day"]
            )
        except (ValueError, TypeError):
            return None

    def __resolve_query_id(self, _id: int or Id, allow_mal: bool) \
            -> Optional[Tuple[int, IdType]]:
        """
        Calculates the ID value to use in a query
        :param _id: The ID, which may be an Id object or an int value
        :param allow_mal: If True, may return a Myanimelist ID.
                          This will be signified by the second return value
                          being IdType.MYANIMELIST
        :return: A tuple consisting of the ID and the IDs type
        """
        if not isinstance(_id, int):
            mal_id = _id.get(IdType.MYANIMELIST)
            anilist_id = _id.get(IdType.ANILIST)
        else:
            mal_id = None
            anilist_id = _id

        id_type = IdType.ANILIST
        if anilist_id is None:
            query_id = mal_id

            if allow_mal:
                id_type = IdType.MYANIMELIST
            else:
                query_id = self.get_anilist_id_from_mal_id(query_id)

        else:
            query_id = anilist_id

        if query_id is None:
            return None
        else:
            return query_id, id_type
