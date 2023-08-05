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

# pylint: disable=no-member

from collections import namedtuple


class DeletionMixIn:

    def delete(self):
        self.handle_req('POST', 'doDelete', allow_redirects=False)


class ConfigurationMixIn:

    def configure(self, xml=None):
        if not xml:
            return self.handle_req('GET', 'config.xml').text
        return self.handle_req('POST', 'config.xml',
                               headers=self.headers, data=xml)

    @property
    def name(self):
        return self.url.split('/')[-2]


class DescriptionMixIn:

    def set_description(self, text):
        self.handle_req('POST', 'submitDescription',
                        params={'description': text})


class RunScriptMixIn:

    def run_script(self, script):
        return self.handle_req('POST', 'scriptText',
                               data={'script': script}).text


class EnableMixIn:

    def enable(self):
        return self.handle_req('POST', 'enable')

    def disable(self):
        return self.handle_req('POST', 'disable')


class RawJsonMixIn:

    def api_json(self, tree='', depth=0):
        return self.raw


Parameter = namedtuple('Parameter', ['class_name', 'name', 'value'])


class ActionsMixIn:

    def get_parameters(self):
        parameters = []
        for action in self.api_json()['actions']:
            if 'parameters' in action:
                parameters.extend(Parameter(raw['_class'], raw['name'], raw.get(
                    'value', '')) for raw in action['parameters'])
                break
        return parameters

    def get_causes(self):
        return next((action['causes'] for action in self.api_json()['actions'] if 'causes' in action), [])
