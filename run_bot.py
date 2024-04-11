import re
import os
import asyncio

import toml
import discord
from discord.commands import Option
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
DISCORD_API = os.getenv("DISCORD_API")

client = OpenAI(base_url=LLM_API_URL, api_key=LLM_API_KEY)

# Load the configuration from the TOML file
config = toml.load("config.toml")

model_id = config["llm_model"]["model_id"]

# Access the language channels
language_channels = config["language_channels"]

# Access the monitored channels
monitored_channels = config["monitored_channels"]["channels"]


# Access the discord prompt template
discord_prompt_template = config["discord_prompt"]["prompt"]

# Function to format the discord prompt with the language
def discord_prompt(language):
    return discord_prompt_template.format(language=language)

language_choices = [
    discord.OptionChoice(name='Korean', value='korean'),
    discord.OptionChoice(name='Chinese', value='chinese'),
    discord.OptionChoice(name='Hindi', value='hindi'),
    discord.OptionChoice(name='Japanese', value='japanese'),
    discord.OptionChoice(name='French', value='french'),
    discord.OptionChoice(name='Vietnamese', value='vietnamese'),
    discord.OptionChoice(name='Spanish', value='spanish'),
]



intents = discord.Intents.default()
intents.messages = True

# https://www.reddit.com/r/learnpython/comments/xicdp9/discord_bot_messagecontent_not_working/ 
intents.message_content = True
bot = discord.Bot(intents=intents,auto_sync_commands=True)
class ModerationError(Exception):
    """Custom exception for moderation errors."""
    pass

def active_reply(language, message):
    messages = [
            {"role": "system", "content": discord_prompt(language)},
            {"role": "user", "content": f"{message}"}
        ]
    print("active reply messages:", messages)


    completion = client.chat.completions.create(
        temperature=0.3,
        model=model_id,
        messages=messages,
    )
    print("completion: ", completion)
    
    content = completion.choices[0].message.content
    

    content = process_llm_response(content)

    content = re.sub(r'@[^\s]+', '', content) # Remove "@" mentions
    content = re.sub(r'http\S+|www\S+', '', content) # Remove URL links
        
    return content

def process_llm_response(content):
    content = content.strip('"')
    content = content.replace('\\n', '').replace('\n', '').replace('\\', '')

    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    
    return content

# listen language channels msg and rout to Babel channel
@bot.event
async def on_message(message):
    if message.channel.id in monitored_channels and not message.author.bot:
        print(f"Received message: {message}")
        print(f"Received message content: {message.content}")
        translated_text = active_reply('English', message.content)
        print(f"Translated to English: {translated_text}")

        # Send the translated message to the designated channel
        target_channel_id = config["target_channel"]["target_channel_id"]  # Replace with the ID of the channel to send translated messages
        target_channel = bot.get_channel(target_channel_id)
        sender = message.author
        await target_channel.send(f"{sender.name} posted in {message.channel.name} channel: {translated_text}")



@bot.slash_command(name='translate', description='Translate text to a specific language and teleport to its language channel')
async def translate(ctx, 
                    language: Option(str, 'Select the target language', choices=language_choices, required=True), # type: ignore
                    *, 
                    text: str
                    ):
    await ctx.defer()  # Defer the response to the command
    translated_text = active_reply(language, text)
    print(f"Translated to {language}: {translated_text}")
    
    
    if language in language_channels:
        channel_id = language_channels[language]
        channel = bot.get_channel(channel_id)
        sender = ctx.author.display_name
        translated_message = await channel.send(f"{sender}: {translated_text}")
        # Get the link to the translated message
        message_link = translated_message.jump_url
        await ctx.followup.send(f"Your message has been translated and sent to the {language} channel. Link: {message_link}")
    else:
        await ctx.followup.send(f"Unsupported language: {language}")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Heurist"))
    # Sync commands with Discord
    if bot.auto_sync_commands:
        await bot.sync_commands()
        print("sync command")

async def run_bots():
    await bot.start(DISCORD_API)


loop = asyncio.get_event_loop()
loop.run_until_complete(run_bots())
