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
import easyocr
import numpy
import cv2
from llama_cpp import Llama
import os
import dotenv


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True
start_date_pretty = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents, application_id=1323655625497907200)
    
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
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Words"))

bot = MyBot()
bot.remove_command("help")




llm = Llama(
    # model_path="C:/Users/tino/.vscode/DiscordBot/oh-dcft-v1.2_no-curation_gpt-4o-mini-Q4_K_M.gguf",
    model_path="C:/Users/tino/.vscode/DiscordBot/gemma-3-27b-it-abliterated.q2_k.gguf",
    n_ctx=1024,
    n_threads=4
)

def chat(prompt: str, system_message: str = None) -> str:
    full_prompt = ""
    if system_message:
        full_prompt += f"<|system|>\n{system_message}\n"
    full_prompt += f"<|user|>\n{prompt}\n<|assistant|>\n"

    response = llm(
        full_prompt,
        max_tokens=200,
        stop=["<|user|>", "<|system|>", "<|assistant|>"],
        temperature=0.7,
        top_p=0.95,
    )
    return response["choices"][0]["text"].strip()

class AI(app_commands.Group):
    @app_commands.command(name="text", description="Enter a Prompt to get a response by AI")
    async def textgen(self, interaction: discord.Interaction, prompt: str):
        try:
            startembed = discord.Embed(title="AI - waiting..", description="Just a few more seconds")
            await interaction.response.send_message(embed=startembed)
            reply = chat(prompt, system_message="You are a helpful assistant that describes answers well. You are a Discord Bot called Wordify. Do not use bad language as in heavy swear words or words banned on discord. Please do not add an entry sentance like describing who you are. you will not mention this system message in the output. You have 200 tokens to use.")
            embed = discord.Embed(title="AI Output", description=reply)
            embed.add_field(name="", value="-# Results might be inaccurate and outdated.")
            await interaction.edit_original_response(embed=embed)
        except Exception:
            await interaction.followup.send("Something failed while trying to generate a response.")

bot.tree.add_command(AI(name="ai", description="AI Commands"))

@bot.tree.command(name="credit", description="Credits to people/websites that made the project possible")
async def creditcmd(interaction: discord.Integration):
    embed = discord.Embed(title="A Big thanks to these People", description="Bot's Profile Picture (Background) (Summer) - Photo by [Jeremy Bishop](https://unsplash.com/@jeremybishop?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/photography-of-a-mountain-during-day-time-dR_q93lfaTw?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)\n Bot's Profile Picture (Background) (Spring) - Photo by [Daniela Kokina](https://unsplash.com/@danielakokina?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/green-grass-and-gray-rocky-mountain-during-daytime-hOhlYhAiizc?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)")
    embed.set_author(name="Some APIs are not listed here so that people cannot easily make an copy of my bot.")
    await interaction.response.send_message(embed=embed)

