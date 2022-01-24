# mCodingBot

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Sigmanificient/mCodingBot)
![GitHub repo size](https://img.shields.io/github/repo-size/Sigmanificient/mCodingBot)
![GitHub last commit](https://img.shields.io/github/last-commit/Sigmanificient/mCodingBot)
![GitHub](https://img.shields.io/github/license/Sigmanificient/mCodingBot)
![GitHub top language](https://img.shields.io/github/languages/top/Sigmanificient/mCodingBot)
![Lines of code](https://img.shields.io/tokei/lines/github/Sigmanificient/mCodingBot)
![Code Style](https://img.shields.io/badge/code%20style-pep8-green)

A maintained [pincer](https://github.com/Pincer-org/Pincer) rewrite of the mCodingBot.
This is a fun bot that is used in James Murphy's mCoding Discord server.

Note: this bot is a community-maintained project.
Although James Murphy (mCoding) may contribute to it,
James is neither the maintainer nor the author of most of the code.

After cloning, install with

```sh
python -m pip install poetry
poetry install
```

Then you can run with

```sh
poetry run python -m mcoding_bot
```

You can also just use the start.sh script to install & run

```sh
./start.sh python
```

Note: You need a postgres database setup. Put the dbname, user, and user password into the .env file. The following would work:
```
CREATE USER user_name WITH ENCRYPTED PASSWORD 'user_password';
CREATE DATABASE database_name WITH OWNER user_name;
```
