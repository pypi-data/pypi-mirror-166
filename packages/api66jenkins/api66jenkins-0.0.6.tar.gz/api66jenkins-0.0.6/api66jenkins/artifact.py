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
from .mix import RawJsonMixIn


class Artifact(RawJsonMixIn, Item):

    def __init__(self, jenkins, raw):
        super().__init__(
            jenkins, f"{jenkins.url}{raw['url'][1:]}")
        # remove trailing slash
        self.url = self.url[:-1]
        self.raw = raw
        self.raw['_class'] = 'Artifact'

    def save(self, filename=None):
        if not filename:
            filename = self.name
        with self.handle_req('GET', '') as resp:
            save_response_to(resp, filename)


def save_response_to(response, filename):
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
