import asyncio
import discord
import os

def messageFromBot(message: discord.Message) -> bool:
    if (message.author.bot):
        return True
    return False

async def handleCommand(message: discord.Message) -> None:
    print("comando digitado: "+message.content[1:])
    command = message.content[1:]
    match command:
        case 'alundra':
            await replyWithMyImage(message)


async def handleMessage(message: discord.Message) -> None:
    match message.content:
        case 'ping':
            await message.channel.send('pong')
        case 'vsf':
            await message.reply('vá vc >:T')
        case 'oi':
            await message.reply('oi ' + message.author.display_name + ' :)')
        case default:
            #emoji = '\N{THUMBS UP SIGN}' # or '\U0001f44d'
            await message.add_reaction('👍')

async def replyWithMyImage(message: discord.Message) -> None:
    # async with discord.channel.typing():
    #     await asyncio.sleep(3)
    print(os.listdir())
    print(os.getcwd())
    await message.channel.send(
        content='Sou eu!',
        file=discord.File('Resources/Images/alundra.png')
    )
    
# Send file:    
# with open('Resources/Images/alundra.png', 'rb') as fp:
#     await message.channel.send(
#         content='Sou eu!',
#         file=discord.File(fp, 'newfilename.png')
#     )