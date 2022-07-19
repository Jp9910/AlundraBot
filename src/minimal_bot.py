# This example requires the 'message_content' intent.

#The first line just imports the library
import discord
import env

intents = discord.Intents.default()
intents.message_content = True
#Next, we create an instance of a Client. This client is our connection to Discord.
client = discord.Client(intents=intents)


# We then use the Client.event() decorator to register an event. This library has many events.
# Since this library is asynchronous, we do things in a “callback” style manner.
# A callback is essentially a function that is called when something happens. In our case, the
# on_ready() event is called when the bot has finished logging in and setting things up and the
# on_message() event is called when the bot has received a message.
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(env.botkey)