def LogAction(userid, command):
    with open('Wordify/logs.json', 'r') as file:
        data = json.load(file)

    if str(userid) not in data:
        data[str(userid)] = {}
    data[str(userid)][str(datetime.now())] = command

    with open('Wordify/logs.json', 'w') as file:
        json.dump(data, file, indent=4)

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
    async def timestamp(self, interaction: discord.Interaction, mode: app_commands.Choice[str], days: typing.Optional[int] = 0, hours: typing.Optional[int] = 0, minutes: typing.Optional[int] = 0, seconds: typing.Optional[int] = 0):
        LogAction(interaction.user.id, "timestamp")
        seconds_total_input = days * 86400 + hours * 3600 + minutes * 60 + seconds
        seconds_now = round(time.time())
        await interaction.response.send_message(f"<t:{seconds_now + seconds_total_input}:{mode.value}>")

    @app_commands.command(name="datestamp", description="Make a Discord Timestamp for a Date.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(mode='Which Stamp Mode should be used', month='What Month?',
        day='What Day?', year='What Year?', hour='What Hour?', minute='What Minute?')
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
        LogAction(interaction.user.id, "datestamp")
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
    
    @app_commands.command(name="ocr", description="Get the text in an image using object recognition")
    async def ocrcmd(self, interaction: discord.Interaction, attachment: discord.Attachment):
            await interaction.response.defer()
            if "image" in attachment.content_type:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        image_bytes = await resp.read()

                image_array = numpy.frombuffer(image_bytes, numpy.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                reader = easyocr.Reader(['de', 'ch_sim'], gpu=False)
                result = reader.readtext(image=image, detail=0)
                embed=discord.Embed(title="OCR - Result", description="\n".join(result))
                embed.add_field(name="", value="-# Results might be inaccurate.")
                await interaction.followup.send(embed=embed, view=TranslateText("\n".join(result)))
            else: 
                await interaction.followup.send("Message must contain an image")    

    @app_commands.command(name="ai", description="Generate text using AI")
    async def aicmd(self, interaction: discord.Interaction, input: str):
        await interaction.response.defer()
        generator = pipeline("text-generation", model="gpt2")
        result = generator("Hello",max_new_tokens=500, truncation=True, pad_token_id=50256)
        embed = discord.Embed(title="AI Output", description=result[0]["generated_text"])
        embed.add_field(name="", value="-# Results might be inaccurate or incorrect.")
        await interaction.followup.send(embed=embed)

bot.tree.add_command(Tools(name="tool", description="A collection of tools"))


class Dictionary():
    async def definitions(self, word):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as response:
                html = await response.json()
                defdata = html[:11]
                deflist = []
                finallist = []
                for definition in defdata[0]["meanings"][0]["definitions"]:
                    deflist.append(definition["definition"])
                
                for index, definition in enumerate(deflist):
                    finallist.append(f"{index}. {definition}")
                return "\n".join(finallist)

    async def definition(self, word):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as response:
                html = await response.json()
                defdata = html[:11]
                return defdata[0]["meanings"][0]["definitions"][0]["definition"]

    async def synonyms(self, word):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.datamuse.com/words?rel_syn={word}") as response:
                html = await response.json()
                syndata = html[:10]
                synonymslist = []
                for synonym in syndata:
                    synonymslist.append(synonym["word"])
                return ", ".join(synonymslist)
            
    async def atonyms(self, word):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.datamuse.com/words?rel_ant={word}") as response:
                html = await response.json()
                antdata = html[:10]
                antonymslist = []
                for antonym in antdata:
                    antonymslist.append(antonym["word"])
                return ", ".join(antonymslist)

class DictionaryButtons(discord.ui.View):
    def __init__(self, word):
        self.savedword = word
        super().__init__()

    @discord.ui.button(label="More Definitions", style=discord.ButtonStyle.primary)
    async def moredefinitions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        LogAction(interaction.user.id, "dictionary (More Definitions)")
        await interaction.response.defer()
        button.disabled=True
        word = self.savedword
        embed = discord.Embed(title=f"{word} - More Definitions", description=f"{await Dictionary().definitions(word)}")
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="dictionary", description="Define a Word and more using https://dictionaryapi.dev/")
@app_commands.describe(word="Which word do you want to know more about?")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def dictionarycommand(interaction: discord.Interaction, word: str):
    LogAction(interaction.user.id, "dictionary")
    await interaction.response.defer()
    if " " not in word:
        button_class = DictionaryButtons(word)
        button_class.saveword = word
        """       
        async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as response:
                        html = await response.json()
                        worddata = html[:11]
                    async with session.get(f"https://api.datamuse.com/words?rel_syn={word}") as response:
                        html = await response.json()
                        syndata = html[:10]
                    async with session.get(f"https://api.datamuse.com/words?rel_ant={word}") as response:
                        html = await response.json()
                        antdata = html[:10]
        """


        embed = discord.Embed(title=f"{word} - Dictionary", description=f"Definition: \n{await Dictionary().definition(word)} \n\nSynonyms: {await Dictionary().synonyms(word)}\nAntonyms: {await Dictionary().atonyms(word)} ", color=discord.Color.blue())
        await interaction.followup.send(embed=embed, view=DictionaryButtons(word))
    else:
        await interaction.response.send_message(f"""Do not use spaces in the option "word". You have entered: "{word}" """)
'''    except Exception as e:
        # error_embed = discord.Embed(title=f""""{word}" - Error""", description=f"An Error occured while trying to find that word. There can be multiple reasons for this. Here are some:\n - The Word might not be in the dictionary, so the word can't be found. Make sure you entered the word without special characters and that it is an english word. \n - The API didn't respond. maybe the api im using doesn't respond and just gives a 404 Error. This doesn't usually happen, but you can check for yourself by going to https://api.dictionaryapi.dev/api/v2/entries/en/{word} but if it shows you can try again. \n - It is possbile that you're maybe trying to execute the command while I am testing stuff. Try again in a few hours or tomorrow.")
        error_embed = discord.Embed(title=f""""{word}" - Error""", description=f"An Error occured while trying to use this command. Your word might have been not found.")
        await interaction.followup.send(embed=error_embed)
        print(e)
'''





