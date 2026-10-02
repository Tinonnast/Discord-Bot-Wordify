from discord import activity, app_commands
import asyncio
import discord
from discord.app_commands import Group
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Greedy, Context
from discord.ui import Button, View
from typing import Literal, Optional
from discord import app_commands
from datetime import datetime, timedelta
import time
from discord import DMChannel
import calendar
import random
import typing
from discord import app_commands
import requests
import json
from rich.console import Console
import aiohttp
import os
import dotenv
from better_profanity import profanity

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
intents.message_content = True
start_date_pretty = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents, application_id=1334590704705343499)
    
    async def setup_hook(self):
        await self.tree.sync()
    
    async def on_ready(self):
        await bot.tree.sync()

        print("Bot has started.")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Logs"))

bot = MyBot()
bot.remove_command("help")

logcolor = discord.Colour.blue

## Reporting
def pass_variables(self, message):
    self.message = message

class ReportMessageModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Report a Message to Server Staff")
        self.user_input = discord.ui.TextInput(
            label="Report Message",
            style=discord.TextStyle.short,
            placeholder="Reason...",
            required=True,
        )
        self.add_item(self.user_input)

    async def on_submit(self, interaction: discord.Interaction):
        data = json_r()
        channel = await bot.fetch_channel(data["report"])
        

        await channel.send(f"""{interaction.user.mention} reported "{self.message.content}" from <@{self.message.author.id}>
Reason: "{self.user_input.value}"
<@&1305128938003103755>""",
            view=Buttons())
        await interaction.response.send_message("The message was reported successfully to server staff.", ephemeral=True)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    def pass_variables(self, message):
        self.message = message

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        button.style=discord.ButtonStyle.secondary
        button.label = "Delete"
        await interaction.response.edit_message(view=self)
        await self.message.delete()


@bot.tree.context_menu(name="Report")
async def report_message_context(interaction: discord.Interaction, message: discord.Message):
    print(message)
    ReportMessageModal().pass_variables(message)
    modal = ReportMessageModal()
    await interaction.response.send_modal(modal)

## Save Message
@bot.event
async def on_message(message):
    delete_message = profanity.contains_profanity(message.content)
    if delete_message:
        await message.delete()

    with open("C:/Users/tino/.vscode/DiscordBot/Wordify/messagelogs.json", "r") as file:
        data = json.load(file)

    data[str(message.channel.id)] = {}
    data[str(message.channel.id)][str(message.id)] = message.content

    with open("C:/Users/tino/.vscode/DiscordBot/Wordify/messagelogs.json", "w") as file:
        json.dump(data, file, indent=4)

    level_amounts = {"20": "1", "50": "2", "75": "3", "100": "4", "150": "5", "250": "6", "400": "7", "600": "8", "750": "9", "1000": "10"}
    with open("Wordify/levels.json", "r") as file:
        data = json.load(file) 
    if str(message.author.id) not in data["users"]:
        data["users"][str(message.author.id)] = "0"
    current_amount = int(data["users"][str(message.author.id)])
    data["users"][str(message.author.id)] = str(current_amount + 1)
    if data["users"][str(message.author.id)] in level_amounts:
        response = requests.post("https://discord.com/api/webhooks/1341779933785096222/rO36Y9tLpZSjRwALmsXgY-1GqOp99zLb_p5R73adetI0P4mBgp8EWJ1qQYXZsbOUVye5", json={"content": f"<@{message.author.id}> just got Level {level_amounts[data["users"][str(message.author.id)]]}!"})
        if level_amounts[data["users"][str(message.author.id)]] == "5":
            role = message.guild.get_role(1341770751732355144)
            await message.author.add_roles(role)
    with open("Wordify/levels.json", "w") as file:
        json.dump(data, file, indent=4)


## Log Commands
def LogAction(userid, command):
    with open('Wordify/logs.json', 'r') as file:
        data = json.load(file)

    if str(userid) not in data:
        data[str(userid)] = {}
    data[str(userid)][str(datetime.now())] = command

    with open('Wordify/logs.json', 'w') as file:
        json.dump(data, file, indent=4)

