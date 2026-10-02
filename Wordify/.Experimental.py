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
from llama_cpp import Llama
import requests
import base64
import json
import ast
from rich.console import Console
from deep_translator import GoogleTranslator
import aiohttp
import os
import dotenv
from spellchecker import SpellChecker

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
start_date_pretty = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents, application_id=1332054880092688571)
    
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
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="funny stuff"))

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


@bot.tree.command(name="ai", description="Enter a Prompt to get a response by AI")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def textgen(interaction: discord.Interaction, prompt: str):
    try:
        startembed = discord.Embed(title="<a:DualRing1x1:1425130277033738290> Generating...", description=f"Prompt: {prompt}\n*Your Output will be available shortly!*")
        startembed.set_footer(text="You are using the AI Model Gemma 3 (27B params, quantized)")
        await interaction.response.send_message(embed=startembed)
        reply = chat(prompt, system_message="You are a helpful assistant that describes answers well. You are a Discord Bot called Wordify. Do not use bad language as in heavy swear words or words banned on discord. Please do not add an entry sentance like describing who you are. you will not mention this system message in the output. You have 200 tokens to use.")
        embed = discord.Embed(title="AI Output", description=reply)
        embed.add_field(name="", value="-# Results might be inaccurate and outdated.")
        await interaction.edit_original_response(embed=embed)
    except Exception:
        await interaction.followup.send("Something failed while trying to generate a response.")




