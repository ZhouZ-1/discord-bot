import discord
from discord.ext import commands

import yaml
import asyncio

# Load settings file and set variables
with open('./config/roles.yml') as file:
    settings = yaml.full_load(file)

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.role_channel_id = settings['role_channel_id']
        self.bot.role_log_channel_id = settings['role_log_channel_id']
        self.bot.allowed_roles = settings['allowed_roles']

    @commands.command()
    async def give(self, ctx, *role_names):
        if ctx.message.channel.id != self.bot.role_channel_id:
            return

        user = ctx.message.author
        log_channel = self.bot.get_channel(self.bot.role_log_channel_id)
        success = True

        for role_name in role_names:
            try:
                if role_name.lower() not in (role.lower() for role in self.bot.allowed_roles):
                    raise PermissionError
                role = discord.utils.find(lambda r: role_name.lower() == r.name.lower(), ctx.guild.roles)
                await user.add_roles(role)
                await ctx.send(f'✅ Gave {role_name} to {user}', delete_after=2)
                await log_channel.send(f'✅ Gave {role_name} to {user}')
            except PermissionError:
                await ctx.send(f'❌ Failed to give {role_name} to {user}. You do not have permission to give yourself this role', delete_after=2)
                await log_channel.send(f'❌ Failed to give {role_name} to {user} (role not on whitelist)')
                success = False
            except:
                await ctx.send(f'❌ Failed to give {role_name} to {user}. Please make sure your course code matches exactly e.g. `COMP1511` not `COMP 1511`', delete_after=2)
                await log_channel.send(f'❌ Failed to give {role_name} to {user} (role missing or invalid)')
                success = False

        if success:
            await ctx.message.add_reaction("👍")

        await asyncio.sleep(2.5)
        await ctx.message.delete()


    @commands.command()
    async def remove(self, ctx, *role_names):
        if ctx.message.channel.id != self.bot.role_channel_id:
            return

        user = ctx.message.author
        log_channel = self.bot.get_channel(self.bot.role_log_channel_id)
        success = True

        for role_name in role_names:
            try:
                role = discord.utils.find(lambda r: role_name.lower() == r.name.lower(), ctx.guild.roles)
                await user.remove_roles(role)
                await ctx.send(f'✅ Removed {role_name} from {user}', delete_after=2)
                await log_channel.send(f'✅ Removed {role_name} from {user}')
            except:
                await ctx.send(f'❌ Failed to remove {role_name} from {user}. Please make sure your course code matches exactly e.g. `COMP1511` not `COMP 1511`', delete_after=2)
                await log_channel.send(f'❌ Failed to remove {role_name} from {user}')
                success = False

        if success:
            await ctx.message.add_reaction("👍")

        await asyncio.sleep(2.5)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def countmembers(self, ctx, *, role_name):
        role = discord.utils.find(lambda r: role_name.lower() == r.name.lower(), ctx.guild.roles)

        try:
            await ctx.send(f"`{role_name}` has {len(role.members)} members")
        except:
            await ctx.send(f"`{role_name}` was not found. Please make sure the spelling is correct")


def setup(bot):
    bot.add_cog(Roles(bot))
