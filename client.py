from discord import Client
import discord
import json

# loads config file, exits client if not found
cfg = None
try:
    with open("config.example.json", "r") as cfgFile:
        cfg = json.load(cfgFile)
except FileNotFoundError:
    print(
        'take "config.example.json", rename it to "config.json" and edit the config before running the client')

client = Client()


@client.event
async def on_ready():
    servers = []
    channels = []
    # Initial server selection
    for x in client.guilds:
        servers.append(x)
    for x in range(len(servers)):
        print(f"{ x }: { servers[x].name }")
    while True:
        try:
            server_ch = input("select a server: ")
            server = servers[int(server_ch)]
            break
        except (IndexError, ValueError):
            print(f"not a server: { server_ch }")
    # Initial channel selection
    for x in server.channels:
        if type(x) == discord.TextChannel:
            channels.append(x)
    for x in range(len(channels)):
        print(f"{ x }: #{ channels[x].name }")
    while True:
        try:
            channel_ch = input("select a channel: ")
            channel = channels[int(channel_ch)]
            break
        except (IndexError, ValueError):
            print(f"not a channel: { channel_ch }")
    print("type help to list the commands you can use...")
    while True:
        opts = input(": ").split(" ")
        # Help menu
        if opts[0] == "help":
            print()
            print("help: show this")
            print("send: send a message")
            print("channels: show all channels in this server")
            print("servers: show all servers that you are in")
            print("emojis: shows all emojis for the current server")
            print("move-serv: switch servers")
            print("move-chan: switch channels")
            print("user: get information about a user using their username")
            print("ls: list the last 25 messages")
            print("cwd: list the server and channel you are in")
            print("exit: quit the shell...")
            print()
        # Send messages
        elif opts[0] == "send":
            print("type /exit to exit.\ntype /emojis for a list of emojis.")
            while True:
                msg = input("message: ")
                if msg == "":
                    print("can't send an empty message!")
                    continue
                # Emoji list for current server
                elif msg == "/emojis":
                    print(f"emojis for { server }:")
                    for emoji in channel.guild.emojis[:50]:
                        print(emoji)
                # Leave chatbox
                elif msg == "/exit":
                    break
                else:
                    await channel.send(msg)
        # List channels
        elif opts[0] == "channels":
            for x in range(len(channels)):
                print(f"{ x }: #{ channels[x].name }")
        # List servers
        elif opts[0] == "servers":
            for x in range(len(servers)):
                print(f"{ x }: { servers[x].name }")
        # Move current server
        elif opts[0] == "move-serv":
            previous_server = server
            previous_channel = channel
            try:
                servers = []
                channels = []
                for x in client.guilds:
                    servers.append(x)
                for x in range(len(servers)):
                    print(f"{ x }: { servers[x].name }")
                server_ch = input("select a server: ")
                server = servers[int(server_ch)]
                for x in server.channels:
                    if type(x) == discord.TextChannel:
                        channels.append(x)
                for x in range(len(channels)):
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
        # List emoji list
        elif opts[0] == "emojis":
            print(f"emojis for { server }:")
            for emoji in channel.guild.emojis[:50]:
                print(emoji)
        # Move from channel in server
        elif opts[0] == "move-chan":
            previous_channel = channel
            try:
                for x in range(len(channels)):
                    print(f"{ x }: #{ channels[x].name }")
                channel_ch = input("select a channel: ")
                channel = channels[int(channel_ch)]
            except (IndexError, ValueError):
                print(f"not a channel: { channel_ch }")
                channel = previous_channel
        # User profile
        elif opts[0] == "user":
            try:
                member = discord.utils.get(channel.guild.members, name=opts[1])
                if member is None:
                    print(f"unable to find member { opts[1] }")
                    continue
                activity = {
                    discord.ActivityType.playing: "Playing",
                    discord.ActivityType.streaming: "Streaming",
                    discord.ActivityType.listening: "Listening to",
                    discord.ActivityType.watching: "Watching"}
                try:
                    try:
                        activity_type = activity[member.activity.type]
                    except:
                        activity_type = "Playing"
                except:
                    activity_type = None
                activity_name = member.activity.name if member.activity else None
                print(f"{ member.name }#{ member.discriminator }'s profile:\n\n"
                      f"nick: { member.nick }\n"
                      f"id: { member.id }\n"
                      f"status: { member.status }\n"
                      f"{ activity_type }: { activity_name }\n"
                      f"avatar: { member.avatar_url }\n"
                      f"bot: { member.bot }\n")
            except IndexError:
                print("no username provided for an argument...")
        # Get current server and channel
        elif opts[0] == "cwd":
            print()
            print(f"server: { server.name }")
            print(f"channel: #{ channel.name }")
            print()
        # Exit client
        elif opts[0] == "exit":
            raise KeyboardInterrupt
        # List last amount of messages (Defaults to 25.)
        elif opts[0] == "ls":
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
