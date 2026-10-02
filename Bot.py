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
import base64
import json
import ast
from rich.console import Console
from deep_translator import GoogleTranslator
import aiohttp
from urllib.parse import urlencode
from urllib.request import urlretrieve
import re
from langdetect import detect

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
start_date_pretty = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents, application_id=1333529459843792897)
    
    async def setup_hook(self):
        await self.tree.sync()
    
    async def on_ready(self):
        console = Console()

        def print_colored_log(level, message, level_color_hex, first_message_color_hex, other_message_color_hex):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            level_color = f"#{level_color_hex}"
            first_message_color = f"#{first_message_color_hex}"
            other_message_color = f"#{other_message_color_hex}"
            parts = message.split(" ", 1)
            first_part = parts[0] if len(parts) > 0 else ""
            remaining_message = parts[1] if len(parts) > 1 else ""

            console.print(f"[#808080]{timestamp}[/] [bold {level_color}]{level:<8}[/] "
                        f"[{first_message_color}]{first_part}[/] {remaining_message}")

        print_colored_log("INFO", "discord.bot Bot has been started", "2196F3", "c965c9", "#FFFFFF")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Python Code"))

bot = MyBot()
bot.remove_command("help")

class ReportMessageModal(discord.ui.Modal):
    # Modal for collecting a report reason
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
        message = message_global

        def find_channelid_for_report(data):
            for user in data['servers']:
                if user['serverid'] == interaction.guild_id:
                    return user['channelid']
            return None

        with open('data.json', 'r') as file:
            channel = bot.get_channel(find_channelid_for_report(data = json.load(file)))

        await channel.send(f"""{interaction.user.mention} reported "{message_global.content}" from <@{message_global.author.id}>
Reason: "{self.user_input.value}"
<@&1305128938003103755>""",
            view=Buttons())
        await interaction.response.send_message("The message was reported successfully to server staff.", ephemeral=True)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)


    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        button.style=discord.ButtonStyle.secondary
        button.label = "Delete"
        await interaction.response.edit_message(view=self)
        await message_global.delete()

    @discord.ui.button(label="Timeout", style=discord.ButtonStyle.danger)
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        button.style=discord.ButtonStyle.secondary
        button.label="Timeout"
        await interaction.response.send_message("Choose a Timeout Duration", view=DropdownMenu())

class DropdownMenu(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Select(
            placeholder="Timeout Duration...",
            min_values=1,
            max_values=1,  # Only allow selecting one option
            options=[
                discord.SelectOption(label="30 Minutes", value=30),
                discord.SelectOption(label="1 Hour", value=60),
                discord.SelectOption(label="2 Hours", value=120),
                discord.SelectOption(label="3 Hours", value=180),
                discord.SelectOption(label="4 Hours", value=240),
                discord.SelectOption(label="6 Hours", value=360),
                discord.SelectOption(label="12 Hours", value=720),
                discord.SelectOption(label="1 Day", value=3600),
                discord.SelectOption(label="2 Days", value=7200),
                discord.SelectOption(label="3 Days", value=10800),
                discord.SelectOption(label="7 Days", value=25200),
                discord.SelectOption(label="14 Days", value=50400),
                discord.SelectOption(label="28 Days", value=108000)
            ]
        ))


    
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        global selected_value
        global member_global
        selected_value = int(select.values[0])
        try:
            timeout_duration = timedelta(minutes=selected_value)

            await member_global.timeout(timeout_duration)
            
            await interaction.response.send_message(f"{member_global.mention} was timed out. Duration: {selected_value}")
        except Exception as e:
            await interaction.response.send_message(f"Failed to timeout {member_global.mention}. Error: {e}")

