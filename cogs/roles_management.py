import discord
import utils.data as data
from utils.roles import get_role, get_next_role
from discord.ext import commands
import asyncio


class Roles:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role('ADMIN')
    async def init(self, ctx):
        data.server = ctx.message.server
        await self.bot.say('Prepared for duty in {} guild!'.format(data.server.name))

    @commands.command(pass_context=True)
    async def invites(self, ctx):
        author = ctx.message.author
        for user_invite in data.users_invites.values():
            if user_invite[0].id == author.id:
                await self.bot.say('<@{}> Total invites: {}'.format(user_invite[0].id, user_invite[1]))
                next_rank, invites_needed = get_next_role(user_invite[1])
                await self.bot.say('<@{}> You need {}  invites for {}'.format(
                    user_invite[0].id, invites_needed - user_invite[1], next_rank))

    @commands.command(pass_context=True)
    async def rank(self, ctx):
        message = '**Rank1** - 100 invites\n**Rank2** - 50 invites\n**Rank3** - 10 invites\n' \
                  '**Rank4** - 5 invites\n**Rank5** - 3 invites\n**Rank6** - 1 invite'
        embed = discord.Embed(title='Ranking system', description=message, color=0xfff71e)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def members(self, ctx):
        everyone = ctx.message.server.members
        members = list(filter(lambda x: not x.bot, everyone))
        online_members = list(filter(lambda x: x.status.value == 'online', members))
        embed = discord.Embed(title='Server members', description='------------------\n''**Online members:** {}'
                                                                  '\n**Total members:** {}'
                              .format(online_members.__len__(), members.__len__()), color=0xfff71e)
        await self.bot.send_message(ctx.message.channel, embed=embed)

async def rli(bot):
    # Get the current invites
    while not bot.is_closed:
        await asyncio.sleep(15)
        # Check if server is ready and registered
        if data.server is None:
            continue
        current_invites = await bot.invites_from(data.server)
        for invite in current_invites:
            # User inviter
            inviter = invite.inviter
            if inviter.id not in data.users_invites:
                data.users_invites[inviter.id] = [inviter, 0]
            if invite.id not in data.invites:
                data.invites[invite.id] = invite
                data.users_invites[inviter.id][1] += invite.uses
            else:
                old_uses = data.invites[invite.id].uses
                difference = invite.uses - old_uses
                data.invites[invite.id] = invite
                data.users_invites[inviter.id][1] += difference

        print(data.users_invites)
        print(data.invites)

async def roles(bot):
    while not bot.is_closed:
        await asyncio.sleep(20)
        # Check if server is ready and registered
        if data.server is None:
            continue
        print('Setting roles...')
        for user_invite in data.users_invites.values():
            # Get stored data
            user = user_invite[0]
            invites = user_invite[1]
            print('{} with {} invites'.format(user.display_name, invites))
            # Get the proper role based on invites
            role_name = get_role(invites)
            roles = discord.utils.get(data.server.roles)
            role = discord.utils.get(data.server.roles, name=role_name)
            if role is None:
                continue
            print('Role-> ' + role.name)
            # Set the role
            member = discord.utils.get(data.server.members, name=user.name)
            if member is None:
                continue
            print(member)
            await bot.add_roles(member, role)


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
    bot.loop.create_task(rli(bot))
    bot.loop.create_task(roles(bot))
