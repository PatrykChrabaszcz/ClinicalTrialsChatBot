# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


class DialogFlow:
    def __init__(self):
        self.ai = apiai.ApiAI('b2477d450e0f4c708a50167943645ffa')

    def send_request(self, message):
        request = self.ai.text_request()
        request.session_id = "1"
        request.query = message
        response = request.getresponse().read()

        return response


if __name__ == '__main__':
    df = DialogFlow()

    response = df.send_request("What is the weather today in Freiburg")
    print(response)
