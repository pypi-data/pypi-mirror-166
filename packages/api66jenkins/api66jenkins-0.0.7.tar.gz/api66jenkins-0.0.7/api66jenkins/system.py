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
import json
from functools import partial

from .artifact import save_response_to
from .item import Item, snake
from .mix import RunScriptMixIn


class System(Item, RunScriptMixIn):

    def __init__(self, jenkins, url):
        '''
        see: https://support.cloudbees.com/hc/en-us/articles/216118748-How-to-Start-Stop-or-Restart-your-Instance-
        '''
        super().__init__(jenkins, url)

        def _post(entry):
            return self.handle_req('POST', entry, allow_redirects=False)

        for entry in ['restart', 'safeRestart', 'exit',
                      'safeExit', 'quietDown', 'cancelQuietDown']:
            setattr(self, snake(entry), partial(_post, entry))

    def reload_jcasc(self):
        return self.handle_req('POST', 'configuration-as-code/reload')

    def export_jcasc(self, filename='jenkins.yaml'):
        with self.handle_req('POST', 'configuration-as-code/export') as resp:
            save_response_to(resp, filename)

    def apply_jcasc(self, new):
        params = {"newSource": new}
        resp = self.handle_req(
            'POST', 'configuration-as-code/checkNewSource', params=params)
        if resp.text.startswith('<div class=error>'):
            raise ValueError(resp.text)
        d = {'json': json.dumps(params),
             'replace': 'Apply new configuration'}
        return self.handle_req('POST', 'configuration-as-code/replace', data=d)

    def decrypt_secret(self, text):
        cmd = f'println(hudson.util.Secret.decrypt("{text}"))'
        return self.run_script(cmd)