@bot.tree.context_menu(name="Report Message")
async def report_message_context(interaction: discord.Interaction, message: discord.Message):
    global message_global, member_global
    message_global = message
    member_global=message.author.id
    modal = ReportMessageModal()
    await interaction.response.send_modal(modal)


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Tools(app_commands.Group):
    @app_commands.command(name="timestamp", description="Generate a Timestamp in a specific time.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(mode='Which Stamp Mode should be used', days='How many Days?', hours='How many Hours?', minutes='How many Minutes?', seconds='How many Seconds?')
    @app_commands.choices(
        mode=[
            app_commands.Choice(name='R - Relative Time', value='R'),
            app_commands.Choice(name='D - Long Date', value='D'),
            app_commands.Choice(name='d - Short Date', value='d'),
            app_commands.Choice(name='T - Long Time', value='T'),
            app_commands.Choice(name='t - Short Time', value='t'),
            app_commands.Choice(name='F - Long Date/Time', value='F'),   
            app_commands.Choice(name='f - Short Date/Time', value='f'),
        ]
    )
    async def timestamp(
        self, 
        interaction: discord.Interaction, 
        mode: app_commands.Choice[str], 
        days: typing.Optional[int] = 0, 
        hours: typing.Optional[int] = 0, 
        minutes: typing.Optional[int] = 0, 
        seconds: typing.Optional[int] = 0
    ):
        seconds_total_input = days * 86400 + hours * 3600 + minutes * 60 + seconds
        seconds_now = round(time.time())
        await interaction.response.send_message(f"<t:{seconds_now + seconds_total_input}:{mode.value}>")

    @app_commands.command(name="datestamp", description="Make a Discord Timestamp for a Date.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        mode='Which Stamp Mode should be used',
        month='What Month?',
        day='What Day?', 
        year='What Year?',
        hour='What Hour?',
        minute='What Minute?'
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(name='R - Relative Time', value='R'),
            app_commands.Choice(name='D - Long Date', value='D'),
            app_commands.Choice(name='d - Short Date', value='d'),
            app_commands.Choice(name='T - Long Time', value='T'),
            app_commands.Choice(name='t - Short Time', value='t'),
            app_commands.Choice(name='F - Long Date/Time', value='F'),   
            app_commands.Choice(name='f - Short Date/Time', value='f'),
        ]
    )
    @app_commands.choices(
        month=[
            app_commands.Choice(name='January', value='1'),
            app_commands.Choice(name='February', value='2'),
            app_commands.Choice(name='March', value='3'),
            app_commands.Choice(name='April', value='4'),
            app_commands.Choice(name='May', value='5'),
            app_commands.Choice(name='June', value='6'),   
            app_commands.Choice(name='July', value='7'),
            app_commands.Choice(name='August', value='8'),
            app_commands.Choice(name='September', value='9'),
            app_commands.Choice(name='October', value='10'),
            app_commands.Choice(name='November', value='11'),
            app_commands.Choice(name='December', value='12'),
        ]
    )
    async def dstamp(self, interaction: discord.Interaction, mode: app_commands.Choice[str], day: int, month: app_commands.Choice[str], year: int, hour: typing.Optional[int] = 0, minute: typing.Optional[int] = 0):
        await interaction.response.defer()
        total_years_1 = (year - 1970) * 365
        total_years_2 = (year - 1970) / 4
        total_years_3 = int(total_years_2) + total_years_1 
        def is_leap_year(year):
            if year % 4 == 0:
                if year % 100 == 0:
                    if year % 400 == 0:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False 
        
        if is_leap_year(year):
            month_seconds=[0, 2678400, 5184000, 7862400, 10454400, 13132800, 15724800, 18403200, 21081600, 23673600, 26352000, 28944000]
            one_day = 86400
        else:
            month_seconds=[0, 2678400, 5097600, 7776000, 10368000, 13046400, 15638400, 18316800, 20995200, 23587200, 26265600, 28857600]
            one_day = 0

        total_seconds = total_years_3 * 86400 + day * 86400 + hour * 3600 + minute * 60 + month_seconds[int(month.value) - 1] - 3600 - one_day
        await interaction.followup.send(f"<t:{total_seconds}:{mode.value}>")



bot.tree.add_command(Tools(name="tool", description="A collection of tools"))

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)

class Random(app_commands.Group):
    @app_commands.command(name="number", description="Get a Random Number")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(starting_number="The Range from this Number")
    @app_commands.describe(ending_number="The Range to this Number")
    async def randomnumber(self, interaction: discord.Interaction, starting_number: int, ending_number: int):
            randomnumber=random.randint(starting_number, ending_number)
            embed=discord.Embed(title=f"{randomnumber} was chosen", description=f"{randomnumber} was Randomly picked.")
            await interaction.response.send_message(embed=embed)
    



