import os


class BaseGameWebSocket:
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 8766

    def __init__(self):
        self.score = 0

    def get_port(self):
        return os.getenv('WS_PORT', self.DEFAULT_PORT)

    def get_host(self):
        return os.getenv('WS_HOST', self.DEFAULT_HOST)

    def get_uri(self):
        return f'ws://{self.get_host()}:{self.get_port()}'

    def exit_game(self):
        print(f'\nGame Over!! Your score is {self.score}!')
        self._shutdown()

    def _shutdown(self):
        self.loop.call_soon_threadsafe(self.loop.stop)