## Read messagelogs.json
def messagelogsread():
    with open("C:/Users/tino/.vscode/DiscordBot/Wordify/messagelogs.json", "r") as file:
        data = json.load(file)
    return data

## Logging 

## attributes
channel_attributes = [
    "category",
    "changed_roles",
    "created_at",
    "guild",
    "jump_url",
    "mention",
    "name",
    "overwrites",
    "permissions_synced",
    "position"
]

guild_attributes = [
    "afk_channel",
    "afk_timeout",
    "approximate_member_count",
    "approximate_presence_count",
    "banner",
    "bitrate_limit",
    "categories",
    "channels",
    "chunked",
    "created_at",
    "default_notifications",
    "default_role",
    "description",
    "discovery_splash",
    "dm_spam_detected_at",
    "dms_paused_until",
    "emoji_limit",
    # "emojis",
    "explicit_content_filter",
    "features",
    "filesize_limit",
    "forums",
    "icon",
    "id",
    "invites_paused_until",
    "large",
    "max_members",
    "max_presences",
    "max_stage_video_users",
    "max_video_channel_users",
    "me",
    "member_count",
    "members",
    "mfa_level",
    "name",
    "nsfw_level",
    "owner",
    "owner_id",
    "preferred_locale",
    "premium_progress_bar_enabled",
    "premium_subscriber_role",
    "premium_subscribers",
    "premium_subscription_count",
    "premium_tier",
    "public_updates_channel",
    "raid_detected_at",
    "roles",
    "rules_channel",
    "safety_alerts_channel",
    "scheduled_events",
    "self_role",
    "shard_id",
    "soundboard_sounds",
    "splash",
    "stage_channels",
    "stage_instances",
    "sticker_limit",
    # "stickers",
    "system_channel",
    "system_channel_flags",
    "text_channels",
    "threads",
    "unavailable",
    "vanity_url",
    "vanity_url_code",
    "verification_level",
    "voice_channels",
    "voice_client",
    "widget_channel",
    "widget_enabled"
]



@bot.event
async def on_connect():
    channel = await bot.fetch_channel(1415363995686404217)
    await channel.send("Client successfully connected to Discord.")

@bot.event
async def on_disconnect():
    channel = await bot.fetch_channel(1415363995686404217)
    await channel.send("Client disconnected from Discord.")


## Messages
@bot.event
async def on_message_delete(message):
    message_before = messagelogsread()
    embed = discord.Embed(title=f"Message Deleted", description=f"**{message.author.global_name}**({message.author.name}) deleted a message in [{message.channel.name}]({message.jump_url})")
    embed.add_field(name="", value=message_before[str(message.channel.id)][str(message.id)])
    embed.set_footer(text=f"User ID: {message.author.id}")
    data = json_r()
    channelid = data["message"]
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.content != after.content and before.author.id != 1334590704705343499:
        embed = discord.Embed(title=f"Message Deleted", description=f"**{after.author.global_name}**({after.author.name}) edited a message in [{after.channel.name}](https://discord.com/channels/{after.guild.id}/{after.channel.id})")
        embed.add_field(name="", value=f"**Before:**\n{before.content}\n\n**After:**\n{after.content}")
        embed.set_footer(text=f"User ID: {after.author.id}")
        data = json_r()
        channelid = data["message"]
        channel = await bot.fetch_channel(channelid)
        await channel.send(embed=embed)


