import dotenv
import pincer
from pincer import Client
from pincer.objects import Message


class Bot(Client):

    def __init__(self, token: str):
        super(Bot, self).__init__(
            token,
            intents=pincer.Intents.all()
        )

    @Client.event
    async def on_ready(self):
        print(
            "       _____       _ _            _____     _",
            " _____|     |___ _| |_|___ ___   | __  |___| |_",
            "|     |   --| . | . | |   | . |  | __ -| . |  _|",
            "|_|_|_|_____|___|___|_|_|_|_  |  |_____|___|_|",
            "                          |___|" "",
            sep="\n",
        )


if __name__ == '__main__':
    Bot(dotenv.dotenv_values('.env').get('TOKEN')).run()
