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
from collections import namedtuple

from .item import Item
from .mix import DeletionMixIn, DescriptionMixIn


class Users(Item):

    tree = 'users[user[id,absoluteUrl,fullName]]'

    def __iter__(self):
        for user in self.api_json(depth=2, tree=self.tree)['users']:
            yield User(self.jenkins, user['user']['absoluteUrl'])

    def get(self, id=None, full_name=None):
        for user in self.api_json(depth=2, tree=self.tree)['users']:
            if id == user['user']['id'] or full_name == user['user']['fullName']:
                return User(self.jenkins, user['user']['absoluteUrl'])
        return None


ApiToken = namedtuple('ApiToken', ['name', 'uuid', 'value'])


class User(Item, DeletionMixIn, DescriptionMixIn):

    def generate_token(self, name=''):
        entry = 'descriptorByName/jenkins.security.' \
                'ApiTokenProperty/generateNewToken'
        data = self.handle_req('POST', entry,
                               params={'newTokenName': name}).json()['data']
        return ApiToken(data['tokenName'],
                        data['tokenUuid'], data['tokenValue'])

    def revoke_token(self, uuid):
        entry = 'descriptorByName/jenkins.security.' \
                'ApiTokenProperty/revoke'
        return self.handle_req('POST', entry,
                               params={'tokenUuid': uuid})