## Channels
def channels_changed_end_text(before, after):
    added = [] # making the end list
    overwrite_end = []
    for attr in channel_attributes:
        if getattr(before, attr) != getattr(after, attr): # If the before is the same as after

            if attr == "changed_roles": # exception for the changed_roles
                Do_Nothing = True
                # changed_roles_names = []
                # for role in after.changed_roles:
                #     changed_roles_names.append(role.name)
                # added.append(f"**changed_roles**: {', '.join(changed_roles_names)}")

            elif attr == "overwrites": # exception for overwrites
                for role in after.changed_roles:
                    overwrite = after.overwrites.get(role)
                    if overwrite:
                        overwrite_end.append(f"{role.name} - {', '.join([perm for perm, value in overwrite if value is not None])}")

            else: # append the end text thing
                added.append(f"**{attr}**: {getattr(after, attr)}")

    if overwrite_end != []:
        added.append(f"\noverwrites:\n{'\n'.join(overwrite_end)}")
    end_text = f"{'\n'.join(added)}"
    return end_text

def channels_end_text(channel):
    added = [] # making the end list
    overwrite_end = []
    id_list = []
    for attr in channel_attributes:
        if attr == "changed_roles": # exception for the changed_roles
            Do_Nothing = True
            # changed_roles_names = []
            # for role in channel.changed_roles:
            #     changed_roles_names.append(role.name)
            # added.append(f"**changed_roles**: {', '.join(changed_roles_names)}")

        elif attr == "overwrites": # exception for overwrites
            for role in channel.changed_roles:
                overwrite = channel.overwrites.get(role)
                if overwrite:
                    overwrite_end.append(f"{role.name} - {', '.join([perm for perm, value in overwrite if value is not None])}")

        elif attr == "mention":
            for character in channel.mention:
                id_list.append(character)
            id_list.remove("<")
            id_list.remove("#")
            id_list.remove(">")
            added.append(f"**channel_id**: {''.join(id_list)}")

        else: # append the end text thing
            added.append(f"**{attr}**: {getattr(channel, attr)}")

    end_text = f"{'\n'.join(added)}\n\noverwrites:\n{'\n'.join(overwrite_end)}"
    return end_text


@bot.event
async def on_guild_channel_delete(channel):
    embed=discord.Embed(title=f"Channel Deleted - {channel.name}", description=f"{channels_end_text(channel)}")
    data = json_r()
    channelid = data["channels"]
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    embed=discord.Embed(title=f"Channel Created - {channel.name}", description=f"{channels_end_text(channel)}")
    data = json_r()
    channelid = data["channels"]
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    embed=discord.Embed(title=f"Channel Updated - {before.name}", description=channels_changed_end_text(before=before, after=after))
    data = json_r()
    channelid = data["channels"]
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=embed)

@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    embed=discord.Embed(title="Pins Update", description=f"A message in {channel} was updated at {last_pin}.")
    data = json_r()
    channelid = data["channels"]
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=embed)

## Guild
def guild_changed(before, after):
    added = [] # making the end list
    features_added = []
    features_removed = []

    for attr in guild_attributes:
        if getattr(before, attr) != getattr(after, attr):
            if attr == "features":
                #do nothing
                nothing = True # very creative
            else:
                added.append(f"**{attr}**: {getattr(after, attr)}")

    # DOESNT WORK
    # for feature in after.features:
    #     if feature not in before.features:
    #         features_added.append(feature)

    # for feature in before.features:
    #     if feature not in after.features:
    #         features_removed.append(feature)


    # FEATURES FOR end_text:      **features added:**\n{', '.join(features_added)}\n\n**features removed:**\n{', '.join(features_removed)}
    end_text = f"{'\n'.join(added)}"
    return end_text

@bot.event
async def on_guild_update(before, after):
    embed=discord.Embed(title="Guild Updated", description=guild_changed(before, after))
    data = json_r()
    channelid = data["guilds"]
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=embed)

## Audit Log
@bot.event
async def on_audit_log_entry_create(entry):
    print(entry.action)
    print(entry.user)
    print(entry.id)
    print(entry.target)
    print(entry.reason)
    print(entry.extra)
    print(entry.category)
    print(entry.changes)
    print(entry.before)
    print(entry.after)







## Function
def json_r():
    with open("Wordify/channels.json", "r") as file:
        data = json.load(file)
    return data

