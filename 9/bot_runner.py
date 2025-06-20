#test token (you wont nuke any servers tho) = "no token lol"
import discord, random, datetime
from discord.ext import commands

def New_bot(bot_token, config, responces, bot_commands):
    command_prefix = config["command_prefix"][0]
    user_replace = config["user_replace"]
    bot_replace = config["bot_replace"]
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix = "", intents=intents)

    def Hello(bot_name):
        return f"Hello, my name is {bot_name}"
    
    def Random_num():
        return f"The number I though of is: {random.randint(1, 10)}"
    
    def Date():
        return f"Currently it is {datetime.datetime.today()}"

    @client.event
    async def on_ready():
        pass

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        prep_message = message.content
        if prep_message[0] == command_prefix:
            prep_message = prep_message.replace(command_prefix, "", 1)
            prep_message = prep_message.replace(client.user.name, bot_replace)
            prep_message = prep_message.replace(message.author.name, user_replace)
            if bot_commands["Hello"] == prep_message:
                await message.channel.send(Hello(client.user.name))
            elif bot_commands["Random_num"] == prep_message:
                await message.channel.send(Random_num())
            elif bot_commands["Date"] == prep_message:
                await message.channel.send(Date())
            else:
                await message.channel.send("Unknown command.")
        else:
            for key_message in responces.keys():
                newkey_message = key_message.replace(bot_replace, client.user.name)
                newkey_message = newkey_message.replace(user_replace, message.author.name)
                if prep_message == newkey_message:
                    responce = responces[key_message].replace(bot_replace, client.user.name)
                    responce = responce.replace(user_replace, message.author.name)
                    await message.channel.send(responce)
                
    client.run(bot_token)