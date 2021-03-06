import asyncio
from concurrent import futures

import websockets

from baseclass import BaseGameWebSocket


class GameServer(BaseGameWebSocket):

    MAX_SCORE = 10
    MIN_SCORE = -3
    EXIT_ON_TIMEOUT_THRESHOLD = 3

    def __init__(self):
        super().__init__()
        self.score_list = []

    def is_game_over_timeout(self):
        return (
            len(self.score_list) >= self.EXIT_ON_TIMEOUT_THRESHOLD and
            not any(self.score_list[-self.EXIT_ON_TIMEOUT_THRESHOLD:])
        )

    def is_game_over_score(self):
        return not (self.MIN_SCORE < self.score < self.MAX_SCORE)

    def get_score(self, input_key, recieved_key):
        return int(input_key == recieved_key) or -1

    async def serve_game(self, websocket, loop):
        while True:
            key = input('Enter Key\t')
            time_out = input('Enter TimeOut\t')
            await websocket.send(f'{time_out}')
            await websocket.send(f'{key}')
            try:
                recieved_key = await asyncio.wait_for(
                    websocket.recv(),
                    timeout=int(time_out))
            except futures.TimeoutError:
                self.score_list.append(0)
                if self.is_game_over_timeout():
                    self.exit_game()
                    break
            else:
                latest_score = self.get_score(key, recieved_key)
                self.score_list.append(latest_score)
                self.score += latest_score
                await websocket.send(f'{self.score}')
                if self.is_game_over_score():
                    self.exit_game()
                    break

    def run(self):
        server = websockets.serve(
            self.serve_game,
            self.get_host(),
            self.get_port()
        )

        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(server)
            self.loop.run_forever()
        except KeyboardInterrupt:
            print(f'Exiting game. Final score is {self.score}')
        except Exception as e:
            print("Server Error!", e)


game_server = GameServer()
game_server.run()
