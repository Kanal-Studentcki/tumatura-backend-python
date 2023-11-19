import os
from datetime import time, timezone

import discord
from discord.ext import tasks

from src.utils.discord_utils import DiscordUtils
from src.utils.mongo_utils import MongoUtils
from src.utils.role_utils import roles_diff
from src.utils.wp_utils import WPUtils


class DiscordClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(intents=intents)

        self.GUILD_ID = int(os.environ["DISCORD_GUILD_ID"])

        self.utils = DiscordUtils(self)
        self.mongo_utils = MongoUtils()
        self.wp_utils = WPUtils()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")  # type: ignore[union-attr]

        self.member_role_check.start()
        print("Member role check - task started")

        self.wp_discord_name_update.start()
        print("WP Discord name update - task started")

        print("------")

    async def on_member_join(self, member: discord.Member) -> None:
        user_roles = [role.id for role in member.roles]
        diff = roles_diff(member.name, user_roles)

        if diff["add"]:
            await self.utils.assign_roles(member.guild, member, role_id=diff["add"])

            # TODO: Ładna wiadomośc do usera
            await member.send(
                f"Elo! Bardzo się cieszymy, że jeteś z nami!\n\nPrzydzieliliśmy Ci przysługujące Ci role: {diff['add']}"
            )

    @tasks.loop(time=time(hour=4, minute=0, tzinfo=timezone.utc))
    async def member_role_check(self) -> None:
        print("Starting member role check...")
        self.mongo_utils.clean_expired_user_roles()

        guild = self.utils.get_guild(self.GUILD_ID)
        discord_users = self.utils.get_all_members(guild)

        for user in discord_users:
            diff = roles_diff(user.nick, [role.id for role in user.roles])  # type: ignore[arg-type]

            if diff["add"]:
                await self.utils.assign_roles(guild, user, role_id=diff["add"])
            if diff["delete"]:
                await self.utils.remove_roles(guild, user, role_id=diff["delete"])
            print(f"{user.name} - {diff}")

        print("Finished member role check")

    @tasks.loop(time=time(hour=3, minute=0, tzinfo=timezone.utc))
    async def wp_discord_name_update(self) -> None:
        customers = self.wp_utils.get_all_customers()

        for customer in customers:
            customer_id = customer["customer_id"]
            discord_name = ""  # FIXME: Waiting for Wordpress configuration
            email = customer["email"]

            self.mongo_utils.upsert_user_data(discord_name, customer_id, email)
