"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import os
import json
import time
import random
import getopt
import sys


class ConvAISampleBot:

    def __init__(self, bot_id):
        self.chat_id = None
        self.observation = None
        self.bot_id = bot_id

    def observe(self, m):
        if self.chat_id is None:
            if m['message']['text'].startswith('/start '):
                self.chat_id = m['message']['chat']['id']
                self.observation = m['message']['text']
                print("Start new chat #%s" % self.chat_id)
            else:
                self.observation = None
                print("Multiple chats are not allowed. Ignore message")
        else:
            if self.chat_id == m['message']['chat']['id']:
                if m['message']['text'] == '/end':
                    self.chat_id = None
                    self.observation = None
                    print("End chat #%s" % self.chat_id)
                else:
                    self.observation = m['message']['text']
                    print("Accept message as part of chat #%s" % self.chat_id)
            else:
                self.observation = None
                print("Multiple dialogs are not allowed. Ignore message.")
        return self.observation

    def act(self):
        if self.chat_id is None:
            print("Dialog not started yet. Do not act.")
            return

        if self.observation is None:
            print("No new messages for chat #%s. Do not act." % self.chat_id)
            return

        message = {
            'chat_id': self.chat_id
        }

        texts = [
            'I love you!',
            'Wow!',
            'Really?',
            'Nice!',
            'Hi',
            'Hello',
            "This is not very interesting. Let's change the subject of the conversation. For example, let's talk about cats. What do you think?",
            '/end']
        text = texts[random.randint(0, 7)]

        data = {}
        if text == '':
            print("Decided to do not respond and wait for new message")
            return
        elif text == '/end':
            print("Decided to finish chat %s" % self.chat_id)
            self.chat_id = None
            data['text'] = '/end'
            data['evaluation'] = {
                'quality': 0,
                'breadth': 0,
                'engagement': 0
            }
        else:
            print("Decided to respond with text: %s" % text)
            data = {
                'text': "%s : %s" % (self.bot_id[0:7], text),
                'evaluation': 0
            }

        message['text'] = json.dumps(data)
        return message


def main(argv):
    USAGE = "bot.py -i <bot id> -u <router bot url>"
    BOT_ID = None
    ROUTER_BOT_URL = None

    try:
        opts, args = getopt.getopt(argv,'hi:u:', ['bot_id','router_bot_url'])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
            sys.exit()
        elif opt == '-i':
            BOT_ID = arg
        elif opt == '-u':
            ROUTER_BOT_URL = arg

    if BOT_ID is None or ROUTER_BOT_URL is None:
        print(USAGE)
        sys.exit(2)

    BOT_URL = os.path.join(ROUTER_BOT_URL, BOT_ID)

    bot = ConvAISampleBot(BOT_ID)

    while True:
        try:
            time.sleep(1)
            print("Get updates from server")
            res = requests.get(os.path.join(BOT_URL, 'getUpdates'))

            if res.status_code != 200:
                print(res.text)
                res.raise_for_status()

            print("Got %s new messages" % len(res.json()))
            for m in res.json():
                print("Process message %s" % m)
                bot.observe(m)
                new_message = bot.act()
                if new_message is not None:
                    print("Send response to server.")
                    res = requests.post(os.path.join(BOT_URL, 'sendMessage'),
                                        json=new_message,
                                        headers={'Content-Type': 'application/json'})
                    if res.status_code != 200:
                        print(res.text)
                        res.raise_for_status()
            print("Sleep for 1 sec. before new try")
        except Exception as e:
            print("Exception: {}".format(e))


if __name__ == '__main__':
    main(sys.argv[1:])
