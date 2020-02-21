#!/usr/bin/env python

import asyncio
import os

import websockets

from inputimeout import inputimeout, TimeoutOccurred

from baseclass import BaseGameWebSocket


class GameClient(BaseGameWebSocket):

    async def play_game(self):
        uri = self.get_uri()
        async with websockets.connect(uri) as websocket:
            while True:
                time_out = await websocket.recv()
                received_key = await websocket.recv()
                print(
                    f"The Key is {received_key}\nThe TimeOut is {time_out}")

                try:
                    key = inputimeout('Enter your response\t',
                                      timeout=int(time_out))
                except TimeoutOccurred:
                    print('Input Timeout, moving on...')
                    continue

                await websocket.send(key)
                self.score = await asyncio.wait_for(websocket.recv(), timeout=1)
                print(f'Your current score is {self.score}\n')

    def run(self):
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.play_game())
        except websockets.ConnectionClosed:
            self.exit_game()


game_client = GameClient()
game_client.run()
