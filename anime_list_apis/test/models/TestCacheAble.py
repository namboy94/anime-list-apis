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

from unittest import TestCase

from anime_list_apis.models.CacheAble import CacheAble
from anime_list_apis.test.models.TestMediaData import TestMediaData
from anime_list_apis.test.models.TestMediaListEntry import TestMediaListEntry
from anime_list_apis.test.models.TestMediaUserData import TestMediaUserData
from anime_list_apis.models.attributes.Id import IdType


class TestCacheAble(TestCase):
    """
    Class that tests cache-able objects
    """

    def test_tag_generation(self):
        """
        Tests generating tags
        :return: None
        """
        media = TestMediaData.generate_sample_anime_data()
        user = TestMediaUserData.generate_sample_manga_user_data()

        self.assertEqual("ANIME-1", media.generate_tag(IdType.MYANIMELIST))
        self.assertEqual(
            "MANGA-1-" + user.username,
            user.generate_tag(IdType.MYANIMELIST)
        )

    def test_getters(self):
        """
        Tests if the getter methods work correctly
        :return:
        """

        # Yeah, it's hacky. But it works!
        getters = list(filter(lambda x: x.startswith("get_"), dir(CacheAble)))

        for obj in [
            TestMediaData.generate_sample_anime_data(),
            TestMediaData.generate_sample_manga_data(),
            TestMediaUserData.generate_sample_anime_user_data(),
            TestMediaUserData.generate_sample_manga_user_data(),
            TestMediaListEntry.generate_sample_anime_entry(),
            TestMediaListEntry.generate_sample_manga_entry()
        ]:
            for getter in getters:
                try:
                    result = obj.__getattribute__(getter)()
                    if not getter.startswith("get_username"):
                        self.assertIsNotNone(result)
                except NotImplementedError:
                    self.fail()
