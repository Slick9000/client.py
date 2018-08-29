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
    # initial server selection
    for x in client.guilds:
        servers.append(x)
    for x in range(len(servers)):
        print(f"{ x }: { servers[x].name }")
    while True:
        try:
            server_ch = input("select a server: ")
            server = servers[int(server_ch)]
            break
        except(IndexError, ValueError):
            print(f"not a server: { server_ch }")
    # initial channel selection
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
        except(IndexError, ValueError):
            print(f"not a channel: { channel_ch }")
    print("type help to list the commands you can use...")
    while True:
        opts = input(": ").split(" ")
        # help menu
        if opts[0] == "help":
            print("\nhelp: show this\n"
                  "send: send a message\n"
                  "channels: show all channels in the current server\n"
                  "servers: show all servers that you are in\n"
                  "emojis: shows all emojis for the current server\n"
                  "move-serv: switch servers\n"
                  "move-chan: switch channels\n"
                  "user: get information about a user using their username\n"
                  "members: shows all members for the current server\n"
                  "ls: list the last 25 messages\n"
                  "cwd: list the server and channel you are in\n"
                  "exit: quit the shell...")
        # send messages
        elif opts[0] == "send":
            print("type /exit to exit.\ntype /emojis for a list of emojis.")
            while True:
                msg = input("message: ")
                if msg == "":
                    print("can't send an empty message!")
                    continue
                # show emojis for current server
                elif msg == "/emojis":
                    print(f"emojis for { server }:")
                    for emoji in channel.guild.emojis[:50]:
                        print(emoji)
                # leave chatbox
                elif msg == "/exit":
                    break
                else:
                    await channel.send(msg)
        # show channels in current server
        elif opts[0] == "channels":
            for x in range(len(channels)):
                print(f"{ x }: #{ channels[x].name }")
        # show all servers
        elif opts[0] == "servers":
            for x in range(len(servers)):
                print(f"{ x }: { servers[x].name }")
        # move to a different server
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
        # show emojis in current server
        elif opts[0] == "emojis":
            print(f"emojis for { server }:")
            for emoji in channel.guild.emojis[:50]:
                print(emoji)
        # move to a different channel in server
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
        # user profile
        elif opts[0] == "user":
            try:
                member = discord.utils.get(channel.guild.members, name=opts[1])
                if member is None:
                    print(f"unable to find member { opts[1] }")
                    continue
                activity = {
                    discord.ActivityType.playing:    "playing",
                    discord.ActivityType.streaming:  "streaming",
                    discord.ActivityType.listening:  "listening to",
                    discord.ActivityType.watching:   "watching"}
                try:
                    try:
                        activity_type = activity[member.activity.type]
                    except:
                        activity_type = "playing"
                except:
                    activity_type = None
                activity_name = member.activity.name if member.activity else None
                print(f"{ member.name }#{ member.discriminator }'s profile:\n\n"
                      f"nick: { member.nick }\n"
                      f"id: { member.id }\n"
                      f"status: { member.status }\n"
                      f"{ activity_type }: { activity_name }\n"
                      f"avatar: { member.avatar_url }\n"
                      f"bot: { member.bot }\n"
                      f"created at { member.created_at }\n")
            except IndexError:
                print("no username provided for an argument...")
        # show current server and channel
        elif opts[0] == "cwd":
            print(f"\nserver: { server.name }")
            print(f"channel: #{ channel.name }\n")
        # exit client
        elif opts[0] == "exit":
            print("Exited client.")
            raise KeyboardInterrupt
        # show last amount of messages (defaults to 25.)
        elif opts[0] == "ls":
            if len(opts) == 2:
                messages = await channel.history(limit=int(opts[1])).flatten()
            else:
                messages = await channel.history(limit=25).flatten()
            for x in reversed(messages):
                print(f"({ x.guild }) { x.author }: { x.clean_content }")
        else:
            print(f"unrecognized command: { opts[0] }")

client.run(cfg["token"], bot=cfg["bot"])
