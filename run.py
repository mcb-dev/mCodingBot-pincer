import mcodingbot
import dotenv

if __name__ == '__main__':
    mcodingbot.Bot(dotenv.dotenv_values('.env').get('TOKEN')).run()
