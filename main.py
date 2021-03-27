from discord.ext import commands
import discord
import openai
import json
openai.api_key = ""
openai.Engine.retrieve("davinci")


client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_message(message):

    if message.content.startswith('!help'):
        await message.channel.send("Commands: " + "\n" + "To ask Questions: !q <question>" + "\n" + "To translate English to French: !etf <english>" + "\n" + "To see tweet classification: !tweet <tweet-text>" + "\n" + "To get a short summary: !tldr <paragraph-to-tummarize>")

    if message.author == client.user:
        return

    if message.content.startswith('!q'):
        msg = message.content[2:]
        response = openai.Completion.create(
            engine="davinci",
            prompt="Q:" + msg + "?",
            max_tokens=100,
            temperature=0,
            top_p=1,
            n=1,
            stop="\nQ",
            frequency_penalty=1
        )
    if message.content.startswith('!etf'):
        msg = message.content[4:]
        response = openai.Completion.create(
            engine="davinci",
            prompt="English:" + msg + "\nFrench:",
            temperature=0.5,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
    if message.content.startswith('!tweet'):
        msg = message.content[6:]
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a tweet sentiment classifier\n\n\nTweet: \"I loved the new Batman movie!\"\nSentiment: Positive\n###\nTweet: \"I hate it when my phone battery dies.\"\nSentiment: Negative\n###\nTweet: \"My day has been 👍\"\nSentiment: Positive\n###\nTweet: \"This is the link to the article\"\nSentiment: Neutral\n###\nTweet: \"This new music video blew my mind\"\nSentiment:" + "\nTweet: \"" + msg + "\"\nSentiment:",
            temperature=0.3,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["\n"]
        )
    if message.content.startswith('!tldr'):
        msg = message.content[5:]
        response = openai.Completion.create(
            engine="davinci",
            prompt=msg + "\n\ntl;dr:",
            temperature=0.3,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop="."
        )

    outer = response['choices']
    ans = outer[0].text
    await message.channel.send(ans)


client.run('')
