from pincer.utils.snowflake import Snowflake
import dotenv


class Config:
    __config = {}
    __config_map = (
        ("mcoding_server", Snowflake),
        ("mcoding_yt_id", str),
        ("member_count_channel", Snowflake),
        ("subscriber_count_channel", Snowflake),
        ("token", str),
        ("view_count_channel", Snowflake),
        ("yt_api_key", str),
    )

    def __init__(self):
        __env = dotenv.dotenv_values('.env')

        for key, _type in self.__config_map:
            if not __env.get(key.upper()):
                raise ValueError(f'Missing key {key} within `.env`.')

            self.__config[key.lower()] = _type(__env.pop(key.upper()))

    def __getattr__(self, item):
        return self.__config.get(item)
