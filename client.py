from discord import Client
import discord
import json

# loads config file, exits client if not found
cfg = None
try:
    with open("config.json", "r") as cfgFile:
        cfg = json.load(cfgFile)
except FileNotFoundError:
    print(
        'take "config.example.json", rename it to "config.json" and edit the config before running the client')

client = Client()


@client.event
async def on_ready():
    servers = []
    channels = []
    for x in client.guilds:
        servers.append(x)
    for x in range(0, len(servers)):
        print(f"{ x }: { servers[x].name }")
    while True:
        try:
            server_ch = input("select a server: ")
            server = servers[int(server_ch)]
            break
        except (IndexError, ValueError):
            print(f"not a server: { server_ch }")
    for x in server.channels:
        if type(x) == discord.TextChannel:
            channels.append(x)
    for x in range(0, len(channels)):
        print(f"{ x }: #{ channels[x].name }")
    while True:
        try:
            channel_ch = input("select a channel: ")
            channel = channels[int(channel_ch)]
            break
        except (IndexError, ValueError):
            print(f"not a channel: { channel_ch }")
    print("type /help to list the commands you can use...")
    while True:
        opts = input(": ").split(" ")

        if opts[0] == "/help":
            print()
            print("/help: show this")
            print("/send: send a message")
            print("/channels: show all channels in this server")
            print("/servers: show all servers that you are in")
            print("/emojis: shows all emojis for the current server")
            print("/move-serv: switch servers")
            print("/move-chan: switch channels")
            print("/user: get information about a user using their username")
            print("/ls: list the last 25 messages")
            print("/cwd: list the server and channel you are in")
            print("/exit: quit the shell...")
            print()

        elif opts[0] == "/send":
            print("Type /leave to exit.\nType /emojis for a list of emojis.")
            while True:
                msg = input("message: ")
                if msg == "":
                    print("Can't send an empty message!")
                    continue
                elif msg == "/emojis":
                    print(f"emojis for { server }:")
                    for emoji in channel.guild.emojis[:50]:
                        print(emoji)
                elif msg == "/leave":
                    break
                else:
                    await channel.send(msg)

        elif opts[0] == "/channels":
            for x in range(0, len(channels)):
                print(f"{ x }: #{ channels[x].name }")

        elif opts[0] == "/servers":
            for x in range(0, len(servers)):
                print(f"{ x }: { servers[x].name }")

        elif opts[0] == "/move-serv":
            previous_server = server
            previous_channel = channel
            try:
                servers = []
                channels = []
                for x in client.guilds:
                    servers.append(x)
                for x in range(0, len(servers)):
                    print(f"{ x }: { servers[x].name }")
                server_ch = input("select a server: ")
                server = servers[int(server_ch)]
                for x in server.channels:
                    if type(x) == discord.TextChannel:
                        channels.append(x)
                for x in range(0, len(channels)):
                    print(f"{ x }: #{ channels[x].name }")
                try:
                    channel_ch = input("select a channel: ")
                    channel = channels[int(channel_ch)]
                except (IndexError, ValueError):
                    print(f"not a channel: { channel_ch }")
                    server = previous_server
                    channel = previous_channel
            except (IndexError, ValueError):
                print(f"not a server: { server_ch }")
                server = previous_server

        elif opts[0] == "/emojis":
            print(f"emojis for { server }:")
            for emoji in channel.guild.emojis[:50]:
                print(emoji)

        elif opts[0] == "/move-chan":
            previous_channel = channel
            try:
                for x in range(0, len(channels)):
                    print(f"{ x }: #{ channels[x].name }")
                channel_ch = input("select a channel: ")
                channel = channels[int(channel_ch)]
            except (IndexError, ValueError):
                print(f"not a channel: { channel_ch }")
                channel = previous_channel

        elif opts[0] == "/user":
            if len(opts) == 0:
                print("no username provided for an arugment...")
            else:
                member = discord.utils.get(channel.guild.members, name=opts[1])
                if member is None:
                    print(f"unable to find member { opts[1] }")
                else:
                    print(f"{ member.name }#{ str(member.discriminator) }'s profile:\n"
                          f"nick: { member.nick }\n"
                          f"id: { str(member.id) }\n"
                          f"avatar: { str(member.avatar_url) }\n"
                          f"bot: { str(member.bot) }\n")

        elif opts[0] == "/cwd":
            print()
            print(f"server: { server.name }")
            print(f"channel: #{ channel.name }")
            print()

        elif opts[0] == "/exit":
            raise KeyboardInterrupt

        elif opts[0] == "/ls":
            if len(opts) == 2:
                messages = await channel.history(limit=int(opts[1])).flatten()
            else:
                messages = await channel.history(limit=25).flatten()
            for x in reversed(messages):
                print(f"({ x.guild }) { x.author }: { x.clean_content }")
        else:
            print(f"unrecognized command: { opts[0] }")


account = (cfg["bot"])
token = (cfg["token"])
client.run(token, bot=not bool(int(account)))