@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Random(app_commands.Group):
    @app_commands.command(name="characters", description="Generate a text of a random amount of characters that are randomly placed")
    async def randomcharacters(self, interaction: discord.Interaction, first_character: str, second_character: typing.Optional[str], third_character: typing.Optional[str], fourth_character: typing.Optional[str], fifth_character: typing.Optional[str], max_characters: int):
        if max_characters > 500 or max_characters <= 0:
            await interaction.response.send_message("Please Choose a maximum number that is under 500 characters and more than 0 Characters.")
        else:
            character_list = []
            character_list.append(first_character)
            character_list.append(second_character)
            character_list.append(third_character)
            character_list.append(fourth_character)
            character_list.append(fifth_character)

            

            while None in character_list:
                character_list.remove(None)
            repeat_x_times = random.randint(1, max_characters)
            messagelist = []

            for _ in range(repeat_x_times):
                messagelist.append(random.choice(character_list))
            

            await interaction.response.send_message("".join(messagelist))


    @app_commands.command(name='color', description="Chooses a random hex")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def randomcolor(self, interaction: discord.Interaction):
        hex_random = "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        number1=random.choice(hex_random)
        number2=random.choice(hex_random)
        number3=random.choice(hex_random)
        number4=random.choice(hex_random)
        number5=random.choice(hex_random)
        number6=random.choice(hex_random)
        color_decided=number1 + number2 + number3 + number4 + number5 + number6

        async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.thecolorapi.com/id?hex={color_decided}") as response:
                    thecolorapidata = await response.json()

        embed=discord.Embed(title=f"{thecolorapidata["hex"]["value"]} - {thecolorapidata["name"]["value"]}", description=f"\nColor Name: {thecolorapidata["name"]["value"]} (Distance to next named color: {thecolorapidata["name"]["distance"]})\nNearest Named Color: {thecolorapidata["name"]["closest_named_hex"]}\n\nrgb: {thecolorapidata["rgb"]["r"]}, {thecolorapidata["rgb"]["g"]}, {thecolorapidata["rgb"]["b"]} (fraction: {thecolorapidata["rgb"]["fraction"]["r"]}, {thecolorapidata["rgb"]["fraction"]["g"]}, {thecolorapidata["rgb"]["fraction"]["b"]})\nhsl: {thecolorapidata["hsl"]["h"]}, {thecolorapidata["hsl"]["s"]}, {thecolorapidata["hsl"]["l"]} (fraction: {thecolorapidata["hsl"]["fraction"]["h"]}, {thecolorapidata["hsl"]["fraction"]["s"]}, {thecolorapidata["hsl"]["fraction"]["l"]})\nhsv: {thecolorapidata["hsv"]["h"]}, {thecolorapidata["hsv"]["s"]}, {thecolorapidata["hsv"]["v"]} (fraction: {thecolorapidata["hsv"]["fraction"]["h"]}, {thecolorapidata["hsv"]["fraction"]["s"]}, {thecolorapidata["hsv"]["fraction"]["v"]})", color=f"0x{thecolorapidata["hex"]["value"]}")
        embed.set_thumbnail(url=f"https://dummyimage.com/1000x1000/{color_decided}/ffffff.png&text=+")

        await interaction.response.send_message(embed=embed)



    @app_commands.command(name="emoji", description="Chooses one random emoji")
    async def randomemoji(self, interaction: discord.Interaction):
        emojis = "👁️‍🗨️", ":grinning:", ":smiley:", ":smile:", ":grin:", ":laughing:", ":sweat_smile:", ":rofl:", ":joy:", ":slight_smile:", ":upside_down:", ":melting_face:", ":wink:", ":blush:", ":innocent:", ":smiling_face_with_3_hearts:", ":heart_eyes:", ":star_struck:", ":kissing_heart:", ":kissing:", ":relaxed:", ":kissing_closed_eyes:", ":kissing_smiling_eyes:", ":smiling_face_with_tear:", ":yum:", ":stuck_out_tongue:", ":stuck_out_tongue_winking_eye:", ":zany_face:", ":stuck_out_tongue_closed_eyes:", ":money_mouth:", ":hugging:", ":face_with_hand_over_mouth:", ":face_with_open_eyes_and_hand_over_mouth:", ":face_with_peeking_eye:", ":shushing_face:", ":thinking:", ":saluting_face:", ":zipper_mouth:", ":face_with_raised_eyebrow:", ":neutral_face:", ":expressionless:", ":no_mouth:", ":dotted_line_face:", ":face_in_clouds:", ":smirk:", ":unamused:", ":rolling_eyes:", ":grimacing:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":relieved:", ":pensive:", ":sleepy:", ":drooling_face:", ":sleeping:", ":mask:", ":thermometer_face:", ":head_bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:", ":cold_face:", ":woozy_face:", ":dizzy_face:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy:", ":partying_face:", ":disguised_face:", ":sunglasses:", ":nerd:", ":face_with_monocle:", ":confused:", ":face_with_diagonal_mouth:", ":worried:", ":slight_frown:", ":frowning2:", ":open_mouth:", ":hushed:", ":astonished:", ":flushed:", ":pleading_face:", ":face_holding_back_tears:", ":frowning:", ":anguished:", ":fearful:", ":cold_sweat:", ":disappointed_relieved:", ":cry:", ":sob:", ":scream:", ":confounded:", ":persevere:", ":disappointed:", ":sweat:", ":weary:", ":tired_face:", ":yawning_face:", ":triumph:", ":rage:", ":angry:", ":face_with_symbols_over_mouth:", ":smiling_imp:", ":imp:", ":skull:", ":skull_crossbones:", ":poop:", ":clown:", ":japanese_ogre:", ":japanese_goblin:", ":ghost:", ":alien:", ":space_invader:", ":robot:", ":smiley_cat:", ":smile_cat:", ":joy_cat:", ":heart_eyes_cat:", ":smirk_cat:", ":kissing_cat:", ":scream_cat:", ":crying_cat_face:", ":pouting_cat:", ":see_no_evil:", ":hear_no_evil:", ":speak_no_evil:", ":love_letter:", ":cupid:", ":gift_heart:", ":sparkling_heart:", ":heartpulse:", ":heartbeat:", ":revolving_hearts:", ":two_hearts:", ":heart_decoration:", ":heart_exclamation:", ":broken_heart:", ":heart_on_fire:", ":mending_heart:", ":heart:", ":pink_heart:", ":orange_heart:", ":yellow_heart:", ":green_heart:", ":blue_heart:", ":light_blue_heart:", ":purple_heart:", ":brown_heart:", ":black_heart:", ":grey_heart:", ":white_heart:", ":kiss:", ":100:", ":anger:", ":boom:", ":dizzy:", ":sweat_drops:", ":dash:", ":hole:", ":speech_balloon:, :speech_left:", ":anger_right:", ":thought_balloon:", ":zzz:", ":wave:", ":raised_back_of_hand:", ":hand_splayed:", ":raised_hand:", ":vulcan:", ":rightwards_hand:", ":leftwards_hand:", ":palm_down_hand:", ":palm_up_hand:", ":leftwards_pushing_hand:", ":rightwards_pushing_hand:", ":ok_hand:", ":pinched_fingers:", ":pinching_hand:", ":v:", ":fingers_crossed:", ":hand_with_index_finger_and_thumb_crossed:", ":love_you_gesture:", ":metal:", ":call_me:", ":point_left:", ":point_right:", ":point_up_2:", ":middle_finger:", ":point_down:", ":point_up:", ":index_pointing_at_the_viewer:", ":thumbsup:", ":thumbsdown:", ":fist:", ":punch:", ":left_facing_fist:", ":right_facing_fist:", ":clap:", ":raised_hands:", ":heart_hands:", ":open_hands:", ":palms_up_together:", ":handshake:", ":pray:", ":writing_hand:", ":nail_care:", ":selfie:", ":muscle:", ":mechanical_arm:", ":mechanical_leg:", ":leg:", ":foot:", ":ear:", ":ear_with_hearing_aid:", ":nose:", ":brain:", ":anatomical_heart:", ":lungs:", ":tooth:", ":bone:", ":eyes:", ":eye:", ":tongue:", ":lips:", ":biting_lip:", ":baby:", ":child:", ":adult:", ":blond_haired_person:", ":bearded_person:", ":person_red_hair:", ":person_curly_hair:", ":person_white_hair:", ":person_bald:", ":older_adult:", ":person_frowning:", ":person_pouting:", ":person_gesturing_no:", ":person_gesturing_ok:", ":person_tipping_hand:", ":person_raising_hand:", ":deaf_person:", ":person_bowing:", ":person_facepalming:", ":person_shrugging:", ":health_worker:", ":student:", ":teacher:", ":judge:", ":farmer:", ":cook:", ":mechanic:", ":factory_worker:", ":office_worker:", ":scientist:", ":technologist:", ":singer:", ":artist:", ":pilot:", ":astronaut:", ":firefighter:", ":police_officer:", ":detective:", ":guard:", ":ninja:", ":construction_worker:", ":person_with_crown:", ":prince:", ":princess:", ":person_wearing_turban:", ":man_with_chinese_cap:", ":woman_with_headscarf:", ":person_in_tuxedo:", ":person_with_veil:", ":pregnant_person:", ":breast_feeding:", ":person_feeding_baby:", ":angel:", ":santa:", ":mrs_claus:", ":mx_claus:", ":superhero:", ":supervillain:", ":mage:", ":fairy:", ":vampire:", ":merperson:", ":elf:", ":genie:", ":zombie:", ":troll:", ":person_getting_massage:", ":person_getting_haircut:", ":person_walking:", ":person_standing:", ":person_kneeling:", ":person_with_probing_cane:", ":person_in_motorized_wheelchair:", ":person_in_manual_wheelchair:", ":person_running:", ":dancer:", ":man_dancing:", ":levitate:", ":people_with_bunny_ears_partying:", ":person_in_steamy_room:", ":person_climbing:", ":person_fencing:", ":horse_racing:", ":skier:", ":snowboarder:", ":person_golfing:", ":person_surfing:", ":person_rowing_boat:", ":person_swimming:", ":person_bouncing_ball:", ":person_lifting_weights:", ":person_biking:", ":person_mountain_biking:", ":person_doing_cartwheel:", ":people_wrestling:", ":person_playing_water_polo:", ":person_playing_handball:", ":person_juggling:", ":person_in_lotus_position:", ":bath:", ":sleeping_accommodation:", ":people_holding_hands:", ":two_women_holding_hands:", ":couple:", ":two_men_holding_hands:", ":couplekiss:", ":kiss_woman_man:", ":kiss_mm:", ":kiss_ww:", ":couple_with_heart:", ":couple_with_heart_woman_man:", ":couple_mm:", ":couple_ww:", ":family:", ":family_mwg:", ":family_mwgb:", ":family_mwbb:", ":family_mwgg:", ":family_mmb:", ":family_mmg:", ":family_mmgb:", ":family_mmbb:", ":family_mmgg:", ":family_wwb:", ":family_wwg:", ":family_wwgb:", ":family_wwbb:", ":family_wwgg:", ":family_man_boy:", ":family_man_boy_boy:", ":family_man_girl:", ":family_man_girl_boy:", ":family_man_girl_girl:", ":family_woman_boy:", ":family_woman_boy_boy:", ":family_woman_girl:", ":family_woman_girl_boy:", ":family_woman_girl_girl:", ":speaking_head:", ":bust_in_silhouette:", ":busts_in_silhouette:", ":people_hugging:", ":footprints:", ":monkey_face:", ":monkey:", ":gorilla:", ":orangutan:", ":dog:", ":dog2:", ":guide_dog:", ":service_dog:", ":poodle:", ":wolf:", ":fox:", ":raccoon:", ":cat:", ":cat2:", ":black_cat:", ":lion_face:", ":tiger:", ":tiger2:", ":horse:", ":moose:", ":donkey:", ":racehorse:", ":unicorn:", ":zebra:", ":deer:", ":bison:", ":cow:", ":ox:", ":water_buffalo:", ":cow2:", ":pig:", ":pig2:", ":boar:", ":pig_nose:", ":ram:", ":sheep:", ":goat:", ":dromedary_camel:", ":camel:", ":llama:", ":giraffe:", ":elephant:", ":mammoth:", ":rhino:", ":hippopotamus:", ":mouse:", ":mouse2:", ":rat:", ":hamster:", ":rabbit:", ":rabbit2:", ":chipmunk:", ":beaver:", ":hedgehog:", ":bat:", ":bear:", ":polar_bear:", ":koala:", ":panda_face:", ":sloth:", ":otter:", ":skunk:", ":kangaroo:", ":badger:", ":feet:", ":turkey:", ":chicken:", ":rooster:", ":hatching_chick:", ":baby_chick:", ":hatched_chick:", ":bird:", ":penguin:", ":dove:", ":eagle:", ":duck:", ":swan:", ":owl:", ":dodo:", ":feather:", ":flamingo:", ":peacock:", ":parrot:", ":wing:", ":black_bird:", ":goose:", ":frog:", ":crocodile:", ":turtle:", ":lizard:", ":snake:", ":dragon_face:", ":dragon:", ":sauropod:", ":t_rex:", ":whale:", ":whale2:", ":dolphin:", ":seal:", ":fish:", ":tropical_fish:", ":blowfish:", ":shark:", ":octopus:", ":shell:", ":coral:", ":jellyfish:", ":snail:", ":butterfly:", ":bug:", ":ant:", ":bee:", ":beetle:", ":lady_beetle:", ":cricket:", ":cockroach:", ":spider:", ":spider_web:", ":scorpion:", ":mosquito:", ":fly:", ":worm:", ":microbe:", ":bouquet:", ":cherry_blossom:", ":white_flower:", ":lotus:", ":rosette:", ":rose:", ":wilted_rose:", ":hibiscus:", ":sunflower:", ":blossom:", ":tulip:", ":hyacinth:", ":seedling:", ":potted_plant:", ":evergreen_tree:", ":deciduous_tree:", ":palm_tree:", ":cactus:", ":ear_of_rice:", ":herb:", ":shamrock:", ":four_leaf_clover:", ":maple_leaf:", ":fallen_leaf:", ":leaves:", ":empty_nest:", ":nest_with_eggs:", ":mushroom:", ":grapes:", ":melon:", ":watermelon:", ":tangerine:", ":lemon:", ":banana:", ":pineapple:", ":mango:", ":apple:", ":green_apple:", ":pear:", ":peach:", ":cherries:", ":strawberry:", ":blueberries:", ":kiwi:", ":tomato:", ":olive:", ":coconut:", ":avocado:", ":eggplant:", ":potato:", ":carrot:", ":corn:", ":hot_pepper:", ":bell_pepper:", ":cucumber:", ":leafy_green:", ":broccoli:", ":garlic:", ":onion:", ":peanuts:", ":beans:", ":chestnut:", ":ginger_root:", ":pea_pod:", ":bread:", ":croissant:", ":french_bread:", ":flatbread:", ":pretzel:", ":bagel:", ":pancakes:", ":waffle:", ":cheese:", ":meat_on_bone:", ":poultry_leg:", ":cut_of_meat:", ":bacon:", ":hamburger:", ":fries:", ":pizza:", ":hotdog:", ":sandwich:", ":taco:", ":burrito:", ":tamale:", ":stuffed_flatbread:", ":falafel:", ":egg:", ":cooking:", ":shallow_pan_of_food:", ":stew:", ":fondue:", ":bowl_with_spoon:", ":salad:", ":popcorn:", ":butter:", ":salt:", ":canned_food:", ":bento:", ":rice_cracker:", ":rice_ball:", ":rice:", ":curry:", ":ramen:", ":spaghetti:", ":sweet_potato:", ":oden:", ":sushi:", ":fried_shrimp:", ":fish_cake:", ":moon_cake:", ":dango:", ":dumpling:", ":fortune_cookie:", ":takeout_box:", ":crab:", ":lobster:", ":shrimp:", ":squid:", ":oyster:", ":icecream:", ":shaved_ice:", ":ice_cream:", ":doughnut:", ":cookie:", ":birthday:", ":cake:", ":cupcake:", ":pie:", ":chocolate_bar:", ":candy:", ":lollipop:", ":custard:", ":honey_pot:", ":baby_bottle:", ":milk:", ":coffee:", ":teapot:", ":tea:", ":sake:", ":champagne:", ":wine_glass:", ":cocktail:", ":tropical_drink:", ":beer:", ":beers:", ":champagne_glass:", ":tumbler_glass:", ":pouring_liquid:", ":cup_with_straw:", ":bubble_tea:", ":beverage_box:", ":mate:", ":ice_cube:", ":chopsticks:", ":fork_knife_plate:", ":fork_and_knife:", ":spoon:", ":knife:", ":jar:", ":amphora:", ":earth_africa:", ":earth_americas:", ":earth_asia:", ":globe_with_meridians:", ":map:", ":japan:", ":compass:", ":mountain_snow:", ":mountain:", ":volcano:", ":mount_fuji:", ":camping:", ":beach:", ":desert:", ":island:", ":park:", ":stadium:", ":classical_building:", ":construction_site:", ":bricks:", ":rock:", ":wood:", ":hut:", ":homes:", ":house_abandoned:", ":house:", ":house_with_garden:", ":office:", ":post_office:", ":european_post_office:", ":hospital:", ":bank:", ":hotel:", ":love_hotel:", ":convenience_store:", ":school:", ":department_store:", ":factory:", ":japanese_castle:", ":european_castle:", ":wedding:", ":tokyo_tower:", ":statue_of_liberty:", ":church:", ":mosque:", ":hindu_temple:", ":synagogue:", ":shinto_shrine:", ":kaaba:", ":fountain:", ":tent:", ":foggy:", ":night_with_stars:", ":cityscape:", ":sunrise_over_mountains:", ":sunrise:", ":city_dusk:", ":city_sunset:", ":bridge_at_night:", ":hotsprings:", ":carousel_horse:", ":playground_slide:", ":ferris_wheel:", ":roller_coaster:", ":barber:", ":circus_tent:", ":steam_locomotive:", ":railway_car:", ":bullettrain_side:", ":bullettrain_front:", ":train2:", ":metro:", ":light_rail:", ":station:", ":tram:", ":monorail:", ":mountain_railway:", ":train:", ":bus:", ":oncoming_bus:", ":trolleybus:", ":minibus:", ":ambulance:", ":fire_engine:", ":police_car:", ":oncoming_police_car:", ":taxi:", ":oncoming_taxi:", ":red_car:", ":oncoming_automobile:", ":blue_car:", ":pickup_truck:", ":truck:", ":articulated_lorry:", ":tractor:", ":race_car:", ":motorcycle:", ":motor_scooter:", ":manual_wheelchair:", ":motorized_wheelchair:", ":auto_rickshaw:", ":bike:", ":scooter:", ":skateboard:", ":roller_skate:", ":busstop:", ":motorway:", ":railway_track:", ":oil:", ":fuelpump:", ":wheel:", ":rotating_light:", ":traffic_light:", ":vertical_traffic_light:", ":octagonal_sign:", ":construction:", ":anchor:", ":ring_buoy:", ":sailboat:", ":canoe:", ":speedboat:", ":cruise_ship:", ":ferry:", ":motorboat:", ":ship:", ":airplane:", ":airplane_small:", ":airplane_departure:", ":airplane_arriving:", ":parachute:", ":seat:", ":helicopter:", ":suspension_railway:", ":mountain_cableway:", ":aerial_tramway:", ":satellite_orbital:", ":rocket:", ":flying_saucer:", ":bellhop:", ":luggage:", ":hourglass:", ":hourglass_flowing_sand:", ":watch:", ":alarm_clock:", ":stopwatch:", ":timer:", ":clock:", ":clock12:", ":clock1230:", ":clock1:", ":clock130:", ":clock2:", ":clock230:", ":clock3:", ":clock330:", ":clock4:", ":clock430:", ":clock5:", ":clock530:", ":clock6:", ":clock630:", ":clock7:", ":clock730:", ":clock8:", ":clock830:", ":clock9:", ":clock930:", ":clock10:", ":clock1030:", ":clock11:", ":clock1130:", ":new_moon:", ":waxing_crescent_moon:", ":first_quarter_moon:", ":waxing_gibbous_moon:", ":full_moon:", ":waning_gibbous_moon:", ":last_quarter_moon:", ":waning_crescent_moon:", ":crescent_moon:", ":new_moon_with_face:", ":first_quarter_moon_with_face:", ":last_quarter_moon_with_face:", ":thermometer:", ":sunny:", ":full_moon_with_face:", ":sun_with_face:", ":ringed_planet:", ":star:", ":star2:", ":stars:", ":milky_way:", ":cloud:", ":partly_sunny:", ":thunder_cloud_rain:", ":white_sun_small_cloud:", ":white_sun_cloud:", ":white_sun_rain_cloud:", ":cloud_rain:", ":cloud_snow:", ":cloud_lightning:", ":cloud_tornado:", ":fog:", ":wind_blowing_face:", ":cyclone:", ":rainbow:", ":closed_umbrella:", ":umbrella2:", ":umbrella:", ":beach_umbrella:", ":zap:", ":snowflake:", ":snowman2:", ":snowman:", ":comet:", ":fire:", ":droplet:", ":ocean:", ":cloud_snow:", ":cloud_lightning:", ":cloud_tornado:", ":fog:", ":wind_blowing_face:", ":cyclone:", ":rainbow:", ":closed_umbrella:", ":umbrella2:", ":umbrella:", ":beach_umbrella:", ":zap:", ":snowflake:", ":snowman2:", ":snowman:", ":comet:", ":fire:", ":droplet:", ":ocean:", ":eyeglasses:", ":dark_sunglasses:", ":goggles:", ":lab_coat:", ":safety_vest:", ":necktie:", ":shirt:", ":jeans:", ":scarf:", ":gloves:", ":coat:", ":socks:", ":dress:", ":kimono:", ":sari:", ":one_piece_swimsuit:", ":briefs:", ":shorts:", ":bikini:", ":womans_clothes:", ":folding_hand_fan:", ":purse:", ":handbag:", ":pouch:", ":shopping_bags:", ":school_satchel:", ":thong_sandal:", ":mans_shoe:", ":athletic_shoe:", ":hiking_boot:", ":womans_flat_shoe:", ":high_heel:", ":sandal:", ":ballet_shoes:", ":boot:", ":hair_pick:", ":crown:", ":womans_hat:", ":tophat:", ":mortar_board:", ":billed_cap:", ":military_helmet:", ":helmet_with_cross:", ":prayer_beads:", ":lipstick:", ":ring:", ":gem:", ":mute:", ":speaker:", ":sound:", ":loud_sound:", ":loudspeaker:", ":mega:", ":postal_horn:", ":bell:", ":no_bell:", ":musical_score:", ":musical_note:", ":notes:", ":microphone2:", ":level_slider:", ":control_knobs:", ":microphone:", ":headphones:", ":radio:", ":saxophone:", ":accordion:", ":guitar:", ":musical_keyboard:", ":trumpet:", ":violin:", ":banjo:", ":drum:", ":long_drum:", ":maracas:", ":flute:", ":mobile_phone:", ":calling:", ":telephone:", ":telephone_receiver:", ":pager:", ":fax:", ":battery:", ":low_battery:", ":electric_plug:", ":computer:", ":desktop:", ":printer:", ":keyboard:", ":mouse_three_button:", ":trackball:", ":minidisc:", ":floppy_disk:", ":cd:", ":dvd:", ":abacus:", ":movie_camera:", ":film_frames:", ":projector:", ":clapper:", ":tv:", ":camera:", ":camera_with_flash:", ":video_camera:", ":vhs:", ":mag:", ":mag_right:", ":candle:", ":bulb:", ":flashlight:", ":izakaya_lantern:", ":diya_lamp:", ":notebook_with_decorative_cover:", ":closed_book:", ":book:", ":green_book:", ":blue_book:", ":orange_book:", ":books:", ":notebook:", ":ledger:", ":page_with_curl:", ":scroll:", ":page_facing_up:", ":newspaper:", ":newspaper2:", ":bookmark_tabs:", ":bookmark:", ":label:", ":moneybag:", ":coin:", ":yen:", ":dollar:", ":euro:", ":pound:", ":money_with_wings:", ":credit_card:", ":receipt:", ":chart:", ":envelope:", ":e_mail:", ":incoming_envelope:", ":envelope_with_arrow:", ":outbox_tray:", ":inbox_tray:", ":package:", ":mailbox:", ":mailbox_closed:", ":mailbox_with_mail:", ":mailbox_with_no_mail:", ":postbox:", ":ballot_box:", ":pencil2:", ":black_nib:", ":pen_fountain:", ":pen_ballpoint:", ":paintbrush:", ":crayon:", ":pencil:", ":briefcase:", ":file_folder:", ":open_file_folder:", ":dividers:", ":date:", ":calendar:", ":notepad_spiral:", ":calendar_spiral:", ":card_index:", ":chart_with_upwards_trend:", ":chart_with_downwards_trend:", ":bar_chart:", ":clipboard:", ":pushpin:", ":round_pushpin:", ":paperclip:", ":paperclips:", ":straight_ruler:", ":triangular_ruler:", ":scissors:", ":card_box:", ":file_cabinet:", ":wastebasket:", ":lock:", ":unlock:", ":lock_with_ink_pen:", ":closed_lock_with_key:", ":key:", ":key2:", ":hammer:", ":axe:", ":pick:", ":hammer_pick:", ":tools:", ":dagger:", ":crossed_swords:", ":bomb:", ":boomerang:", ":bow_and_arrow:", ":shield:", ":carpentry_saw:", ":wrench:", ":screwdriver:", ":nut_and_bolt:", ":gear:", ":compression:", ":scales:", ":probing_cane:", ":link:", ":chains:", ":hook:", ":toolbox:", ":magnet:", ":ladder:", ":alembic:", ":test_tube:", ":petri_dish:", ":dna:", ":microscope:", ":telescope:", ":satellite:", ":syringe:", ":drop_of_blood:", ":pill:", ":adhesive_bandage:", ":crutch:", ":stethoscope:", ":x_ray:", ":door:", ":elevator:", ":mirror:", ":window:", ":bed:", ":couch:", ":chair:", ":toilet:", ":plunger:", ":shower:", ":bathtub:", ":mouse_trap:", ":razor:", ":squeeze_bottle:", ":safety_pin:", ":broom:", ":basket:", ":roll_of_paper:", ":bucket:", ":soap:", ":bubbles:", ":toothbrush:", ":sponge:", ":fire_extinguisher:", ":shopping_cart:", ":smoking:", ":coffin:", ":headstone:", ":urn:", ":nazar_amulet:", ":hamsa:", ":moyai:", ":placard:", ":identification_card:", ":atm:", ":put_litter_in_its_place:", ":potable_water:", ":wheelchair:", ":mens:", ":womens:", ":restroom:", ":baby_symbol:", ":wc:", ":passport_control:", ":customs:", ":baggage_claim:", ":left_luggage:", ":warning:", ":children_crossing:", ":no_entry:", ":no_entry_sign:", ":no_bicycles:", ":no_smoking:", ":do_not_litter:", ":non_potable_water:", ":no_pedestrians:", ":no_mobile_phones:", ":underage:", ":radioactive:", ":biohazard:", ":arrow_up:", ":arrow_upper_right:", ":arrow_right:", ":arrow_lower_right:", ":arrow_down:", ":arrow_lower_left:", ":arrow_left:", ":arrow_upper_left:", ":arrow_up_down:", ":left_right_arrow:", ":leftwards_arrow_with_hook:", ":arrow_right_hook:", ":arrow_heading_up:", ":arrow_heading_down:", ":arrows_clockwise:", ":arrows_counterclockwise:", ":back:", ":end:", ":on:", ":soon:", ":top:", ":place_of_worship:", ":atom:", ":om_symbol:", ":star_of_david:", ":wheel_of_dharma:", ":yin_yang:", ":cross:", ":orthodox_cross:", ":star_and_crescent:", ":peace:", ":menorah:", ":six_pointed_star:", ":khanda:", ":aries:", ":taurus:", ":gemini:", ":cancer:", ":leo:", ":virgo:", ":libra:", ":scorpius:", ":sagittarius:", ":capricorn:", ":aquarius:", ":pisces:", ":ophiuchus:", ":twisted_rightwards_arrows:", ":repeat:", ":repeat_one:", ":arrow_forward:", ":fast_forward:", ":track_next:", ":play_pause:", ":arrow_backward:", ":rewind:", ":track_previous:", ":arrow_up_small:", ":arrow_double_up:", ":arrow_down_small:", ":arrow_double_down:", ":pause_button:", ":stop_button:", ":record_button:", ":eject:", ":cinema:", ":low_brightness:", ":high_brightness:", ":signal_strength:", ":wireless:", ":vibration_mode:", ":mobile_phone_off:", ":female_sign:", ":male_sign:", ":yellow_square:", ":green_square:", ":blue_square:", ":purple_square:", ":brown_square:", ":black_large_square:", ":white_large_square:", ":black_medium_square:", ":white_medium_square:", ":black_medium_small_square:", ":white_medium_small_square:", ":black_small_square:", ":white_small_square:", ":large_orange_diamond:", ":large_blue_diamond:", ":small_orange_diamond:", ":small_blue_diamond:", ":small_red_triangle:", ":small_red_triangle_down:", ":diamond_shape_with_a_dot_inside:", ":radio_button:", ":white_square_button:", ":black_square_button:", ":checkered_flag:", ":triangular_flag_on_post:", ":crossed_flags:", ":flag_black:", ":flag_white:", ":rainbow_flag:", ":transgender_flag:", ":pirate_flag:", ":flag_ac:", ":flag_ad:", ":flag_ae:", ":flag_af:", ":flag_ag:", ":flag_ai:", ":flag_al:", ":flag_am:", ":flag_ao:", ":flag_aq:", ":flag_ar:", ":flag_as:", ":flag_at:", ":flag_au:", ":flag_aw:", ":flag_ax:", ":flag_az:", ":flag_ba:", ":flag_bb:", ":flag_bd:", ":flag_be:", ":flag_bf:", ":flag_bg:", ":flag_bh:", ":flag_bi:", ":flag_bj:", ":flag_bl:", ":flag_bm:", ":flag_bn:", ":flag_bo:", ":flag_bq:", ":flag_br:", ":flag_bs:", ":flag_bt:", ":flag_bv:", ":flag_bw:", ":flag_by:", ":flag_bz:", ":flag_ca:", ":flag_cc:", ":flag_cd:", ":flag_cf:", ":flag_cg:", ":flag_ch:", ":flag_ci:", ":flag_ck:", ":flag_cl:", ":flag_cm:", ":flag_cn:", ":flag_co:", ":flag_cp:", ":flag_cr:", ":flag_cu:", ":flag_cv:", ":flag_cw:", ":flag_cx:", ":flag_cy:", ":flag_cz:", ":flag_de:", ":flag_dg:", ":flag_dj:", ":flag_dk:", ":flag_dm:", ":flag_do:", ":flag_dz:", ":flag_ea:", ":flag_ec:", ":flag_ee:", ":flag_eg:", ":flag_eh:", ":flag_er:", ":flag_es:", ":flag_et:", ":flag_eu:", ":flag_fi:", ":flag_fj:", ":flag_fk:", ":flag_fm:", ":flag_fo:", ":flag_fr:", ":flag_ga:", ":flag_gb:", ":flag_gd:", ":flag_ge:", ":flag_gf:", ":flag_gg:", ":flag_gh:", ":flag_gi:", ":flag_gl:", ":flag_gm:", ":flag_gn:", ":flag_gp:", ":flag_gq:", ":flag_gr:", ":flag_gs:", ":flag_gt:", ":flag_gu:", ":flag_gw:", ":flag_gy:", ":flag_hk:", ":flag_hm:", ":flag_hn:", ":flag_hr:", ":flag_ht:", ":flag_hu:", ":flag_ic:", ":flag_id:", ":flag_ie:", ":flag_il:", ":flag_im:", ":flag_in:", ":flag_io:", ":flag_iq:", ":flag_ir:", ":flag_is:", ":flag_it:", ":flag_je:", ":flag_jm:", ":flag_jo:", ":flag_jp:", ":flag_ke:", ":flag_kg:", ":flag_kh:", ":flag_ki:", ":flag_km:", ":flag_kn:", ":flag_kp:", ":flag_kr:", ":flag_kw:", ":flag_ky:", ":flag_kz:", ":flag_la:", ":flag_lb:", ":flag_lc:", ":flag_li:", ":flag_lk:", ":flag_lr:", ":flag_ls:", ":flag_lt:", ":flag_lu:", ":flag_lv:", ":flag_ly:", ":flag_ma:", ":flag_mc:", ":flag_md:", ":flag_me:", ":flag_mf:", ":flag_mg:", ":flag_mh:", ":flag_mk:", ":flag_ml:", ":flag_mm:", ":flag_mn:", ":flag_mo:", ":flag_mp:", ":flag_mq:", ":flag_mr:", ":flag_ms:", ":flag_mt:", ":flag_mu:", ":flag_mv:", ":flag_mw:", ":flag_mx:", ":flag_my:", ":flag_mz:", ":flag_na:", ":flag_nc:", ":flag_ne:", ":flag_nf:", ":flag_ng:", ":flag_ni:", ":flag_nl:", ":flag_no:", ":flag_np:", ":flag_nr:", ":flag_nu:", ":flag_nz:", ":flag_om:", ":flag_pa:", ":flag_pe:", ":flag_pf:", ":flag_pg:", ":flag_ph:", ":flag_pk:", ":flag_pl:", ":flag_pm:", ":flag_pn:", ":flag_pr:", ":flag_ps:", ":flag_pt:", ":flag_pw:", ":flag_py:", ":flag_qa:", ":flag_re:", ":flag_ro:", ":flag_rs:", ":flag_ru:", ":flag_rw:", ":flag_sa:", ":flag_sb:", ":flag_sc:", ":flag_sd:", ":flag_se:", ":flag_sg:", ":flag_sh:", ":flag_si:", ":flag_sj:", ":flag_sk:", ":flag_sl:", ":flag_sm:", ":flag_sn:", ":flag_so:", ":flag_sr:", ":flag_ss:", ":flag_st:", ":flag_sv:", ":flag_sx:", ":flag_sy:", ":flag_sz:", ":flag_ta:", ":flag_tc:", ":flag_td:", ":flag_tf:", ":flag_tg:", ":flag_th:", ":flag_tj:", ":flag_tk:", ":flag_tl:", ":flag_tm:", ":flag_tn:", ":flag_to:", ":flag_tr:", ":flag_tt:", ":flag_tv:", ":flag_tw:", ":flag_tz:", ":flag_ua:", ":flag_ug:", ":flag_um:", ":united_nations:", ":flag_us:", ":flag_uy:", ":flag_uz:", ":flag_va:", ":flag_vc:", ":flag_ve:", ":flag_vg:", ":flag_vi:", ":flag_vn:", ":flag_vu:", ":flag_wf:", ":flag_ws:", ":flag_xk:", ":flag_ye:", ":flag_yt:", ":flag_za:", ":flag_zm:", ":flag_zw:", ":england:", ":scotland:", ":wales:", ":flag_py:", ":flag_qa:", ":flag_re:", ":flag_ro:", ":flag_rs:", ":flag_ru:", ":flag_rw:", ":flag_sa:", ":flag_sb:", ":flag_sc:", ":flag_sd:", ":flag_se:", ":flag_sg:", ":flag_sh:", ":flag_si:", ":flag_sj:", ":flag_sk:", ":flag_sl:", ":flag_sm:", ":flag_sn:", ":flag_so:", ":flag_sr:", ":flag_ss:", ":flag_st:", ":flag_sv:", ":flag_sx:", ":flag_sy:", ":flag_sz:", ":flag_ta:", ":flag_tc:", ":flag_td:", ":flag_tf:", ":flag_tg:", ":flag_th:", ":flag_tj:", ":flag_tk:", ":flag_tl:", ":flag_tm:", ":flag_tn:", ":flag_to:", ":flag_tr:", ":flag_tt:", ":flag_tv:", ":flag_tw:", ":flag_tz:", ":flag_ua:", ":flag_ug:", ":flag_um:", ":united_nations:", ":flag_us:", ":flag_uy:", ":flag_uz:", ":flag_va:", ":flag_vc:", ":flag_ve:", ":flag_vg:", ":flag_vi:", ":flag_vn:", ":flag_vu:", ":flag_wf:", ":flag_ws:", ":flag_xk:", ":flag_ye:", ":flag_yt:", ":flag_za:", ":flag_zm:", ":flag_zw:", ":england:", ":scotland:", ":wales:", ":heavy_multiplication_x:", ":heavy_plus_sign:", ":heavy_minus_sign:", ":heavy_division_sign:", ":heavy_equals_sign:", ":infinity:", ":bangbang:", ":interrobang:", ":question:", ":grey_question:", ":grey_exclamation:", ":exclamation:", ":wavy_dash:", ":currency_exchange:", ":heavy_dollar_sign:", ":medical_symbol:", ":recycle:", ":fleur_de_lis:", ":trident:", ":name_badge:", ":beginner:", ":o:", ":white_check_mark:", ":ballot_box_with_check:", ":heavy_check_mark:", ":x:", ":negative_squared_cross_mark:", ":curly_loop:", ":loop:", ":part_alternation_mark:", ":eight_spoked_asterisk:", ":eight_pointed_black_star:", ":sparkle:", ":copyright:", ":registered:", ":tm:", ":hash:", ":asterisk:", ":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:", ":capital_abcd:", ":abcd:", ":1234:", ":symbols:", ":abc:", ":a:", ":ab:", ":b:", ":cl:", ":cool:", ":free:", ":information_source:", ":id:", ":m:", ":new:", ":ng:", ":o2:", ":ok:", ":parking:", ":sos:", ":up:", ":vs:", ":koko:", ":sa:", ":u6708:", ":u6709:", ":u6307:", ":ideograph_advantage:", ":u5272:", ":u7121:", ":u7981:", ":accept:", ":u7533:", ":u5408:", ":u7a7a:", ":congratulations:", ":secret:", ":u55b6:", ":u6e80:", ":red_circle:", ":orange_circle:", ":yellow_circle:", ":green_circle:", ":blue_circle:", ":purple_circle:", ":brown_circle:", ":black_circle:", ":white_circle:", ":red_square:", ":orange_square:", ":yellow_square:", ":green_square:", ":blue_square:", ":purple_square:", ":brown_square:", ":black_large_square:", ":white_large_square:", ":black_medium_square:", ":white_medium_square:", ":black_medium_small_square:", ":white_medium_small_square:", ":black_small_square:", ":white_small_square:", ":large_orange_diamond:", ":large_blue_diamond:", ":small_orange_diamond:", ":small_blue_diamond:", ":small_red_triangle:", ":small_red_triangle_down:", ":diamond_shape_with_a_dot_inside:", ":radio_button:", ":white_square_button:", ":black_square_button:", "⚧️"
        await interaction.response.send_message(random.choice(emojis))

