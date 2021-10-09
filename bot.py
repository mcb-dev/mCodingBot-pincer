import dotenv
import pincer
from pincer import Client
from pincer.objects import Message, Embed


class Bot(Client):

    def __init__(self, token: str):
        self.theme = 0x0B7CD3
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

    def embed(self, **kwargs):
        _embed = Embed(**kwargs, color=self.theme)

        return _embed.set_footer(
            text=f"{self.user.name} - m!help for " "more information",
            icon_url=self.user.avatar_url,
        )


if __name__ == '__main__':
    Bot(dotenv.dotenv_values('.env').get('TOKEN')).run()
