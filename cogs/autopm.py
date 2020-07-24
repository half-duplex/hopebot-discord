# coding=utf-8

import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class AutoPMCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logger.info("joins: %s (%s)", member.name, member.id)
        await self._do_pm(member)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # TODO: make this work. no idea how to get bot's user_id
        # if payload.user_id == self._bot.user_id:
        #     return
        user = self._bot.get_user(payload.user_id)
        if payload.guild_id is None:
            return
        guild = self._bot.get_guild(payload.guild_id)
        if payload.channel_id != guild.system_channel.id:
            return
        logger.info("reacts: %s (%s)", user.name, user.id)
        await self._do_pm(user)
        message = await self._bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        await message.remove_reaction(payload.emoji, user)

    async def _do_pm(self, user):
        if user.dm_channel is None:
            logger.debug("Creating DM channel with %s (%s)", user.name, user.id)
            await user.create_dm()
        chat = user.dm_channel
        await chat.send("Hello! Please send me the HOPE ticket code from your email.")


def setup(bot):
    logger.info("Loaded AutoPM cog")
    bot.add_cog(AutoPMCog(bot))