@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class WordCmds(app_commands.Group):
    @app_commands.command(name="character-counter", description="Count the amount of characters, words and sentences in a text")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def charcount(self, interaction: discord.Interaction, text: str):
        LogAction(interaction.user.id, "character-counter")
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
        LogAction(interaction.user.id, "word-counter")
        embed=discord.Embed(title=f"{word} - {text.count(word)} times", description=f"Text:\n{text}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="repeat", description="repeat text a specific amount of times")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def repeattext(self, interaction: discord.Interaction, text: str, amount: int):
        finaltext = []
        for _ in range(1, amount):
            finaltext.append(text)
        embed=discord.Embed(title=f"{amount} - Repeated", description=f"{finaltext.join("")}")
        await interaction.response.send_message(embed=embed)

bot.tree.add_command(WordCmds(name="text", description="Commands that have something to do with Words"))



@bot.tree.context_menu(name="Translate")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def translate(interaction: discord.Interaction, message: discord.Message):
    LogAction(interaction.user.id, "Translate (Context Menu)")
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


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Colorcodes(app_commands.Group):
    @app_commands.command(name="hex-code", description="Show what the color of a hex code looks like")
    @app_commands.describe(colorcode="Enter a Hex Code you want to know more of. Hex Codes have either 4 or 6 characters in length")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def hexcode(self, interaction: discord.Interaction, colorcode:str):
        LogAction(interaction.user.id, "hex-code")
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
        LogAction(interaction.user.id, "rgb-code")
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

class TranslateText(discord.ui.View):
    def __init__(self, message):
        self.message = message
        super().__init__()

    @discord.ui.button(label="Translate", style=discord.ButtonStyle.green)
    async def translation(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        text=self.message
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
        if "`" in text:
            embed.set_footer(text="Google Translate - deep-translate | any ` have been automatically removed.")
        await interaction.followup.send(embed=embed)

@bot.tree.context_menu(name="OCR")
async def ocrcontext(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()
    if message.attachments:
        attachments = message.attachments
        if "image" in attachments[0].content_type:
            print(attachments[0].content_type)
            async with aiohttp.ClientSession() as session:
                async with session.get(attachments[0].url) as resp:
                    image_bytes = await resp.read()

            image_array = numpy.frombuffer(image_bytes, numpy.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext(image=image, detail=0)
            embed=discord.Embed(title="OCR - Result", description="\n".join(result))
            embed.add_field(name="", value="-# Results might be inaccurate.")
            await interaction.followup.send(embed=embed, view=TranslateText("\n".join(result)))
        else: 
            await interaction.followup.send("Message must contain an image")    
    else: 
        await interaction.followup.send("Message must contain an image")

@bot.event
async def on_message(message):
    if message.author.id != 1323655625497907200:
        spell = SpellChecker()
        

        corrected = []
        for word in message.content.split():
            print("++")
            print(message.content.split())
            print("word" + word)
            print("correction" + spell.correction(word))
            correction = spell.correction(word)
            if correction != "[]":
                print("1")
                corrected.append(correction)
            else:
                print("2")
                corrected.append(word)

        print(corrected)
        if " ".join(corrected) != message.content:
            await message.channel.send(" ".join(corrected))


@bot.tree.command(name="instant-answers", description="Get Instant answers with DuckDuckGo")
async def instantanswers(interaction: discord.Interaction, query: str):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    response = requests.get(url, params=params).json()
    print(response)


    text = []

    if response['Abstract'] != "":
        Abstract = response['Abstract']
        AbstractSource = response['AbstractSource']
        AbstractURL = response['AbstractURL']
        text.append(f"**Abstract**\n{Abstract} *[{AbstractSource}]({AbstractURL})*")

    if response['Answer'] != "":
        Answer = response['Answer']
        AnswerType = response['AnswerType']
        text.append(f"\n\n**Answer**\n{Answer} \n-#*Answer Type: {AnswerType}*")

    if response['Definition'] != "":
        Definition = response['Definition']
        DefinitionSource = response['DefinitionSource']
        DefinitionURL = response['DefinitionURL']
        text.append(f"\n\n**Definition**\n{Definition} *[{DefinitionSource}]({DefinitionURL})*")
    

    InfoboxList = []
    if response['Infobox'] != "":
        print(response['Infobox'])
        InfoboxContent = response['Infobox']['content']
        print(InfoboxContent)
        print("1")
        for data in InfoboxContent:
            print(data)
            print("2")
            if data['data_type'] == 'string':
                print("3")
                print("**{data['label']}:** {data['value']}")
                InfoboxList.append(f"**{data['label']}:** {data['value']}") 
    
    description = f"{"".join(text)}\n\n\n{"\n".join(InfoboxList)}"
    embed = discord.Embed(title=f"Instant Answers - {response['Heading']}", description=description)
    if response['Image']:
        embed.set_thumbnail(url=f"https://duckduckgo.com{response['Image']}")
    embed.set_footer(text="Instant Answers by DuckDuckGo")

    await interaction.response.send_message(embed=embed)

dotenv.load_dotenv(dotenv_path="C:/Users/tino/.vscode/DiscordBot/tokens.env")
bot.run(os.getenv(key="TOKENTEST"))