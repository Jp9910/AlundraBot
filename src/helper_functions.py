#print(vars(self.commandHandler))
#print(self.commandHandler.__dict__)
# from pprint import pprint; # pprint(self.commandHandler)

import discord

def messageFromBot(message: discord.Message) -> bool:
    if (message.author.bot):
        return True
    return False

def splitCommandFromArguments(message: discord.Message):
    words = message.content.split()
    command = words[0][1:]
    arguments = words[1:] or [None]
    return (command,arguments)

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
            pass
            #await message.add_reaction('👍')

async def replyWithMyImage(message: discord.Message) -> None:
    # async with discord.channel.typing():
    #     await asyncio.sleep(3)
    #print(os.listdir())
    #print(os.getcwd())
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


# To upload the file instead of just linking it,
# see https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-upload-an-image