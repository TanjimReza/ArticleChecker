import re
from creds import BOT_TOKEN
import discord
from discord.commands import ApplicationContext, Option
guidid = [863087690889822238]
bot = discord.Bot(debug_guilds=[863087690889822238],intents=discord.Intents.all())
bot.connections = {}

@bot.event
async def on_ready():
    print('Ready')

@bot.slash_command(guild_ids=guidid, name="record", aliases=["r"])
async def record(
    ctx: ApplicationContext,
    encoding: Option(
        str,
        choices=[
            "mp3",
            "wav",
            "pcm",
            "ogg",
            "mka",
            "mkv",
            "mp4",
            "m4a",
        ],
    ),
):
    """Start Recording

    Args:
        ctx (ApplicationContext): Get commmand context
        encoding (Option, optional): Recording format. Defaults to [ "mp3", "wav", "pcm", "ogg", "mka", "mkv", "mp4", "m4a", ], ).

    Returns:
        File: Recorded file
    """
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("You're not in a vc right now")

    vc = await voice.channel.connect()
    bot.connections.update({ctx.guild.id: vc})

    if encoding == "mp3":
        sink = discord.sinks.MP3Sink()
    elif encoding == "wav":
        sink = discord.sinks.WaveSink()
    elif encoding == "pcm":
        sink = discord.sinks.PCMSink()
    elif encoding == "ogg":
        sink = discord.sinks.OGGSink()
    elif encoding == "mka":
        sink = discord.sinks.MKASink()
    elif encoding == "mkv":
        sink = discord.sinks.MKVSink()
    elif encoding == "mp4":
        sink = discord.sinks.MP4Sink()
    elif encoding == "m4a":
        sink = discord.sinks.M4ASink()
    else:
        return await ctx.respond("Invalid encoding.")

    vc.start_recording(
        sink,
        finished_callback,
        ctx.channel,
    )

    await ctx.respond("The recording has started!")


async def finished_callback(sink, channel: discord.TextChannel, *args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [
        discord.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]
    await channel.send(
        f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files
    )


@bot.command()
async def stoprecord(ctx):
    """Stop Recording

    Args:
        ctx (command): Stops recording
    """
    if ctx.guild.id in bot.connections:
        vc = bot.connections[ctx.guild.id]
        vc.stop_recording()
        del bot.connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.respond("Not recording in this guild.")

@bot.command()
async def clear(ctx, amount: int=1):
    """Clean messages

    Args:
        ctx (context): command object
        amount (int, optional): Number of messages to delete. Defaults to 1.
    """
    amount = int(amount)
    print(ctx)
    log_channel = bot.get_channel(872204827810209873)
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount+1)
        # await log_channel.send(f"{ctx.guild}\nPurge Completed - {amount} - on {ctx.channel.name} by {ctx.message.author}",delete_after=5.0)
        await ctx.send(f"LOGGER:\nPurge Completed - {amount} messages \nby: {ctx.author}")
        print("Purge Completed")
    else: 
        ctx.reply("Sorry you don't have enough permission to run this command!")
        await log_channel.send(f"Purge Failed - {amount} - on {ctx.channel.name} by {ctx.author}")
    
@bot.command()
async def serverinfo(ctx):
    print(ctx)
    """Get Server info

    Args:
        ctx (command context): bot object
    """
    # member_list = ""
    # for member in ctx.guild.members:
    #     member_list += str(member)
    #     print(member)
    server = ctx.guild
    info = "{ **Server Info** +\
                Name: {server.name}+\
                Server ID: {server.id}+\
                Creation Date: {server.created_at}+\
                Members: {server.member_count}+\
        }"
    await ctx.respond(info)
@bot.slash_command(guild_ids=guidid)
async def shammocheck(ctx,**message):
    print(message)
    # count = len(re.findall(r'\w+', contents))
    # paragraphs = contents.split('\n')
    # paragraphs = message['message'].split('\n')
    paragraphs = re.split("[?!.]", message['message'])
    print(paragraphs)
    issues = {}
    # sentences = []
    # for line in paragraphs:
    #     sentences = line.split('.')
    #     for sentence in sentences:
    #         count = len(re.findall(r'\w+', sentence))
    #         if count > 25:
    #             issues[count] = sentence
    for line in paragraphs:
        count = len(re.findall(r'\w+', line))
        print(count)
        if count > 25:
            issues[count] = line
    
    if len(issues) > 0:
        print(issues)
        embed=discord.Embed(title="**Total Issues: **" + str(len(issues)), color=0x22e27f)
        embed.set_author(name="Word Checker")
        for word,desc in issues.items():
            embed.add_field(name=word, value=desc, inline=False)
        embed.set_footer(text="Current Word Limit: 25")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="**No Issues Found!**", color=0x22e27f)
        embed.set_author(name="Word Checker")
        embed.set_footer(text="Current Word Limit: 25")
        await ctx.send(embed=embed)

bot.run(BOT_TOKEN)