# encoding: utf-8
"""
Copyright (c) [2022] [sanmejie]
[Software Name] is licensed under the Mulan PSL v1.
You can use this software according to the terms and conditions of the Mulan PSL v1.
You may obtain a copy of Mulan PSL v1 at:
    http://license.coscl.org.cn/MulanPSL
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
PURPOSE.
See the Mulan PSL v1 for more details.
"""

from .item import Item
from .mix import ConfigurationMixIn, DeletionMixIn


class Credentials(Item):

    def get(self, id):
        for item in self.api_json(tree='credentials[id]')['credentials']:
            if item['id'] == id:
                return Credential(self.jenkins,
                                  f'{self.url}credential/{id}/')
        return None

    def create(self, xml):
        self.handle_req('POST', 'createCredentials',
                        headers=self.headers, data=xml)

    def __iter__(self):
        for item in self.api_json(tree='credentials[id]')['credentials']:
            yield Credential(self.jenkins,
                             f'{self.url}credential/{item["id"]}/')


class Credential(Item, ConfigurationMixIn, DeletionMixIn):
    pass
