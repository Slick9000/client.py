import discord, json, sys, os

# loads config file, setup if unfound
cfg = None
try:
    with open("config.json", "r") as cfgFile:
         cfg = json.load(cfgFile)
except FileNotFoundError:
    with open("config.json", "a+") as cfgFile:
         token = input("input token: ")
         bot = input("is this a bot? (y, n): ")
         def check_bot():
             if bot == 'y':
                 return True
             elif bot == 'n':
                 return False
         data = {
	         "bot":   check_bot(),
	         "token": token
         }
         setup = json.dumps(data, indent = 4)
         cfgFile.write(setup)
         print("setup complete, please rerun the client.")
         sys.exit()

client = discord.Client()


@client.event
async def on_ready():
    channels = []
    servers = client.guilds
    # initial server selection
    for x in range(len(servers)):
        print(f"{ x }: { servers[x].name }")
    while True:
        try:
            server_sl = input("select a server: ")
            server = servers[int(server_sl)]
            break
        except (IndexError, ValueError):
            print(f"not a server: { server_sl }")
    # initial channel selection
    for x in server.channels:
        if type(x) == discord.TextChannel:
            channels.append(x)
    for x in range(len(channels)):
        print(f"{ x }: #{ channels[x].name }")
    while True:
        try:
            channel_sl = input("select a channel: ")
            channel = channels[int(channel_sl)]
            break
        except (IndexError, ValueError):
            print(f"not a channel: { channel_sl }")
    print("client.py\ntype help for help.")
    while True:
        opts = input(": ").split(" ")
        # help menu
        if opts[0] == "help":
            print(
                "\nhelp:            |   show this\n"
                "send:            |   send a message\n"
                "delete:          |   delete a message\n"
                "dm:              |   opens a dm channel with the user\n"
                "upload:          |   uploads files to transfer.sh\n"
                "channels:        |   show all channels in the current server\n"
                "servers:         |   show all servers that you are in\n"
                "emojis:          |   shows all emojis for the current server\n"
                "reload-servers:  |   reload the client\n"
                "move-serv:       |   switch servers\n"
                "move-chan:       |   switch channels\n"
                "user:            |   get information about a user using their username\n"
                "ls:              |   list the last 25 messages\n"
                "cwd:             |   list the server and channel you are in\n"
                "shell:           |   execute shell commands\n"
                "exit:            |   quit the shell..."
            )
        # reload
        elif opts[0] == "reload-servers":
            servers = client.guilds
        # send messages
        elif opts[0] == "send":
            # send messages
            print("type ^^exit to exit.\n")
            while True:
                try:
                    msg = input("message: ")
                    if msg == "":
                        print("can't send an empty message!")
                        continue
                    elif msg == "^^exit":
                        break
                    else:
                        async with channel.typing():
                            await channel.send(msg)
                except Exception as e:
                    print(e)
        # delete a message
        elif opts[0] == "delete":
            try:
                if len(opts) == 2:
                    msg = await channel.get_message(opts[1])
                    await msg.delete()
                    print("message deleted.")
                else:
                    messages = await channel.history(limit=50).flatten()
                    for x in reversed(messages):
                        print(f"content: {x.clean_content if x.clean_content else None}\n"
                              f"id:      {x.id}\n"
                              )
                    msg_id = input("select an id: ")
                    msg = await channel.get_message(msg_id)
                    await msg.delete()
                    print(f"message with id of {msg.id} deleted.")
            except Exception as e:
                    print(e)
        # enter a dm channel
        elif opts[0] == "dm":
            try:
                # get user, open dm
                user = discord.utils.get(client.users,
                                         name = ' '.join(opts[1:])
                )
                if user is None:
                    print(f"unable to find member { ' '.join(opts[1:]) }")
                    continue
                print(f"entered dm channel with { user.name }.")
                channel = user
            except IndexError:
                # no name given
                print("no username provided as an argument...")
        # upload files to transfer.sh
        elif opts[0] == "upload":
            try:
                directory = opts[1]
                file = directory.split("\\")[-1]
                os.system(
                    f"curl --upload-file { directory } https://transfer.sh/{ file }"
                )
            except IndexError:
                # no directory given
                print(
                    "invalid syntax:\n"
                    '"upload C:\\users\\user\\Downloads\\file" or "local\\file.txt" would be the correct format.'
                )
        # show current server's channels
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
                server_sl = input("select a server: ")
                server = servers[int(server_sl)]
                for x in server.channels:
                    if type(x) == discord.TextChannel:
                        channels.append(x)
                for x in range(len(channels)):
                    print(f"{ x }: #{ channels[x].name }")
                try:
                    channel_sl = input("select a channel: ")
                    channel = channels[int(channel_sl)]
                except (IndexError, ValueError):
                    print(f"not a channel: { channel_sl }")
                    server = previous_server
                    channel = previous_channel
            except (IndexError, ValueError):
                print(f"not a server: { server_sl }")
                server = previous_server
        # move channel in current server
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
        # list emojis
        elif opts[0] == "emojis":
            for emoji in channel.guild.emojis[:100]:
                print(emoji)
        # lookup a user
        elif opts[0] == "user":
            try:
                # get user
                member = discord.utils.get(
                    channel.guild.members, name=" ".join(opts[1:])
                )
                if member is None:
                    print(f"unable to find member { opts[1] }")
                    continue
                # activity list
                activity = {
                    discord.ActivityType.playing: "playing",
                    discord.ActivityType.streaming: "streaming",
                    discord.ActivityType.listening: "listening to",
                    discord.ActivityType.watching: "watching",
                }
                try:
                    try:
                        activity_type = activity[member.activity.type]
                    except:
                        activity_type = "playing"
                except:
                    activity_type = None
                activity_name = member.activity.name if member.activity else None
                if activity_name == "Spotify":
                    activity_name += (f"\n  title:        {member.activity.title}\n"
                                      f"  artist(s):    {','.join(member.activity.artists)}\n"
                                      f"  album:        {member.activity.album}"
                                      )
                print(
                    f"{ member.name }#{ member.discriminator }'s profile:\n"
                    f"nick: { member.nick }\n"
                    f"id: { member.id }\n"
                    f"status: { member.status }\n"
                    f"{ activity_type }: { activity_name }\n"
                    f"avatar: { member.avatar_url }\n"
                    f"bot: { member.bot }\n"
                    f"created at { member.created_at }\n"
                )
            except IndexError:
                print("no username provided for an argument...")
        # current working directory
        elif opts[0] == "cwd":
            print(f"server: { server.name }")
            print(f"channel: #{ channel.name }\n")
        # exit client
        elif opts[0] == "exit":
            print("exited client.")
            await client.close()
            sys.exit()
        # execute shell commands
        elif opts[0] == "shell":
            print("enabled shell mode.")
            while True:
                command = input(": ")
                if not command == "exit":
                    os.system(command)
                else:
                    print("disabled shell mode.")
                    break
        # show last amount of messages (defaults to 25.)
        elif opts[0] == "ls":
            if len(opts) == 2:
                messages = await channel.history(limit=int(opts[1])).flatten()
            else:
                messages = await channel.history(limit=25).flatten()
            for x in reversed(messages):
                if discord.ChannelType.private:
                    print(f"{ x.author }: { x.clean_content }")
                else:
                    print(f"({ x.guild }) { x.author }: { x.clean_content }")
                if len(x.attachments) > 0:
                    print("attachments:")
                    for y in x.attachments:
                        print(f"  { y.filename }: { y.url }")
                if len(x.embeds) > 0:
                    print("embed:")
                    for y in x.embeds:
                        print(f"  title:       {y.title if y.title else ''}\n"
                              f"  description: {y.description if y.description else ''}\n"
                              f"  fields:      {y.fields if y.fields else ''}\n"
                              f"  image:       {y.image if y.image else ''}\n"
                              f"  footer:      {y.footer if y.image else ''}\n"
                       )
        # credits
        elif opts[0] == "credits":
            print(
"""
------------------------------------------------
      _ _            _
     | (_)          | |
  ___| |_  ___ _ __ | |_   _ __  _   _
 / __| | |/ _ \ '_ \| __| | '_ \| | | |
| (__| | |  __/ | | | |_ _| |_) | |_| |
 \___|_|_|\___|_| |_|\__(_) .__/ \__, |
                          | |     __/ |
                          |_|    |___/
------------------------------------------------
credits to:
    superwhiskers - original creator
    Slick9000 - cleanup, adding several features
------------------------------------------------
"""
)

        else:
            print(f"invalid command: { opts[0] }")

client.run(cfg['token'], bot=cfg['bot'])
