# import openai
import random
from openai import OpenAI
import asyncio
from collections import deque
import discord
import time
import random
# from BotInfo import ShellBot_manager
OPENROUTER_API_KEY = "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"

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

language_channels = {
    'korean': 1226343034514440353,  # Replace with the actual channel ID for Korean
    'chinese': 1226343034514440353,  # Replace with the actual channel ID for Chinese
}

monitored_channels = [
    1224412891340607712,  # Chinese channel
    1224412666450153482, # Korean channel,
    1226343034514440353,  # Mock chinese channel

    # Add more channel IDs as needed
]



# model_id = "openai/gpt-3.5-turbo-0125"
model_id = "nousresearch/nous-hermes-2-mixtral-8x7b-dpo"
print("model_id: ", model_id)

intents = discord.Intents.default()
intents.messages = True
# https://www.reddit.com/r/learnpython/comments/xicdp9/discord_bot_messagecontent_not_working/ 
intents.message_content = True
bot = discord.Bot(intents=intents)
# bot = commands.Bot(command_prefix='/', intents=intents)

# queue_en = deque(maxlen=10)
# queue_cn = deque(maxlen=10)
# queues = {##接���消息的频道
#     # '1140481547355553792': queue_en,
#     '1226275844809560175': queue_cn,
# }
# intents = discord.Intents.all()

# # Global dictionary to track messages being handled
# message_handling_status = {}

def discord_prompt(language):
    # Discord prompt is appended before the bot's custom system message to provide background info about our project
    return  f"""You are Babel in a Discord server of a Layer-2 AI protocol - Heurist, which is the most innovative and exciting project in crypto + AI, built by the dreamers and innovators. Heurist protocol aims to democratize AI inference access by a decentralized GPU network. You are also powered by Heurist's AI models and responsible for co-hosting this discord server that is full of cryptocurrency and AI enthusiasts.\n
     You are a helpful AI assistant. You task is to identify the language of the user message. Then translate it to ${language}. Your response should be the translation of the original of user message. Provide the translation in a clear, concise, and natural-sounding manner. Maintain the original meaning and tone of the message.
     """

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
    # print(completion.error.metadata.reasons)

    # if not completion.choices and ['harassment', 'hate'] in completion.error.metadata.reasons:
    #     raise ModerationError("The AI assistant has detected inappropriate content in the user message.")
    
    content = completion.choices[0].message.content
    

    content = process_llm_response(content)

        
    return content

def process_llm_response(content):
    content = content.strip('"')
    content = content.replace('\\n', '').replace('\n', '').replace('\\', '')

    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    
    return content

@bot.event
async def on_message(message):
    if message.channel.id in monitored_channels and not message.author.bot:
        print(f"Received message: {message}")
        print(f"Received message content: {message.content}")
        translated_text = active_reply('English', message.content)
        print(f"Translated to English: {translated_text}")

        # Send the translated message to the designated channel
        target_channel_id = 1226275844809560175  # Replace with the ID of the channel to send translated messages
        target_channel = bot.get_channel(target_channel_id)
        sender = message.author
        await target_channel.send(f"{sender.name}: {translated_text}")

    # await bot.process_commands(message)


@bot.slash_command()
async def translate(ctx, language: str, *, text: str):
    await ctx.defer()  # Defer the response to the command
    # deferred_message = await ctx.defer(ephemeral=True)
    # translator = Translator()
    translated_text = active_reply(language, text)
    print(f"Translated to {language}: {translated_text}")
    
    
    if language in language_channels:
        channel_id = language_channels[language]
        channel = bot.get_channel(channel_id)
        # sender = ctx.author.display_name
        sender = ctx.author
        translated_message = await channel.send(f"{sender.mention}: {translated_text}")
        # Get the link to the translated message
        message_link = translated_message.jump_url
        # await ctx.send(f"Your message has been translated and sent to the {language} channel. Link: {message_link}")
        await ctx.followup.send(f"Your message has been translated and sent to the {language} channel. Link: {message_link}")
    else:
        # await ctx.send(f"Unsup  ported language: {language}")
        await ctx.followup.send(f"Unsupported language: {language}")

async def run_bots():
    await bot.start('MTIyNjI3NDMwMzA2NzI5NTkwNQ.Goh5z0.zUKRcucGTTuhUEA4PDgqeGUeluF7m5GzrqZt2Q')

loop = asyncio.get_event_loop()
loop.run_until_complete(run_bots())