bot.tree.add_command(Random(name="random", description="Some Random Generators"))

@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=False)
class Set(app_commands.Group):
    @app_commands.command(name="log-channel", description="Set the Channel for Reports using the Context Menu")
    async def setreportchannel(self, interaction: discord.Interaction):
        await interaction.response.defer()
        def set_channelid(data):
            for user in data['servers']:
                if user['serverid'] == interaction.guild_id:
                    if user['channelid'] == interaction.channel_id:
                        response_for_bot = "You have already set this Channel as the Report Channel"
                        return response_for_bot
                    else:
                        keys_list = list(data['servers'])
                        find_index = keys_list.index(user)
                        replace_channel = {"serverid": interaction.guild_id, "channelid": interaction.channel_id}
                        data['servers'][find_index] = replace_channel
                        with open('data.json', 'w') as file:
                            json.dump(data, file, indent=4)
                        response_for_bot = f"You set {interaction.channel_id} as the Report Channel for {interaction.guild_id}"
                        return response_for_bot
            new_channel = {"serverid": interaction.guild_id, "channelid": interaction.channel_id}
            data['servers'].append(new_channel)
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            response_for_bot = f"You set {interaction.channel_id} as the Report Channel for {interaction.guild_id}"
            return response_for_bot
        
        with open('data.json', 'r') as file:
            await interaction.followup.send(set_channelid(data = json.load(file)))
    

bot.tree.add_command(Set(name="set", description="Set a Channel for specific things"))

@bot.event
async def on_message(message):
    if "cdn.discordapp.com/emojis/" in str(message.content):
       await message.delete()
       await message.channel.send("Don't use fake Nitro!")
    if "cdn.discordapp.com/sticker/" in str(message.content):
       await message.delete()
       await message.channel.send("Don't use fake Nitro!")
    if "media.discordapp.net/stickers/" in str(message.content):
       await message.delete()
       await message.channel.send("Don't use fake Nitro!")
    if "media.discordapp.net/emojis/" in str(message.content):
       await message.delete()
       await message.channel.send("Don't use fake Nitro!")
    if "good bot" in str(message.content):
        await message.channel.send("beep boop.")

@bot.tree.command(name="commands", description="A list of all of the commands and what they do.")
@app_commands.describe(command="for which Command do you want more information?")
async def commandslist(interaciton: discord.Interaction, command: str):
    if command == "timestamp" or command == "/timestamp":
        embed = discord.Embed("timestamp (/timestamp)", description="With this Command, you can create a Discord Timestamp using the Bot, so there's no need to visit external websites. A Discord Timestamp can show how long is left until that event and updates the time remaining of how much time is actually remaining. It automatically adjusts to the Time Zone you have while for someone in a different Time Zone it also is changed for them. \n You will have multiple command options. \n mode: will choose the mode. There are many different Options, for example R (Relative Time) shows how much time is left until that event. F (Long Date) will show the date and hours/minutes when that even is happening. \n days, hours, minutes, seconds They are all basically the same, enter the number of days, hours, minutes or seconds until the event and hit enter! If you leave any of those options empty, they will automatically be zero, meaning that they won't be calculated, so you don't have to worry about that")
        embed.add_field(name="", value="More Info at https://github.com/Tino-Botted/Botted/wiki/Features-and-Commands#timestamp")
        await interaciton.response.send_message(embed=embed)

@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=False)
@bot.tree.context_menu(name = "Delete")
@app_commands.default_permissions(manage_expressions=True)
async def SaveMessage(interaction : discord.Interaction, message: discord.Message):
    def find_channelid_for_report(data):
        for user in data['servers']:
            if user['serverid'] == interaction.guild_id:
                return user['channelid']
        return None

    with open('data.json', 'r') as file:
        channel = bot.get_channel(find_channelid_for_report(data = json.load(file)))
    await interaction.response.send_message("The Message has successfully been Deleted.", ephemeral=True)
    await channel.send(f"""{interaction.user.mention} deleted "{message.content}" from {message.author} from https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}""")
    await message.delete()




