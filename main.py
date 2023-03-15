import config
import re


from typing import Optional

import discord
from discord import app_commands


MY_GUILD = discord.Object(id=config.get_guild_id())


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
@app_commands.rename(color='color_rgb')
@app_commands.describe(color='顏色的 RGB 代碼 (六碼)')
@app_commands.describe(member='選擇其他成員，複製他們的顏色')
async def change_color(
    interaction: discord.Interaction,
    color: Optional[str] = None,
    member: Optional[discord.Member] = None
):
    """更換暱稱顏色"""

    await interaction.response.defer()

    if color is not None:
        color = color.lower()

        if re.match("^[0-9a-f]{6}$", color) is None:
            return await interaction.followup.send("無效的設定")

        await remove_role(interaction)
        await add_role(interaction, color)
        await interaction.followup.send(f"已經將您的暱稱顏色更改為 #{color}")
    elif member is not None:
        color_int = member.color.value
        color = hex(color_int)
        color = re.sub("0x", "", color)
        color = color.rjust(6, "0")

        await remove_role(interaction)
        await add_role(interaction, color)
        await interaction.followup.send(f"已經將您的暱稱顏色更改成跟 {member} 一樣的顏色了")
    else:
        await interaction.followup.send("無效的設定（color 或 member 必須擇一輸入）")


async def add_role(interaction: discord.Interaction, lower_color: str):
    """增加純顏色身分組至指定使用者"""
    filtered_role = list(filter(lambda role: role.name ==
                                f"#{lower_color}", interaction.guild.roles))
    has_role = len(filtered_role) != 0

    if not has_role:
        await interaction.guild.create_role(name=f"#{lower_color}", color=int(lower_color, 16), permissions=discord.Permissions())
        filtered_role = list(filter(lambda role: role.name ==
                                    f"#{lower_color}", interaction.guild.roles))

    role = filtered_role[0]

    await interaction.user.add_roles(role)


async def remove_role(interaction: discord.Interaction):
    """刪除指定使用者的純顏色身分組"""
    filtered_role = list(
        filter(lambda role: role.name.startswith("#"), interaction.user.roles))
    has_role = len(filtered_role) != 0

    if has_role:
        role = filtered_role[0]
        await interaction.user.remove_roles(role)

client.run(config.get_token())
