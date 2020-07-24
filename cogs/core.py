# coding=utf-8

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class CoreCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    # @self._bot.event
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("ready!")
        await self._bot.change_presence(
            activity=discord.Game(name="Destroy All Humans")
        )

    @commands.command(hidden=True)
    @commands.is_owner()
    async def chatinfo(self, context):
        response = "\n"
        if context.guild:
            response += "Guild ID: {}\n".format(context.guild.id)
        response += "Chat ID: {}".format(context.channel.id)
        await context.send(response)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def react(self, context, *, emoji: str = None):
        if not emoji:
            await context.send(f"Usage: {context.command} :emoji:")
            return
        message = (await context.channel.history(limit=2).flatten())[1]
        await message.add_reaction(emoji)

    # Cog management
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, context, *, extension: str = None):
        await self._manage_ext(self._bot.load_extension, context, extension)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, context, *, extension: str = None):
        await self._manage_ext(self._bot.unload_extension, context, extension)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, context, *, extension: str = None):
        await self._manage_ext(self._bot.reload_extension, context, extension)

    async def _manage_ext(self, func, context, extension):
        if extension is None:
            await context.send("Usage: {context.command} some_cog")
            return
        return func("cogs." + extension)


def setup(bot):
    logger.info("Loaded Core cog")
    bot.add_cog(CoreCog(bot))
