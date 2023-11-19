from typing import List

import discord

from src.utils.mongo_utils import MongoUtils


class DiscordUtils:
    def __init__(self, client: discord.Client):
        self.client = client
        self.mongo = MongoUtils()

    async def assign_roles(self, guild: discord.Guild, member: discord.Member, *, role_name: List[str] = None,
                           role_id: List[int] = None) -> None:
        if not role_id and not role_name:
            raise Exception("Neither role ID nor role name is specified")

        if not role_id and role_name:
            role_id = [self.mongo.get_role_id_by_name(role) for role in role_name]

        roles = [self._get_role_by_id(guild, role) for role in role_id]

        await member.add_roles(*roles)

    async def remove_roles(self, guild: discord.Guild, member: discord.Member, *, role_name: List[str] = None,
                           role_id: List[int] = None) -> None:
        if not role_id and not role_name:
            raise Exception("Neither role ID nor role name is specified")

        if not role_id and role_name:
            role_id = [self.mongo.get_role_id_by_name(role) for role in role_name]

        roles = [self._get_role_by_id(guild, role) for role in role_id]

        await member.remove_roles(*roles)
        # except discord.HTTPException:

    def get_guild(self, guild_id: int) -> discord.Guild:
        guild = self.client.get_guild(guild_id)

        if guild is None:
            raise Exception("Invalid guild id")
        return guild

    def get_member_by_id(self, guild: discord.Guild, user_id: int) -> discord.Member:
        member = guild.get_member(user_id)

        if member is None:
            raise Exception("Invalid user id")
        return member

    def get_all_members(self, guild: discord.Guild) -> List[discord.Member]:
        members = list(guild.members)
        members.remove(self.get_member_by_id(guild, 1172185255185231953))  # exclude tu.MATURA bot

        return members

    def _get_role_by_id(self, guild: discord.Guild, role_id: int) -> discord.Role:
        role = guild.get_role(role_id)

        if role is None:
            raise Exception("Invalid role id")
        return role