class DropdownSettings(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Ephermal Messages (Only visible to you)", value="ephermal_message"),
            discord.SelectOption(label="Examples", value="definitionexamples")
        ]
        super().__init__(placeholder="Choose a setting...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]

        with open('usersettings.json', 'r') as file:
            json_settings = (json.load(file))

        ephermal_messages = json_settings[0]["users"][0][str(interaction.user.id)][0]["ephermal_message"]

        if ephermal_messages == "True":
            ephermal_messages2 = "On."
        else:
            ephermal_messages2 = "Off."

        examples = json_settings[0]["users"][0][str(interaction.user.id)][0]["examples"]

        if examples == "True":
            examples = "On."
        else:
            examples = "Off."


        if selected_value == "definitionexamples":
            option = "Examples"
        elif selected_value == "ephermal_message":
            option = "Ephermal Messages (only visible to you messages)"

        select = EphermalMessages()
        view = discord.ui.View()
        view.add_item(select)

        if ephermal_messages2 == "On.":
            on_off_color = discord.Color.green()
        else:
            on_off_color = discord.Color.red()

        if examples == "On.":
            on_off_color = discord.Color.green()
        else:
            on_off_color = discord.Color.red()

        embed=discord.Embed(title="Ephermal Messages (only visible to you messages)", description=f"{option} are currently set to {ephermal_messages2}", color=on_off_color)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
       
class EphermalMessages(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Enable", style=discord.ButtonStyle.green)
    async def ephermal_messages_on(self, interaction: discord.Interaction):
        with open('usersettings.json', 'r') as file:
            json_settings = (json.load(file))

        json_settings[0]["users"][0][str(interaction.user.id)][0]["ephermal_message"] = selected_value

        with open('usersettings.json', 'w') as file:
            json.dump(json_settings, file, indent=4)
        
        interaction.response.send_message(f"Successfully turned Ephermal Messages (Only visible to you messages) to {selected_value}")
    
    @discord.ui.button(label="Enable", style=discord.ButtonStyle.red)
    async def ephermal_messages_off(self, interaction: discord.Interaction):
        with open('usersettings.json', 'r') as file:
            json_settings = (json.load(file))

        json_settings[0]["users"][0][str(interaction.user.id)][0]["ephermal_message"] = selected_value

        with open('usersettings.json', 'w') as file:
            json.dump(json_settings, file, indent=4)
        
        interaction.response.send_message(f"Successfully turned Ephermal Messages (Only visible to you messages) to {selected_value}")

class DictionaryButtons(discord.ui.View):
    def __init__(self, word):
        self.savedword = word
        super().__init__()

    @discord.ui.button(label="More Definitions", style=discord.ButtonStyle.primary)
    async def moredefinitions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled=True
        word = self.savedword
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as response:
                html = await response.json()

                worddata = html[:11]
                
        newlist = []
        definitions = []
        synonymslist = []
        antonymslist = []

        for only_definitions in worddata[0]["meanings"][0]["definitions"]:
            newlist.append(only_definitions['definition'])    


        for index, definition in enumerate(newlist):
            definitions.append(f"{index}. {definition}")

        if worddata[0]["meanings"][0]["definitions"][0]["synonyms"] == []:
            synonymslist.append("There are no synonyms for this word.")
        else:
            for synonyms in worddata[0]["meanings"][0]["definitions"][0]["synonyms"]:
                synonymslist.append(synonyms)

        if worddata[0]["meanings"][0]["definitions"][0]["synonyms"] == []:
            antonymslist.append("There are no antonyms for this word.")
        else:
            for antonyms in worddata[0]["meanings"][0]["definitions"][0]["antonyms"]:
                antonymslist.append(antonyms)

        definition_and_synonyms = '\n'.join(definitions)
        embed = discord.Embed(title=f"""{word} - More Definitions""", description=f"""{definition_and_synonyms}""")
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Detailed Definition", style=discord.ButtonStyle.primary)
    async def noun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled=True
        word = self.savedword
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as response:
                html = await response.json()

                worddata = html[:11]
        
            worddatalength = len(worddata[0]["meanings"])
            x_times = 0
            partofspeechlist = []

            while x_times <= worddatalength:
                for part in worddata[0]["meanings"][x_times - 1]["partOfSpeech"]:
                    partofspeechlist.append(part)
                x_times = x_times + 1
                partofspeechlist.append(", ")
            
            partofspeechlist.pop()

            if partofspeechlist[0] == "a" or partofspeechlist[0] == "e" or partofspeechlist[0] == "i" or partofspeechlist[0] == "o" or partofspeechlist[0] == "u":
                an_check = "n"
            else:
                an_check = ""

            embed = discord.Embed(title=f"\"{word}\" - Detailed Definitions", description=f"\"{word}\" can be used as a{an_check} {"".join(partofspeechlist)}\n\n")
            await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Settings", style=discord.ButtonStyle.primary)
    async def settings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = DropdownSettings()
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message("Choose one of the avaible settings:", ephemeral=True, view=view)



@bot.tree.command(name="dictionary", description="Define a Word and more using https://dictionaryapi.dev/")
@app_commands.describe(word="Which word do you want to know more about?")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def dictionarycommand(interaction: discord.Interaction, word: str):
    await interaction.response.defer()
    try:
        if " " not in word:
            button_class = DictionaryButtons(word)
            button_class.saveword = word
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as response:
                    html = await response.json()
                    worddata = html[:11]

            synonymslist = []
            antonymslist = []
            if worddata[0]["phonetics"][0]["text"] == []: 
                phoneticslist = "There are no phonetics for this word."
            else: 
                phoneticslist = worddata[0]["phonetics"][0]["text"]

            if worddata[0]["meanings"][0]["definitions"][0]["synonyms"] == []:
                synonymslist.append("There are no synonyms for this word.")
            else:
                for synonyms in worddata[0]["meanings"][0]["definitions"][0]["synonyms"]:
                    synonymslist.append(synonyms)

            if worddata[0]["meanings"][0]["definitions"][0]["antonyms"] == []:
                antonymslist.append("There are no antonyms for this word.")
            else:
                for antonyms in worddata[0]["meanings"][0]["definitions"][0]["antonyms"]:
                    antonymslist.append(antonyms)

            embed = discord.Embed(title=f""""{worddata[0]["word"]}" - Dictionary""", description=f"Definition: \n{worddata[0]["meanings"][0]["definitions"][0]["definition"]} \n\nsynonyms: {', '.join(synonymslist)} \nantonyms: {', '.join(antonymslist)} \nphonetics: {str(phoneticslist)} \nPart of Speech: {worddata[0]["meanings"][0]["partOfSpeech"]}", color=discord.Color.blue())
            await interaction.followup.send(embed=embed, view=DictionaryButtons(word))
        else:
            await interaction.response.send_message(f"""Do not use spaces in the option "word". You have entered: "{word}" """)
    except Exception as e:
        error_embed = discord.Embed(title=f""""{word}" - Error""", description=f"An Error occured while trying to find that word. There can be multiple reasons for this. Here are some:\n - The Word might not be in the dictionary, so the word can't be found. Make sure you entered the word without special characters and that it is an english word. \n - The API didn't respond. maybe the api im using doesn't respond and just gives a 404 Error. This doesn't usually happen, but you can check for yourself by going to https://api.dictionaryapi.dev/api/v2/entries/en/{word} but if it shows you can try again. \n - It is possbile that you're maybe trying to execute the command while I am testing stuff. Try again in a few hours or tomorrow.")
        error_embed.add_field(name="", value="If you think that is not the case, please ask for help in my server (<https://discord.gg/hzzCSPKbmV>)")
        await interaction.followup.send(embed=error_embed)
        print(e)


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class WordCmds(app_commands.Group):
    @app_commands.command(name="character-counter", description="Count the amount of characters, words and sentences in a text")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def charcount(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        character_count = len(text)
        no_space = len(text.replace(" ", ""))
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]', text)) - 1
        embed = discord.Embed(title="Character Count", description=f"Total Characters: {character_count} (excluding spaces: {no_space})\nTotal Words: {word_count}\n Total Sentences: {sentence_count}")
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="word-counter", description="Count how often a word is in a text")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(word="Which Word to search for?", text="The Text you want to search the word in.")
    async def wordcounter(self, interaction: discord.Interaction, word: str, text: str):
        embed=discord.Embed(title=f"{word} - {text.count(word)} times", description=f"Text:\n{text}")
        await interaction.response.send_message(embed=embed)

bot.tree.add_command(WordCmds(name="text", description="Commands that have something to do with Words"))

@bot.tree.context_menu(name="Translate")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def translate(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()
    if message.content != None:
        text = message.content
        while "`" in text:
            text.replace("`", "")
        translator = GoogleTranslator(source="auto", target="en")
        result = translator.translate(text)
        try:
            language_detected = detect(text)
        except Exception as e:
            language_detected = "Unknown Language"
            print(e)
        LANGUAGES = {'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'ca': 'Catalan', 
             'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 
             'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 
             'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 
             'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'kn': 'Kannada', 'ko': 'Korean', 
             'lt': 'Lithuanian', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 
             'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi', 'pl': 'Polish', 
             'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 
             'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil', 
             'te': 'Telugu', 'th': 'Thai', 'tl': 'Tagalog', 'tr': 'Turkish', 'uk': 'Ukrainian', 
             'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)'}
        embed = discord.Embed(title="Translator", description=f"From {LANGUAGES.get(language_detected, "Unknown Language")}\n```\n{text}```\nTo English\n```\n{result}```")
        if "`" in message.content:
            embed.set_footer(text="Google Translate - deep-translate | any ` have been automatically removed.")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.response.send_message("Please provide a valid message.")


@bot.tree.command(name="website", description="Get an Image of a webiste")
@app_commands.describe(url="What Website do you want to get a screenshot of?")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def websitecommand(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    try:
        if " " not in url:
            if "." in url:
                params = urlencode(dict(access_key="bfb8fc8b6fdc4a0d916d69cf8e20908f",
                                        url=url))
                urlretrieve("https://api.apiflash.com/v1/urltoimage?" + params, "screenshot.jpeg")

                file = discord.File("screenshot.jpeg", filename="screenshot.jpeg")
                embed = discord.Embed(title=f"{url} - Screenshot")
                await interaction.followup.send(file=file, embed=embed)
            else:
                await interaction.followup.send("Please use a dot (.) in your message. Use a valid website")
        else:
            await interaction.followup.send("Please do not have any spaces in your url. Use a valid url.")
    except Exception as e:
        errorembed = discord.Embed(title="That didn't work", description=f"Uh oh, that didnt wrok. Seems like there was an error. Please check if your url is correct (you have entered {url}) or try again **1 time**. Dont try again too often or the API will get rate limited and wont work anymore. Which can also be the reason youre getting this error. more help in my discord server - https://discord.gg/hzzCSPKbmV")
        await interaction.followup.send(embed=errorembed)
        print(e)

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Colorcodes(app_commands.Group):
    @app_commands.command(name="hex-code", description="Show what the color of a hex code looks like")
    @app_commands.describe(colorcode="Enter a Hex Code you want to know more of. Hex Codes have either 4 or 6 characters in length")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def hexcode(self, interaction: discord.Interaction, colorcode:str):
        colorcodeletterlist = []
        for colorcode_letters in colorcode:
            colorcodeletterlist.append(colorcode_letters)
        if "#" in colorcodeletterlist:
            colorcodeletterlist.pop(0)
        async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.thecolorapi.com/id?hex={"".join(colorcodeletterlist)}") as response:
                    thecolorapidata = await response.json()

        if len(colorcodeletterlist) == 4 or len(colorcodeletterlist) == 6:
            try:
                embed=discord.Embed(title=f"{thecolorapidata["hex"]["value"]} - {thecolorapidata["name"]["value"]}", description=f"\nColor Name: {thecolorapidata["name"]["value"]} (Distance to next named color: {thecolorapidata["name"]["distance"]})\nNearest Named Color: {thecolorapidata["name"]["closest_named_hex"]}\n\nhex: {thecolorapidata["hex"]["value"]}\nrgb: {thecolorapidata["rgb"]["r"]}, {thecolorapidata["rgb"]["g"]}, {thecolorapidata["rgb"]["b"]}\nhsl: {thecolorapidata["hsl"]["h"]}, {thecolorapidata["hsl"]["s"]}, {thecolorapidata["hsl"]["l"]}\nhsv: {thecolorapidata["hsv"]["h"]}, {thecolorapidata["hsv"]["s"]}, {thecolorapidata["hsv"]["v"]}\n\nFraction:\nrgb: {thecolorapidata["rgb"]["fraction"]["r"]}, {thecolorapidata["rgb"]["fraction"]["g"]}, {thecolorapidata["rgb"]["fraction"]["b"]}\nhsl: {thecolorapidata["hsl"]["fraction"]["h"]}, {thecolorapidata["hsl"]["fraction"]["s"]}, {thecolorapidata["hsl"]["fraction"]["l"]}\nhsl: {thecolorapidata["hsv"]["fraction"]["h"]}, {thecolorapidata["hsv"]["fraction"]["s"]}, {thecolorapidata["hsv"]["fraction"]["v"]}")
                embed.set_thumbnail(url=f"https://dummyimage.com/1000x1000/{thecolorapidata["hex"]["clean"]}/ffffff.png&text=+")
                await interaction.response.send_message(embed=embed)
            except Exception:
                try:
                    if thecolorapidata["code"] == 400:
                        await interaction.response.send_message("Seems like you have entered something invalid. The API couldn't understand the colorcode you wanted.")
                except Exception:
                    await interaction.response.send_message("Sorry, but an unexpected Error happened. Please try again or try again later.")
        else:
            await interaction.response.send_message("You didn't enter a valid hexcode. Hexcodes have either 4 or 6 characters.")

    @app_commands.command(name="rgb-code", description="Show what the color of a rgb code looks like")
    @app_commands.describe(r="Enter the R Value you want to know more of. Rgb codes have 3 numbers that can go up to 255", g="Enter the G Value you want to know more of. Rgb codes have 3 numbers that can go up to 255", b="Enter the B Value you want to know more of. Rgb codes have 3 numbers that can go up to 255")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def rgbcode(self, interaction: discord.Interaction, r:int, g: int, b: int):
        async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.thecolorapi.com/id?rgb={r},{g},{b}") as response:
                    thecolorapidata = await response.json()



        if r < 255 or r > 0 or g < 255 or g > 0 or b < 255 or b > 0:
            try:
                embed=discord.Embed(title=f"{thecolorapidata["rgb"]["r"]}, {thecolorapidata["rgb"]["g"]}, {thecolorapidata["rgb"]["b"]} - {thecolorapidata["name"]["value"]}", description=f"\nColor Name: {thecolorapidata["name"]["value"]} (Distance to next named color: {thecolorapidata["name"]["distance"]})\nNearest Named Color: {thecolorapidata["name"]["closest_named_hex"]}\n\nhex: {thecolorapidata["hex"]["value"]}\nrgb: {thecolorapidata["rgb"]["r"]}, {thecolorapidata["rgb"]["g"]}, {thecolorapidata["rgb"]["b"]}\nhsl: {thecolorapidata["hsl"]["h"]}, {thecolorapidata["hsl"]["s"]}, {thecolorapidata["hsl"]["l"]}\nhsv: {thecolorapidata["hsv"]["h"]}, {thecolorapidata["hsv"]["s"]}, {thecolorapidata["hsv"]["v"]}\n\nFraction:\nrgb: {thecolorapidata["rgb"]["fraction"]["r"]}, {thecolorapidata["rgb"]["fraction"]["g"]}, {thecolorapidata["rgb"]["fraction"]["b"]}\nhsl: {thecolorapidata["hsl"]["fraction"]["h"]}, {thecolorapidata["hsl"]["fraction"]["s"]}, {thecolorapidata["hsl"]["fraction"]["l"]}\nhsl: {thecolorapidata["hsv"]["fraction"]["h"]}, {thecolorapidata["hsv"]["fraction"]["s"]}, {thecolorapidata["hsv"]["fraction"]["v"]}")
                embed.set_thumbnail(url=f"https://dummyimage.com/1000x1000/{thecolorapidata["hex"]["clean"]}/ffffff.png&text=+")
                await interaction.response.send_message(embed=embed)
            except Exception:
                try:
                    if thecolorapidata["code"] == 400:
                        await interaction.response.send_message("Seems like you have entered something invalid. The API couldn't understand the colorcode you wanted.")
                except Exception:
                    await interaction.response.send_message("Sorry, but an unexpected Error happened. Please try again or try again later.")
        else:
            await interaction.response.send_message("You didn't enter a valid rgb colorcode. a valid colorcode can only go up to 255 and has to be higher than 0.")



bot.tree.add_command(Colorcodes(name="colorcode", description="Commands about Colorcodes"))

bot.run()