#!/usr/bin/env python

import asyncio
import websockets

from inputimeout import inputimeout, TimeoutOccurred

from constants import WS_HOST, WS_PORT, WS_URI


async def client():
    uri = WS_URI.format(host=WS_HOST, port=WS_PORT)
    score = 0
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                time_out = await websocket.recv()
                recieved_key = await websocket.recv()
                print(f"The Key is {recieved_key}\nThe TimeOut is {time_out}")

                try:
                    key = inputimeout('Enter your response\t',
                                      timeout=int(time_out))
                except TimeoutOccurred:
                    print('Input Timeout, moving on...')
                    continue

                await websocket.send(key)
                score = await websocket.recv()
                print(f'current score is {score}')
        except websockets.ConnectionClosed:
            print(f'Game Over!! Your score is {score}!')

loop = asyncio.get_event_loop()
stop = asyncio.Future()
loop.run_until_complete(client())
