#!/usr/bin/env python3
# coding=utf-8

import logging
import os
from sys import stdout

from discord.ext import commands
import MySQLdb
import MySQLdb.cursors
from tomlkit.toml_file import TOMLFile

logger = logging.getLogger()


class HOPEBot:
    _bot: commands.Bot
    _config: dict
    _db_cfg: dict
    _token_lock: None

    def __init__(self):
        config_file = os.environ.get(
            "CONFIG", os.path.join(os.path.dirname(__file__), "config.toml")
        )
        toml = TOMLFile(config_file)
        self._config = toml.read()

        for key in [
            "db_host",
            "db_name",
            "db_user",
            "db_pass",
            "discord_token",
            "discord_guild_id",
        ]:
            if key not in self._config:
                logging.error("Required attribute %r not in config", key)
                raise Exception("MissingConfigEntry", key)
        if "db_table_prefix" not in self._config:
            self._config["db_table_prefix"] = ""

        self._db_cfg = {
            "host": self._config["db_host"],
            "user": self._config["db_user"],
            "passwd": self._config["db_pass"],
            "db": self._config["db_name"],
            "cursorclass": MySQLdb.cursors.DictCursor,
            "charset": "utf8mb4",
        }

        logger.setLevel(getattr(logging, self._config.get("log_level", logging.INFO)))
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
        )
        logger.addHandler(handler)
        logging.getLogger("websockets").setLevel("INFO")
        logging.getLogger("discord").setLevel("INFO")

        self._bot = commands.Bot(command_prefix=self._command_prefix)
        for cog in self._config.get("cogs", []):
            self._bot.load_extension("cogs." + cog)

    def _command_prefix(self, bot, message):
        prefixes = [".", "!"]
        if not message.guild:
            return commands.when_mentioned_or("", *prefixes)(bot, message)
        return commands.when_mentioned_or(*prefixes)(bot, message)

    def run(self):
        self._bot.run(self._config["discord_token"], bot=True, reconnect=True)


if __name__ == "__main__":
    bot = HOPEBot()
    bot.run()
