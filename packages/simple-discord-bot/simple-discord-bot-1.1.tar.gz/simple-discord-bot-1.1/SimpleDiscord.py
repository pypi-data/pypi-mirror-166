from discord.ext import commands
import discord
import asyncio

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
custom_commands = {}

class SimpleBot():

    def __init__(self, token):

        # global bot

        self.TOKEN = token
        self.loop = asyncio.get_event_loop()
        self.running = False


        self.custom_commands = {}

        ## add debugging command ##
        self.add_command("test", lambda:"test function")



    def add_command(self, command_key, command_func):

        global custom_commands

        self.custom_commands[command_key] = command_func
        custom_commands = self.custom_commands


    def run(self):
        self.running = True
        bot.run(self.TOKEN)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    found = False

    print(message.content.split())
    # Find if custom command exist in dictionary
    for key in list(custom_commands.keys()):
        value = custom_commands[key]()
        # Added simple hardcoded prefix
        if message.content.startswith('!' + key):
            found = True
            await message.channel.send(value)

    # If not b
    if not found:
        await bot.process_commands(message)




def main():

    ## unit testing ##

    TOKEN = "YOUR TOKEN HERE"
    sBot = SimpleBot(TOKEN)

    def hello():
        return "Hello world!"


    def rand():
        import numpy as np
        return np.random.random()

    def readFile():
        with open("t.txt", "r") as t:
            t = t.read()
        return t.strip('\n')

    print("Adding command")
    sBot.add_command("hello", hello)
    sBot.add_command("rand", rand)
    sBot.add_command("file", readFile)

    sBot.run()
    asyncio.run(sBot.send_msg("Hello"))



if __name__ == '__main__':
    main()