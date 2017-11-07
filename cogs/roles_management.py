import discord
import utils.data as data
from utils.roles import get_role
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


async def rli(bot):
    # Get the current invites
    while not bot.is_closed:
        await asyncio.sleep(60)
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
                data.users_invites[inviter.id][1] += difference

        print(data.users_invites)
        print(data.invites)

async def roles(bot):
    while not bot.is_closed:
        await asyncio.sleep(150)
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
            print('Role-> ' + role.name)
            # Set the role
            member = discord.utils.get(data.server.members, name=user.name)
            print(member)
            await bot.add_roles(member, role)


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
    bot.loop.create_task(rli(bot))
    bot.loop.create_task(roles(bot))
