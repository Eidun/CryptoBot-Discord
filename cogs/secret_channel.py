import discord
import utils.data as data
from utils.roles import get_role, get_next_role
from discord.ext import commands
import asyncio


class Secret:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def secret(self, ctx, channel_name):

        server = ctx.message.server
        permissions = discord.PermissionOverwrite(read_messages=False)
        mine = discord.PermissionOverwrite(read_messages=True)
        channel = await self.bot.create_channel(ctx.message.server, channel_name,
                                      (server.default_role, permissions), (server.me, mine))
        print(channel.name)
        await self.bot.send_message(channel, '**{}** created. Now I\'ll invite users ordered by rank...'.format(channel_name))

        await asyncio.sleep(15)
        rank1 = discord.utils.get(data.server.roles, name='Rank1')
        permissions = discord.PermissionOverwrite(read_messages=True)
        await self.bot.edit_channel_permissions(channel, rank1, permissions)
        await self.bot.send_message(channel, '**{}** invited!'.format(rank1.name))

        await asyncio.sleep(15)
        rank2 = discord.utils.get(data.server.roles, name='Rank2')
        permissions = discord.PermissionOverwrite(read_messages=True)
        await self.bot.edit_channel_permissions(channel, rank2, permissions)
        await self.bot.send_message(channel, '**{}** invited!'.format(rank2.name))


def setup(bot: commands.Bot):
    bot.add_cog(Secret(bot))