def json_w(data):
    with open("Wordify/channels.json", "w") as file:
        json.dump(data, file, indent=4)

# def check_server_existence(interaction):
#     data = json_r()
#     if str(interaction.guild.id) in data:
#         return
#     else:
#         data[str(interaction.guild.id)] = {
#                 "message": "channelid",
#                 "report": "channelid",
#                 "members": "channelid",
#                 "integrations & commands": "channelid",
#                 "guilds": "channelid",
#                 "channels": "channelid",
#                 "polls & reactions": "channelid",
#                 "roles": "channelid",
#                 "events & stages": "channelid",
#                 "threads": "channelid",
#                 "voice": "channelid"
#             }
#         json_w(data = data)
#         return

## Logging channel set
class logging_channels(app_commands.Group):
    @app_commands.command(name="message", description="Logging for Message Deleted, Edited")
    async def messagelogging(self, interaction: discord.Interaction):
        data = json_r()
        # check_server_existence(interaction=interaction)
        if data["message"] == str(interaction.channel.id):
            await interaction.response.send_message("This Channel is already the Channel for Messages.")
        else:
            data["message"] = str(interaction.channel.id)
            json_w(data=data)
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for messages.")

    @app_commands.command(name="report", description="Set the Channel for Reports using the Context Menu")
    async def setreportchannel(self, interaction: discord.Interaction):
        data = json_r() 
        
        if data["report"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for Reports.") 
        else: 
            data["report"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for reports.")

    @app_commands.command(name="members", description="Set the Logging Channel for Members")
    async def memberslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["members"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for Members.") 
        else: 
            data["members"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for members.")

    @app_commands.command(name="integrations-commands", description="Set the Logging Channel for integrations & commands")
    async def integrationscommandslogging(self, interaction: discord.Interaction): 
        data = json_r() 

        if data["integrations & commands"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for integrations & commands.") 
        else: 
            data["integrations & commands"] = str(interaction.channel.id) 
            json_w(data=data) 
        await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for integrations & commands.")

    @app_commands.command(name="guilds", description="Set the Logging Channel for guilds") 
    async def guildslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["guilds"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for guilds.") 
        else: 
            data["guilds"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for guilds.")

    @app_commands.command(name="channels", description="Set the Logging Channel for channels") 
    async def channelslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["channels"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for channels.") 
        else: 
            data["channels"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for channels.")        

    @app_commands.command(name="polls-reactions", description="Set the Logging Channel for polls & reactions")
    async def pollsreactionslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["polls & reactions"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for polls & reactions.") 
        else: 
            data["polls & reactions"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for polls & reactions.")
    
    @app_commands.command(name="roles", description="Set the Logging Channel for roles") 
    async def roleslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["roles"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for roles.") 
        else: 
            data["roles"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for roles.")

    @app_commands.command(name="events-stages", description="Set the Logging Channel for events & stages") 
    async def eventsstageslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["events & stages"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for events & stages.") 
        else: 
            data["events & stages"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for events & stages.")

    @app_commands.command(name="threads", description="Set the Logging Channel for threads") 
    async def threadslogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["threads"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for threads.") 
        else: 
            data["threads"] = str(interaction.channel.id) 
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for threads.")

    @app_commands.command(name="voice-channels", description="Set the Logging Channel for voice channels") 
    async def voicelogging(self, interaction: discord.Interaction): 
        data = json_r() 
        
        if data["voice"] == str(interaction.channel.id): 
            await interaction.response.send_message("This Channel is already the Channel for voice channels.") 
        else: 
            data["voice"] = str(interaction.channel.id)
            json_w(data=data) 
            await interaction.response.send_message(f"This Channel ({interaction.channel.id}) has been set to the log channel for voice channels.")

bot.tree.add_command(logging_channels(name="loggingchannel-set", description="Set the logging channels"))

dotenv.load_dotenv(dotenv_path="C:/Users/tino/.vscode/DiscordBot/tokens.env")
bot.run(os.getenv(key="TOKENMOD"))