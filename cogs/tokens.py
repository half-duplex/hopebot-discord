# coding=utf-8

import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class TokensCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="ticket")
    async def ticket(self, context, *, token: str):
        print(token)

    @commands.command(name="volunteer")
    async def volunteer(self, context, *, token: str = None):
        if token is None:
            await context.send(
                "Send the ticket code from your email after the command, like this:\n"
                "`{context.command} a1b2c3d4e5f6...`"
            )
            return
        if token == "poweroverwhelming":
            self._bot.get_guild().get_member(context.user)


def setup(bot):
    logger.info("Loaded Tokens cog")
    bot.add_cog(TokensCog(bot))
