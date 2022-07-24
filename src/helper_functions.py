#print(vars(self.commandHandler))
#print(self.commandHandler.__dict__)
# from pprint import pprint; # pprint(self.commandHandler)

import asyncio
import discord
import bot_http_requests
import json
import os

def messageFromBot(message: discord.Message) -> bool:
    if (message.author.bot):
        return True
    return False

async def handleCommand(message: discord.Message) -> None:
    print("comando digitado: "+message.content[1:])
    words = message.content.split()
    command = words[0][1:]
    arguments = words[1:] or [None]
    print("comando: ", command)
    print("argumentos: ", arguments)
    match command.lower():
        case 'alundra':
            await replyWithMyImage(message)

        case 'meme':
            async with message.channel.typing():
                await asyncio.sleep(1)
            jsn = await bot_http_requests.meme_search(1,arguments[0])
            await message.reply(jsn['url'])

        case 'google':
            if (not arguments[0]):
                await message.reply('Digite "!google <algo legal>" para pesquisar')
                return
            async with message.channel.typing():
                await asyncio.sleep(1)
            result = bot_http_requests.google_search(' '.join(str(pal) for pal in arguments[0:]))
            await message.reply('\n'.join(str(link) for link in result))

        case 'google2':
            if (True):
                await message.reply('Digite "!google <algo legal>" para pesquisar')
                return
            jsn = await bot_http_requests.google_http_search(' '.join(str(pal) for pal in arguments[0:]))
            await message.reply(jsn['file'])

        case 'play':
            if (not arguments[0]):
                await message.reply('Digite "!play <nome do vídeo>" para tocar')
                return
            await message.channel.send('!play <video> está em desenvolvimento!')
            # entrar no canal
            # buscar video
            # streamar o áudio

        case 'gato':
            async with message.channel.typing():
                await asyncio.sleep(1)
            jsn = await bot_http_requests.cat_search()
            await message.channel.send(jsn['file'])

        case 'cachorro':
            async with message.channel.typing():
                await asyncio.sleep(1)
            jsn = await bot_http_requests.dog_search(arguments[0])
            await message.channel.send(jsn['message'])

        case 'digite':
            async with message.channel.typing():
                await asyncio.sleep(1)
        
        case 'digite2':
            message.channel.typing()
            # Do some computational magic for about 10 seconds
            await message.channel.send('Done!')

        case 'voice':
            if (message.author.voice.channel is not None):
                channel = message.author.voice.channel
                await channel.connect()
            else:
                await message.reply("Entre em um canal de voz antes :3 (Caso já esteja tente sair e entrar novamente)")

        case default:
            pass



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