bot.tree.add_command(Random(name="random", description="A set of commands that ues randomness"))

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Minecraft(app_commands.Group):
    @app_commands.command(name="boop", description="Boop Someone!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def boop(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"To {member.mention}:<:_B:1308471985713713292><:oo:1308472199677612044><:p_:1320448611523362826>")

    @app_commands.command(name='skin', description='Get the Skin of a minecraft player')
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.choices(
        mode= [
            app_commands.Choice(name='Face', value='face'),
            app_commands.Choice(name='Head', value='head'),
            app_commands.Choice(name='Body', value='body/full'),
            app_commands.Choice(name='Front Body', value='body/front'),
            app_commands.Choice(name='Back Body', value='body/back'),
            app_commands.Choice(name='Left Body', value='body/left'),
            app_commands.Choice(name='Right Body', value='body/right'),
            app_commands.Choice(name='Skin File', value='skins'),
        ]
    )
    async def mcskin(self, interaction: discord.Interaction, username: str, mode: app_commands.Choice[str], scale: typing.Optional[int]):
        await interaction.response.defer()
        url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
        response = requests.get(url)

        data = response.json()
        uuid = data['id']
        skin_url = f"https://api.mineatar.io/{mode.value}/{uuid}?scale={scale}"
        await interaction.followup.send(skin_url)

    @bot.tree.command(name='achivement', description='Generate a Minecraft Achivement!')
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def achivement(self, interaction: discord.Interaction, block: str, title: str, text1: str, text2: typing.Optional[str]):
        if " " in block: await interaction.response.send_message("Don't use spaces in the block name!")
        else:
            if text2 == None: text2 = " "
            else: text2 = text2
            title.replace(" ", "..")
            text1.replace(" ", "..")
            text2.replace(" ", "..")
            await interaction.response.send_message(f"https://minecraft-api.com/api/achivements/{block}/{title}/{text1}/{text2}")

bot.tree.add_command(Minecraft(name="minecraft", description="Minecraft related Commands"))

@bot.tree.command(name="calculate", description="Calculate something")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.describe(equation="What do you want to calculate?")
async def calculatecommand(interaction: discord.Interaction, equation: str):
    await interaction.response.defer()
    calculated=ast.literal_eval(equation)
    await interaction.followup.send(calculated)

@bot.tree.command(name="yes-no-image", description="Get an yes or no answer and an image matching that over an API")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def yesnoapi(interaction:discord.Interaction):
    url = 'https://yesno.wtf/api'
    response = requests.get(url)
    data = response.json()
    apianswer = data.get('answer')
    apiimage = data.get('image')
    embed=discord.Embed(title=apianswer, description=apiimage)
    await interaction.response.send_message(f"""{apianswer}
{apiimage}""")

@bot.tree.command(name="timeout", description="WIP timeout a member")
@app_commands.describe(member="Who to timeout?", duration="For how long to timeout?")
@app_commands.choices(
    duration=[
        app_commands.Choice(name="30 Minutes", value=30),
        app_commands.Choice(name="1 Hour", value=60),
        app_commands.Choice(name="2 Hours", value=120),
        app_commands.Choice(name="3 Hours", value=180),
        app_commands.Choice(name="4 Hours", value=240),
        app_commands.Choice(name="6 Hours", value=360),
        app_commands.Choice(name="12 Hours", value=720),
        app_commands.Choice(name="1 Day", value=3600),
        app_commands.Choice(name="2 Days", value=7200),
        app_commands.Choice(name="3 Days", value=10800),
        app_commands.Choice(name="7 Days", value=25200),
        app_commands.Choice(name="14 Days", value=50400),
        app_commands.Choice(name="28 Days", value=108000)
    ]
)
async def timeoutcommand(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str):
    timeout_duration = duration * 60
    timeout_end = time.time() + timeout_duration
    await member.timeout(datetime, reason=reason)

    await interaction.response.send_message(f'Added a timeout to {member.mention} for {duration}', ephemeral=True)

@bot.tree.command(name="8ball", description="Let the 8ball decide an Answer!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def embed_command(interaction: discord.Interaction, question: str):
    eightball_responses = "Absolutely", "Yes, definitely.", "Most likely.", "It is certain.", "You can count on it", "It seems so", "Yes", "Positive"  "Microsoft Outlook good.", "Don't count on it.", "My sources say no.", "Microsoft Outlook not so good.", "Very doubtful", "No", "Negative", "It is not certain", "Ask again later.", "Concentrate and try again.", "Cannot predict now."
    answer = random.choice(eightball_responses)
    embed = discord.Embed(title=f"The 8ball says: {answer}", description=f"Your Question: {question}", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="translate", description="WIP Translate something")
@app_commands.describe(to_from="Choose if you want to translate from english to ... or to english from ...", language="Which Language?", language2="Which Language? (Due to discords limitations, I need to make a second Option as I can't have more then 25)")
@app_commands.choices(
    language =[
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="Spanish", value="es"),
        app_commands.Choice(name="French", value="fr"),
        app_commands.Choice(name="German", value="de"),
        app_commands.Choice(name="Italian", value="it"),
        app_commands.Choice(name="Portuguese", value="pt"),
        app_commands.Choice(name="Dutch", value="nl"),
        app_commands.Choice(name="Russian", value="ru"),
        app_commands.Choice(name="Chinese (Simplified)", value="zh-cn"),
        app_commands.Choice(name="Chinese (Traditional)", value="zh-tw"),
        app_commands.Choice(name="Arabic", value="ar"),
        app_commands.Choice(name="Japanese", value="ja"),
        app_commands.Choice(name="Korean", value="ko"),
        app_commands.Choice(name="Turkish", value="tr"),
        app_commands.Choice(name="Hindi", value="hi"),
        app_commands.Choice(name="Bengali", value="bn"),
        app_commands.Choice(name="Greek", value="el"),
        app_commands.Choice(name="Czech", value="cs"),
        app_commands.Choice(name="Polish", value="pl"),
        app_commands.Choice(name="Romanian", value="ro"),
        app_commands.Choice(name="Thai", value="th"),
        app_commands.Choice(name="Vietnamese", value="vi"),
        app_commands.Choice(name="Swedish", value="sv"),
        app_commands.Choice(name="Danish", value="da"),
        app_commands.Choice(name="Finnish", value="fi")
    ]
)
@app_commands.choices(
    language2 =[
        app_commands.Choice(name="Norwegian", value="no"),
        app_commands.Choice(name="Hebrew", value="he"),
        app_commands.Choice(name="Ukrainian", value="uk"),
        app_commands.Choice(name="Hungarian", value="hu"),
        app_commands.Choice(name="Indonesian", value="id"),
        app_commands.Choice(name="Malay", value="ms"),
        app_commands.Choice(name="Tamil", value="ta"),
        app_commands.Choice(name="Telugu", value="te"),
        app_commands.Choice(name="Punjabi", value="pa"),
        app_commands.Choice(name="Lithuanian", value="lt"),
        app_commands.Choice(name="Latvian", value="lv"),
        app_commands.Choice(name="Estonian", value="et"),
        app_commands.Choice(name="Slovak", value="sk"),
        app_commands.Choice(name="Slovenian", value="sl"),
        app_commands.Choice(name="Serbian", value="sr"),
        app_commands.Choice(name="Croatian", value="hr"),
        app_commands.Choice(name="Bosnian", value="bs"),
        app_commands.Choice(name="Swahili", value="sw"),
        app_commands.Choice(name="Icelandic", value="is"),
        app_commands.Choice(name="Nepali", value="ne")
    ]
)
@app_commands.choices(
    to_from =[
        app_commands.Choice(name="to", value="y"),
        app_commands.Choice(name="from", value="n")
    ]
)
async def translatecommand(interaction: discord.Interaction, to_from: app_commands.Choice[str], text: str, language: typing.Optional[str] = None, language2: typing.Optional[app_commands.Choice[str]] = None):
    if language == None and language2 == None: languagetarget = "en" 
    elif language != None and language2 == None: languagetarget = language.value
    elif language2 != None and language == None: languagetarget = language2.value
    else: await interaction.response.send_message("You can only set 1 Language")

    if to_from.value == "n": translatesource="en"
    else: translatesource = language

    

    translator = GoogleTranslator(source=translatesource, target=languagetarget)
    result = translator.translate
    embed = discord.Embed(title="Translator", description=f"""Translated ```
{text}```
to

```
{result}```""")

class User(app_commands.Group):
    @app_commands.command(name="info", description="Get Info about a User.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def dmcommand(self, interaction: discord.Interaction, member: discord.Member):
        for roles in member.roles:
            roleslist = []
            roleslist.append(roles)
        embed=discord.Embed(title=f"{member.mention} - Informations", description=f"**{member.display_name}** ({member.name} - {member.id})")
        embed.add_field(name="Roles", value=roleslist)
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)

bot.tree.add_command(User(name="user", description="A collection of commands about Users."))

@bot.tree.context_menu(name="Spell Correct")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def spellcorrection(interaction: discord.Interaction, message: discord.Message):
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
        await interaction.response.send_message(" ".join(corrected))
    else:
        await interaction.response.send_message("Nothing to correct found.")

@bot.tree.command(name="instant-answers", description="Get Instant answers with DuckDuckGo")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
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
    embed.set_footer(text="Instant Answers")

    await interaction.response.send_message(embed=embed)


dotenv.load_dotenv(dotenv_path="C:/Users/tino/.vscode/DiscordBot/tokens.env")
bot.run(os.getenv(key="TOKENEXP"))